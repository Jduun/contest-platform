import uuid
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm

import src.auth.service as auth_service
from src.auth.exceptions import (
    CredentialsError,
    NotEnoughPermissions,
    UsernameAlreadyExistsError,
)
from src.auth.models import User
from src.auth.roles import Roles
from src.auth.schemas import ProfileResponse, Token, UserAdd, UserLogin, UserResponse
from src.config import settings
from src.database import DbSession
from src.s3 import avatar_s3_client

auth_router = APIRouter(tags=["Auth"])
user_router = APIRouter(prefix="/users", tags=["Users"])


@auth_router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: DbSession,
):
    user_login = UserLogin.model_validate(form_data)
    try:
        user = await auth_service.authenticate(db_session, user_login)
    except CredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    access_token = auth_service.create_access_token(
        token_data={"username": user.username, "role": user.role.name},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/register", response_model=UserResponse)
async def register(
    user_add: UserAdd,
    db_session: DbSession,
):
    min_username_length = 1
    min_password_length = 8
    if len(user_add.username) < min_username_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username must be at least {min_username_length} characters long",
        )
    if len(user_add.password) < min_password_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password must be at least {min_password_length} characters long",
        )
    user_add.password = auth_service.get_password_hash(user_add.password)
    try:
        user = await auth_service.add_user(db_session, user_add)
    except UsernameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same name already exists",
        ) from e
    return user


@user_router.get("/me", response_model=UserResponse)
async def get_me(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
):
    try:
        return user
    except CredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except NotEnoughPermissions as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return await auth_service.get_user_by_id(db_session, user_id)


@user_router.get("/{username}/profile", response_model=ProfileResponse)
async def get_profile_by_username(
    username: str,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return await auth_service.get_profile_by_username(db_session, username)


@user_router.post("/avatars")
async def upload_avatar(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    avatar: UploadFile,
    db_session: DbSession,
) -> str:
    avatar_url = await avatar_s3_client.upload_file(
        file=avatar,
        key=user.username,
    )
    await auth_service.update_image_url(db_session, user.id, avatar_url)
    return avatar_url
