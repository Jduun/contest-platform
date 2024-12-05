import uuid
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm

import src.auth.service as auth_service
from src.auth.exceptions import CredentialsError, UsernameAlreadyExistsError
from src.auth.models import User
from src.auth.roles import Roles
from src.auth.schemas import Token, UserAdd, UserLogin, UserResponse
from src.config import settings
from src.database import DbSession

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
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
    user_add.password = auth_service.get_password_hash(user_add.password)
    try:
        user = await auth_service.add_user(db_session, user_add)
    except UsernameAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем уже существует",
        )
    return user


@user_router.get("/me", response_model=UserResponse)
async def get_me(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ]
):
    try:
        return user
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
