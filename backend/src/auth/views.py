from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import src.auth.service as auth_service
from src.auth.exceptions import CredentialsError
from src.auth.schemas import Token, UserAdd, UserLogin, UserResponse
from src.auth.service import authenticate, get_password_hash
from src.config import settings
from src.database import get_async_db_session

auth_router = APIRouter(tags=["Auth"])
user_router = APIRouter(prefix="/users", tags=["Users"])


@auth_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Token:
    user_login = UserLogin.model_validate(form_data)
    try:
        user = await authenticate(db_session, user_login)
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        token_data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/register", response_model=UserResponse)
async def register(
    user_add: UserAdd,
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Any:
    user_add.password = get_password_hash(user_add.password)
    user = await auth_service.add_user(db_session, user_add)
    return user


@user_router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: Annotated[str, Depends(settings.oauth2)],
    db_session: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> Any:
    try:
        return await auth_service.get_current_user(db_session, token)
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
