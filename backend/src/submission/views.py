import json
import uuid
from typing import Annotated

import requests
from fastapi import APIRouter, Body, Depends, HTTPException, Security, status, Path
from starlette.responses import StreamingResponse

import src.auth.service as auth_service
import src.submission.service as submission_service
from src.auth.models import User
from src.auth.roles import Roles
from src.config import settings
from src.database import DbSession
from src.submission.schemas import SubmissionAdd, SubmissionResponse
from src.submission.exceptions import OffsetAndLimitMustNotBeNegative

submission_router = APIRouter(prefix="/submissions", tags=["Submissions"])


@submission_router.post("/")
async def init_submission(
    submission_add: SubmissionAdd,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
):
    submission = await submission_service.add_submission(
        db_session, submission_add, user.id, "In progress", ""
    )
    return submission.id


@submission_router.get("/{submission_id}")
async def submit_code(
    db_session: DbSession,
    submission_id: uuid.UUID,
):
    # I use Server Side Events (SSE) here
    return StreamingResponse(
        submission_service.submit_code_sse(db_session, submission_id),
        media_type="text/event-stream",
    )


@submission_router.get("/", response_model=list[SubmissionResponse])
async def get_submissions(
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
    db_session: DbSession,
    problem_id: uuid.UUID,
    offset: int = 0,
    limit: int = 10,
):
    try:
        submissions = await submission_service.get_submissions(db_session, user.id, problem_id, offset, limit)
    except OffsetAndLimitMustNotBeNegative:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset and limit must not be negative",
        )
    return submissions
