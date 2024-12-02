import uuid

from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.contest.exceptions import (
    OffsetAndLimitMustNotBeNegative,
    ContestDoesNotExistError,
    ContestProblemDoesNotExistError,
    JoinContestError,
    UnjoinContestError,
)
from src.contest.models import Contest, ContestProblem, ContestUser
from src.problem.models import Problem
import src.problem.service as problem_service


async def get_contests(
    db_session: AsyncSession, offset: int, limit: int
) -> list[Contest]:
    query = select(Contest).offset(offset).limit(limit)
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
    await db_session.commit()
    return res.scalars().all()


async def get_contest_by_id(db_session: AsyncSession, contest_id: uuid.UUID) -> Contest:
    query = select(Contest).filter_by(id=contest_id)
    res = await db_session.execute(query)
    await db_session.commit()
    return res.scalars().first()


async def get_contest_problems(
    db_session: AsyncSession, contest_id: uuid.UUID
) -> list[Problem]:
    query = select(ContestProblem).filter_by(contest_id=contest_id)
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise ContestProblemDoesNotExistError
    await db_session.commit()
    return [
        await problem_service.get_problem_by_id(db_session, i.problem_id)
        for i in res.scalars()
    ]


async def join_contest(
    db_session: AsyncSession, contest_id: uuid.UUID, user_id: uuid.UUID
):
    contest = await get_contest_by_id(db_session, contest_id)
    if contest is None:
        raise ContestDoesNotExistError
    try:
        query = insert(ContestUser).values(contest_id=contest_id, user_id=user_id)
        await db_session.execute(query)
        await db_session.commit()
    except SQLAlchemyError:
        raise JoinContestError


async def unjoin_contest(
    db_session: AsyncSession, contest_id: uuid.UUID, user_id: uuid.UUID
):
    contest = await get_contest_by_id(db_session, contest_id)
    if contest is None:
        raise ContestDoesNotExistError
    try:
        query = delete(ContestUser).filter_by(contest_id=contest_id, user_id=user_id)
        await db_session.execute(query)
        await db_session.commit()
    except SQLAlchemyError:
        raise UnjoinContestError


async def get_join_contest_status(
    db_session: AsyncSession, contest_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    query = select(ContestUser).filter_by(contest_id=contest_id, user_id=user_id)
    res = await db_session.execute(query)
    contest_user = res.scalars().first()
    join_status = contest_user is not None
    return join_status
