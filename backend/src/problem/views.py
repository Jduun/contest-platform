import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Security, status

import src.auth.service as auth_service
import src.problem.service as problem_service
from src.auth.models import User
from src.auth.roles import Roles
from src.database import DbSession
from src.problem.exceptions import (
    OffsetAndLimitMustNotBeNegative,
    ProblemDoesNotExistError,
)
from src.problem.schemas import ProblemResponse
from src.redis_cache import cache_response

problem_router = APIRouter(prefix="/problems", tags=["Problems"])
stats_router = APIRouter(prefix="/stats", tags=["Stats"])


"""@problem_router.get("/count")
async def get_problems_count(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    count = await problem_service.get_public_problems_count(db_session)
    return {"count": count}
"""


@problem_router.get("/")
@cache_response(60, ignore_keys=["user", "db_session"])
async def get_public_problems(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
    search_input: str,
    difficulty: str,
    offset: int = 0,
    limit: int = 10,
):
    try:
        problems, count = await problem_service.get_public_problems(
            db_session, search_input, difficulty, offset, limit
        )
    except OffsetAndLimitMustNotBeNegative as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset and limit must not be negative",
        ) from e
    return {"problems": problems, "count": count}


@problem_router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    try:
        problem = await problem_service.get_problem_by_id(db_session, problem_id)
    except ProblemDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no problem with this id",
        ) from e
    return problem


"""
@problem_router.get("/{problem_id}/score")
async def get_problem(
    problem_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return await problem_service.get_problem_score(db_session, problem_id)
"""


@problem_router.get("/{problem_id}/is-solved")
async def problem_is_solved(
    problem_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return await problem_service.problem_is_solved(db_session, user.id, problem_id)


@stats_router.get("/problems")
async def get_problem_stats(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return await problem_service.get_solved_problems_count(db_session, user.id)
