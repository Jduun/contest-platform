import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import select, func, distinct, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.problem.exceptions import (
    OffsetAndLimitMustNotBeNegative,
)
from src.problem.models import Problem
from src.submission.models import Submission


async def get_problems(
    db_session: AsyncSession, offset: int, limit: int
) -> list[Problem]:
    query = (
        select(Problem).order_by(Problem.created_at.desc()).offset(offset).limit(limit)
    )
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
    return res.scalars().all()


async def get_public_problems(
    db_session: AsyncSession, search_input: str, difficulty: str, offset: int, limit: int
) -> list[Problem]:
    criteria = [Problem.is_public == True]
    if search_input != "":
        criteria.append(Problem.title.ilike(f"%{search_input}%"))
    if difficulty != "all":
        criteria.append(Problem.difficulty == difficulty)
    
    query = (
        select(Problem)
        .filter(*criteria)
        .order_by(Problem.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
    problems = res.scalars().all()

    query = (
        select(func.count(Problem.id))
        .filter(*criteria)
    )
    res = await db_session.execute(query)
    count = res.scalar()

    return problems, count


async def get_public_problems_count(db_session: AsyncSession) -> int:
    query = select(func.count()).select_from(Problem)
    res = await db_session.execute(query)
    return res.scalar_one()


async def filter_problems(db_session: AsyncSession, search_input: str) -> list[Problem]:
    query = select(Problem).filter(Problem.title.ilike(f"%{input}%"))
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
    return res.scalars().all()


async def get_problem_by_id(db_session: AsyncSession, problem_id: uuid.UUID) -> Problem:
    query = select(Problem).filter_by(id=problem_id)
    res = await db_session.execute(query)
    return res.scalars().first()


"""
async def get_problem_score(db_session: AsyncSession, problem_id: uuid.UUID) -> int:
    max_score = 100
    query = select(ContestProblem).filter_by(problem_id=problem_id)
    res = await db_session.execute(query)
    contest_problem = res.scalars().first()
    if contest_problem is None:
        return 0
    contest_id = contest_problem.contest_id
    contest = await contest_service.get_contest_by_id(db_session, contest_id)
    contest_duration = (contest.end_time - contest.start_time).total_seconds()
    time_to_contest_end = (contest.end_time - datetime.now()).total_seconds()
    score = int(max_score * time_to_contest_end / contest_duration)
    return max(0, score)
"""


async def problem_is_solved(
    db_session: AsyncSession, user_id: uuid.UUID, problem_id: uuid.UUID
) -> Optional[bool]:
    query = select(Submission).filter_by(user_id=user_id, problem_id=problem_id)
    res = await db_session.execute(query)
    submissions_list = res.scalars().all()
    if len(submissions_list) == 0:
        return None
    for submission in submissions_list:
        if submission.status == "Accepted":
            return True
    return False


async def get_solved_problems_count(db_session: AsyncSession, user_id: uuid.UUID) -> dict:
    query = (
        select(
            func.count(distinct(Problem.id))
            .filter(Problem.difficulty == "easy")
            .label("easy_count"),
            func.count(distinct(Problem.id))
            .filter(Problem.difficulty == "medium")
            .label("medium_count"),
            func.count(distinct(Problem.id))
            .filter(Problem.difficulty == "hard")
            .label("hard_count"),
        )
        .join(Submission, Submission.problem_id == Problem.id)
        .filter(Submission.user_id == user_id, Submission.status == "Accepted")
    )
    result = await db_session.execute(query)
    easy_count, medium_count, hard_count = result.one()
    return {"easy": easy_count, "medium": medium_count, "hard": hard_count}
