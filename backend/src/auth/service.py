from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import CredentialsError
from src.auth.models import Role, User
from src.auth.schemas import TokenData, UserAdd, UserLogin
from src.config import settings


def verify_password(entered_password: str, password_hash: str):
    entered_password_bytes = entered_password.encode("utf-8")
    password_hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(entered_password_bytes, password_hash_bytes)


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(token_data: dict, expires_delta: timedelta) -> str:
    to_encode = token_data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_default_role(db_session: AsyncSession) -> Optional[Role]:
    query = select(Role).filter_by(name="user")
    res = await db_session.execute(query)
    default_role = res.scalars().first()
    return default_role


async def add_user(db_session: AsyncSession, user_add: UserAdd) -> User:
    default_role = await get_default_role(db_session)
    query = (
        insert(User)
        .values(**user_add.model_dump(), role_id=default_role.id)
        .returning(User)
    )
    res = await db_session.execute(query)
    await db_session.commit()
    return res.scalars().first()


async def get_user_by_username(
    db_session: AsyncSession, username: str
) -> Optional[User]:
    query = select(User).filter_by(username=username)
    res = await db_session.execute(query)
    return res.scalars().first()


async def authenticate(db_session: AsyncSession, user_login: UserLogin) -> User:
    user = await get_user_by_username(db_session, user_login.username)
    password_is_correct = verify_password(user_login.password, str(user.password))
    if not (user and password_is_correct):
        raise CredentialsError
    return user


async def get_current_user(db_session: AsyncSession, token: str) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        name: str = payload.get("sub")
        if name is None:
            raise CredentialsError
        token_data = TokenData(name=name)
    except InvalidTokenError:
        raise CredentialsError
    user = await get_user_by_username(db_session, token_data.name)
    if user is None:
        raise CredentialsError
    return user
