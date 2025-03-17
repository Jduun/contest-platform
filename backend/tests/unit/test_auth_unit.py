from typing import Optional
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import CredentialsError
from src.auth.models import Profile, Role, User
from src.auth.schemas import UserLogin
from src.auth.service import (
    authenticate,
    get_profile_by_username,
    get_role_by_name,
    get_user_by_username,
)


@pytest.fixture
def dummy_user():
    return User(id=uuid4(), username="testuser", password="dummy_hash")


@pytest.fixture
def dummy_role():
    return Role(id=uuid4(), name="admin")


@pytest.mark.asyncio
async def test_get_role_by_name_found(dummy_role):
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = dummy_role

    mock_result = AsyncMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result

    result = await get_role_by_name(mock_session, "admin")
    assert result == dummy_role


@pytest.mark.asyncio
async def test_get_role_by_name_not_found():
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None

    mock_result = AsyncMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result

    result = await get_role_by_name(mock_session, "nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_username_found(dummy_user):
    mock_result = AsyncMock()
    mock_result.scalar = MagicMock(return_value=dummy_user)

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result

    result: Optional[User] = await get_user_by_username(mock_session, "testuser")

    assert result == dummy_user
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_username_not_found():
    mock_result = AsyncMock()
    mock_result.scalar = MagicMock(return_value=None)

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result

    result: Optional[User] = await get_user_by_username(mock_session, "nonexistent")

    assert result is None
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_profile_by_username_found(monkeypatch):
    dummy_user = User(id=1, username="testuser", password="dummy_password")
    dummy_profile = Profile(id=1)

    async def mock_get_user_by_username(
        db_session: AsyncSession, username: str
    ) -> User:
        return dummy_user

    monkeypatch.setattr(
        "src.auth.service.get_user_by_username", mock_get_user_by_username
    )

    mock_scalars = MagicMock()
    mock_scalars.first.return_value = dummy_profile

    mock_result = AsyncMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result

    result: Optional[Profile] = await get_profile_by_username(mock_session, "testuser")

    assert result == dummy_profile
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_profile_by_username_not_found(monkeypatch, dummy_user):
    async def mock_get_user_by_username(
        db_session: AsyncSession, username: str
    ) -> User:
        return dummy_user

    monkeypatch.setattr(
        "src.auth.service.get_user_by_username", mock_get_user_by_username
    )

    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None

    mock_result = AsyncMock()
    mock_result.scalars = MagicMock(return_value=mock_scalars)

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = mock_result

    result: Optional[Profile] = await get_profile_by_username(mock_session, "unknown")
    assert result is None
    mock_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_authenticate_valid(monkeypatch, dummy_user):
    user_login = UserLogin(username=dummy_user.username, password=dummy_user.password)

    async def mock_get_user_by_username(
        db_session: AsyncSession, username: str
    ) -> Optional[User]:
        return dummy_user

    def mock_verify_password(entered_password: str, password_hash: str):
        return True

    monkeypatch.setattr(
        "src.auth.service.get_user_by_username", mock_get_user_by_username
    )
    monkeypatch.setattr("src.auth.service.verify_password", mock_verify_password)

    mock_session = AsyncMock(spec=AsyncSession)
    result = await authenticate(mock_session, user_login)
    assert result == dummy_user


@pytest.mark.asyncio
async def test_authenticate_user_not_found(monkeypatch, dummy_user):
    user_login = UserLogin(username=dummy_user.username, password=dummy_user.password)

    async def mock_get_user_by_username(
        db_session: AsyncSession, username: str
    ) -> Optional[User]:
        return None

    monkeypatch.setattr(
        "src.auth.service.get_user_by_username", mock_get_user_by_username
    )
    mock_session = AsyncMock(spec=AsyncSession)

    with pytest.raises(CredentialsError):
        await authenticate(mock_session, user_login)


@pytest.mark.asyncio
async def test_authenticate_incorrect_password(monkeypatch, dummy_user):
    user_login = UserLogin(username=dummy_user.username, password=dummy_user.password)

    async def mock_get_user_by_username(
        db_session: AsyncSession, username: str
    ) -> Optional[User]:
        return dummy_user

    def mock_verify_password(entered_password: str, password_hash: str):
        return False

    monkeypatch.setattr(
        "src.auth.service.get_user_by_username", mock_get_user_by_username
    )
    monkeypatch.setattr("src.auth.service.verify_password", mock_verify_password)

    mock_session = AsyncMock(spec=AsyncSession)

    with pytest.raises(CredentialsError):
        await authenticate(mock_session, user_login)
