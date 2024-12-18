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

problem_router = APIRouter(prefix="/problems", tags=["Problems"])


@problem_router.get("/", response_model=list[ProblemResponse])
async def get_public_problems(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
    offset: int = 0,
    limit: int = 10,
):
    try:
        problems = await problem_service.get_public_problems(db_session, offset, limit)
    except OffsetAndLimitMustNotBeNegative:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset and limit must not be negative",
        )
    return problems


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
    except ProblemDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no problem with this id",
        )
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
