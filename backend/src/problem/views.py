import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.auth.service as auth_service
import src.problem.service as problem_service
import src.utils as utils
from src.auth.exceptions import CredentialsError
from src.auth.models import User
from src.auth.roles import Roles
from src.config import settings
from src.database import DbSession
from src.problem.exceptions import (
    OffsetAndLimitMustNotBeNegative,
    ProblemAlreadyExistsError,
    ProblemDoesNotExistError,
)
from src.problem.schemas import ProblemAdd, ProblemResponse, ProblemUpdate

problem_router = APIRouter(prefix="/problems", tags=["Problems"])


@problem_router.get("/", response_model=list[ProblemResponse])
async def get_problems(
    offset: int,
    limit: int,
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
        problem = await problem_service.get_problems(db_session, offset, limit)
    except OffsetAndLimitMustNotBeNegative:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset and limit must not be negative",
        )
    return problem


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
