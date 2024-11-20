import json
from typing import Annotated

import requests
from fastapi import APIRouter, Body, Depends, HTTPException, Security, status
from starlette.responses import StreamingResponse

import src.auth.service as auth_service
import src.submission.service as submission_service
from src.auth.models import User
from src.auth.roles import Roles
from src.config import settings
from src.database import DbSession
from src.submission.schemas import SubmissionAdd

submission_router = APIRouter(prefix="/submissions", tags=["Submissions"])


@submission_router.post("/")
async def submit_code(
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
    # TODO: error handling, add limitations, language
    # I use Server Side Events (SSE) here
    return StreamingResponse(
        submission_service.submit_code_using_sse(db_session, submission_add, user.id),
        media_type="text/event-stream",
    )
