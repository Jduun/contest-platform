import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import SecurityScopes
from jwt.exceptions import InvalidTokenError
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import (
    CredentialsError,
    NotEnoughPermissions,
    UsernameAlreadyExistsError,
)
from src.auth.models import Profile, Role, User
from src.auth.schemas import UserAdd, UserLogin
from src.config import settings
from src.database import DbSession


def verify_password(entered_password: str, password_hash: str):
    entered_password_bytes = entered_password.encode("utf-8")
    password_hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(entered_password_bytes, password_hash_bytes)


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(token_data: dict, expires_delta: timedelta) -> str:
    to_encode = token_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_role_by_name(db_session: AsyncSession, name: str) -> Optional[Role]:
    query = select(Role).filter_by(name=name)
    res = await db_session.execute(query)
    role = res.scalars().first()
    return role


async def add_user(db_session: AsyncSession, user_add: UserAdd) -> User:
    default_role = await get_role_by_name(db_session, name="user")
    add_user_query = (
        insert(User)
        .values(**user_add.model_dump(), role_id=default_role.id)
        .returning(User)
    )
    try:
        res = await db_session.execute(add_user_query)
        new_user = res.scalars().first()
        current_year = str(datetime.today().year)
        current_date = datetime.today().strftime("%Y-%m-%d")
        add_profile_query = (
            insert(Profile)
            .values(
                id=new_user.id,
                activity_calendar={
                    current_year: [{"date": current_date, "count": 1, "level": 1}]
                },
            )
            .returning(Profile)
        )
        res = await db_session.execute(add_profile_query)
        await db_session.commit()
    except SQLAlchemyError as e:
        raise UsernameAlreadyExistsError from e
    return new_user


async def update_image_url(
    db_session: AsyncSession, user_id: uuid.UUID, avatar_url: str
):
    query = update(Profile).filter_by(id=user_id).values(avatar_url=avatar_url)
    await db_session.execute(query)
    await db_session.commit()


async def get_user_by_id(
    db_session: AsyncSession, user_id: uuid.UUID
) -> Optional[User]:
    query = select(User).filter_by(id=user_id)
    res = await db_session.execute(query)
    return res.scalars().first()


async def get_user_by_username(
    db_session: AsyncSession, username: str
) -> Optional[User]:
    query = select(User).filter_by(username=username)
    res = await db_session.execute(query)
    return res.scalar()


async def authenticate(db_session: AsyncSession, user_login: UserLogin) -> User:
    user = await get_user_by_username(db_session, user_login.username)
    if not user:
        raise CredentialsError
    password_is_correct = verify_password(user_login.password, str(user.password))
    if not password_is_correct:
        raise CredentialsError
    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(settings.oauth2)],
    db_session: DbSession,
) -> User:
    try:
        payload = get_token_payload(token)
    except InvalidTokenError as e:
        raise CredentialsError from e

    username = payload.get("username")
    role_from_token = payload.get("role", [])
    if username is None:
        raise CredentialsError

    user = await get_user_by_username(db_session, username)
    if user is None:
        raise CredentialsError

    permitted_roles = security_scopes.scopes
    for role in permitted_roles:
        if role == role_from_token:
            return user
    raise NotEnoughPermissions


def get_token_payload(token: str) -> Any:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except InvalidTokenError:
        raise
    return payload


async def get_profile_by_username(
    db_session: AsyncSession,
    username: str,
) -> Profile:
    user = await get_user_by_username(db_session, username)
    query = select(Profile).filter_by(id=user.id)
    res = await db_session.execute(query)
    return res.scalars().first()
