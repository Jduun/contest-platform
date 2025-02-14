import uuid
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, case, delete, desc, func, insert, select, update
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import src.problem.service as problem_service
from src.contest.exceptions import (
    ContestDoesNotExistError,
    ContestProblemDoesNotExistError,
    JoinContestError,
    OffsetAndLimitMustNotBeNegative,
    UnjoinContestError,
)
from src.contest.models import Contest, ContestProblem, ContestResult, ContestUser
from src.problem.models import Problem


async def get_contests(
    db_session: AsyncSession, offset: int, limit: int
) -> list[Contest]:
    query = select(Contest).offset(offset).limit(limit)
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
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


async def calculate_penalty_time(
    db_session: AsyncSession,
    contest_id: uuid.UUID,
    problem_id: uuid.UUID,
    user_id: uuid.UUID,
    submission_status: str,
) -> int:
    query = select(ContestProblem).filter_by(contest_id=contest_id, problem_id=problem_id)
    res = await db_session.execute(query)
    contest_problem = res.scalars().first()
    if contest_problem is None:
        return 0

    query = select(ContestResult).filter_by(
        contest_id=contest_id, problem_id=problem_id, user_id=user_id
    )
    res = await db_session.execute(query)
    contest_result = res.scalars().first()

    contest = await get_contest_by_id(db_session, contest_id)

    penalty_time = 0
    problem_is_solved = submission_status == "Accepted"
    if problem_is_solved:
        penalty_time += int((datetime.now() - contest.start_time).total_seconds() // 60)
    else:
        penalty_time += 20
    if contest_result is None:
        query = insert(ContestResult).values(
            contest_id=contest_id,
            problem_id=problem_id,
            user_id=user_id,
            penalty_time=penalty_time,
            problem_is_solved=problem_is_solved,
        )
        await db_session.execute(query)
        await db_session.commit()
        return penalty_time
    if not contest_result.problem_is_solved:
        new_penalty_time = contest_result.penalty_time + penalty_time
        query = (
            update(ContestResult)
            .filter_by(
                contest_id=contest_id,
                problem_id=problem_id,
                user_id=user_id,
            )
            .values(penalty_time=new_penalty_time, problem_is_solved=problem_is_solved)
        )
        await db_session.execute(query)
        await db_session.commit()
        return new_penalty_time
    return contest_result.penalty_time


async def get_contest_leaderboard(
    db_session: AsyncSession, contest_id: uuid.UUID, offset=0, limit=10
):
    query = (
        select(
            ContestResult.user_id,
            func.count(case((ContestResult.problem_is_solved == True, 1))).label(
                "solved_count"
            ),
            func.sum(
                case(
                    (
                        ContestResult.problem_is_solved == True,
                        ContestResult.penalty_time,
                    )
                )
            ).label("total_penalty"),
            func.array_agg(
                case((ContestResult.problem_is_solved == True, ContestResult.problem_id))
            ).label("solved_problems"),
            func.array_agg(
                case(
                    (
                        ContestResult.problem_is_solved == True,
                        ContestResult.penalty_time,
                    )
                )
            ).label("penalty_times"),
        )
        .filter(ContestResult.contest_id == contest_id)
        .group_by(ContestResult.user_id)
        .order_by(desc("solved_count"), asc("total_penalty"))
        .offset(offset)
        .limit(limit)
    )
    res = await db_session.execute(query)
    rows = res.fetchall()
    leaderboard = [
        {
            "user_id": row.user_id,
            "solved_count": row.solved_count,
            "total_penalty": row.total_penalty,
            "solved_problems": row.solved_problems,
            "penalty_times": row.penalty_times,
        }
        for row in rows
    ]
    return leaderboard
