from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.auth.models import Base
from src.database import get_async_db_session
from src.main import app

test_db_url = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    test_db_url, connect_args={"check_same_thread": False}
)
async_session = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def override_get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in override_get_async_db_session():
        yield session


@pytest_asyncio.fixture
async def client():
    host, port = "127.0.0.1", "9000"
    async with AsyncClient(
        transport=ASGITransport(app=app, client=(host, port)), base_url="http://test"
    ) as client:
        yield client


# override dependency to replace prod db with test db
app.dependency_overrides[get_async_db_session] = override_get_async_db_session
