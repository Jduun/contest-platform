from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# These imports solve the problem of using models before its declaration
from src.auth.models import *  # noqa
from src.config import settings
from src.contest.models import *  # noqa
from src.problem.models import *  # noqa
from src.submission.models import *  # noqa

engine = create_async_engine(settings.db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_async_db_session)]
