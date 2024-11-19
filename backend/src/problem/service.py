import uuid

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.problem.exceptions import (
    OffsetAndLimitMustNotBeNegative,
    ProblemDoesNotExistError,
)
from src.problem.models import Problem


async def get_problems(
    db_session: AsyncSession, offset: int, limit: int
) -> list[Problem]:
    query = select(Problem).offset(offset).limit(limit)
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
    await db_session.commit()
    return res.scalars().all()


async def get_problem_by_id(db_session: AsyncSession, problem_id: uuid.UUID) -> Problem:
    query = select(Problem).filter_by(id=problem_id)
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise ProblemDoesNotExistError
    await db_session.commit()
    return res.scalars().first()
