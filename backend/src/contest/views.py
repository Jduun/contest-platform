import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Security, status

import src.auth.service as auth_service
import src.contest.service as contest_service
from src.auth.models import User
from src.auth.roles import Roles
from src.contest.exceptions import (
    ContestDoesNotExistError,
    ContestProblemDoesNotExistError,
    JoinContestError,
    OffsetAndLimitMustNotBeNegative,
    UnjoinContestError,
)
from src.contest.schemas import ContestResponse, SubmissionStatus
from src.database import DbSession
from src.problem.schemas import ProblemResponse

contest_router = APIRouter(prefix="/contests", tags=["Contests"])


@contest_router.get("/", response_model=list[ContestResponse])
async def get_contests(
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
        contests = await contest_service.get_contests(db_session, offset, limit)
    except OffsetAndLimitMustNotBeNegative:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset and limit must not be negative",
        )
    return contests


@contest_router.get("/{contest_id}", response_model=ContestResponse)
async def get_contest(
    contest_id: uuid.UUID,
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
        contest = await contest_service.get_contest_by_id(db_session, contest_id)
    except ContestDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no contest with this id",
        )
    return contest


@contest_router.get("/{contest_id}/problems", response_model=list[ProblemResponse])
async def get_contest_problems(
    contest_id: uuid.UUID,
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
        contest = await contest_service.get_contest_by_id(db_session, contest_id)
    except ContestDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no contest with this id",
        )
    if contest.start_time >= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The contest hasn't started yet.",
        )
    try:
        problems = await contest_service.get_contest_problems(db_session, contest_id)
    except ContestProblemDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no problems within contest",
        )
    return problems


@contest_router.post("/{contest_id}/join")
async def join_contest(
    contest_id: uuid.UUID,
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
        await contest_service.join_contest(db_session, contest_id, user.id)
    except ContestDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found",
        )
    except JoinContestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You've probably already joined the contest.",
        )


@contest_router.delete("/{contest_id}/unjoin")
async def unjoin_contest(
    contest_id: uuid.UUID,
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
        await contest_service.unjoin_contest(db_session, contest_id, user.id)
    except ContestDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found",
        )
    except UnjoinContestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You've probably already joined the contest.",
        )


@contest_router.get("/{contest_id}/join-status")
async def get_join_contest_status(
    contest_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return {
        "join status": await contest_service.get_join_contest_status(
            db_session, contest_id, user.id
        )
    }


@contest_router.post("/{contest_id}/problems/{problem_id}/set-penalty-time")
async def set_penalty_time(
    contest_id: uuid.UUID,
    problem_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
    submission_status: SubmissionStatus,
):
    return {
        "penalty time": await contest_service.calculate_penalty_time(
            db_session, contest_id, problem_id, user.id, submission_status.status
        )
    }


@contest_router.get("/{contest_id}/leaderboard")
async def get_leaderboard(
    contest_id: uuid.UUID,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    return {
        "leaderboard": await contest_service.get_contest_leaderboard(
            db_session,
            contest_id,
        )
    }
