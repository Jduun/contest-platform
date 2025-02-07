import math
import asyncio
import base64
import json
import os
import uuid
from typing import Any
from datetime import datetime

import requests
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import src.problem.service as problem_service
from src.config import settings
from src.auth.models import Profile
from src.problem.models import Problem
from src.submission.models import Submission
from src.submission.schemas import SubmissionAdd
from src.submission.exceptions import OffsetAndLimitMustNotBeNegative


def string_to_base64(string: str) -> str:
    string_bytes = string.encode("utf-8")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("utf-8")
    return base64_string


def base64_to_string(base64_string: str) -> str:
    base64_bytes = base64.b64decode(base64_string)
    decoded_string = base64_bytes.decode("utf-8")
    return decoded_string


def get_languages():
    languages = [
        {"id": 50, "name": "C (GCC 9.2.0)"},
        {"id": 54, "name": "C++ (GCC 9.2.0)"},
        {"id": 51, "name": "C# (Mono 6.6.0.161)"},
        {"id": 60, "name": "Go (1.13.5)"},
        {"id": 62, "name": "Java (OpenJDK 13.0.1)"},
        {"id": 63, "name": "JavaScript (Node.js 12.14.0)"},
        {"id": 67, "name": "Pascal (FPC 3.0.4)"},
        {"id": 68, "name": "PHP (7.4.1)"},
        {"id": 71, "name": "Python (3.8.1)"},
        {"id": 72, "name": "Ruby (2.7.0)"},
        {"id": 73, "name": "Rust (1.40.0)"},
        {"id": 74, "name": "TypeScript (3.7.4)"},
    ]
    return languages


async def add_submission(
    db_session: AsyncSession,
    submission_add: SubmissionAdd,
    user_id: uuid.UUID,
    status: str,
    stderr: str,
) -> Submission:
    add_submission_query = (
        insert(Submission)
        .values(
            **submission_add.model_dump(), user_id=user_id, status=status, stderr=stderr
        )
        .returning(Submission)
    )
    submission_query_result = await db_session.execute(add_submission_query)
    current_year = str(datetime.today().year)
    current_date = datetime.today().strftime("%Y-%m-%d")
    get_user_profile_query = (
        select(Profile)
        .filter_by(id=user_id)
    )
    get_user_profile_query_result = await db_session.execute(get_user_profile_query)
    user_profile = get_user_profile_query_result.scalars().first()
    acitivity_calendar = user_profile.activity_calendar
    today_activity_exist = False
    if current_year not in acitivity_calendar:
        acitivity_calendar[current_year] = []
    for activity in acitivity_calendar[current_year]:
        if activity["date"] == current_date:
            activity["count"] += 1
            activity["level"] = min(math.ceil(activity["count"] / 5), 4)
            today_activity_exist = True
            break
    if not today_activity_exist:
        acitivity_calendar[current_year].append({
            "date": current_date,
            "count": 1,
            "level": 1
        })
    update_activity_calendar_query = (
        update(Profile)
        .filter_by(id=user_id)
        .values(activity_calendar=acitivity_calendar)
    )
    await db_session.execute(update_activity_calendar_query)
    await db_session.commit()
    return submission_query_result.scalars().first()


async def get_submission_by_id(
    db_session: AsyncSession, submission_id: uuid.UUID
) -> Submission:
    query = select(Submission).filter_by(id=submission_id)
    res = await db_session.execute(query)
    return res.scalars().first()


async def submit_code_sse(db_session: AsyncSession, submission_id: uuid.UUID):
    submission = await get_submission_by_id(db_session, submission_id)
    problem: Problem = await problem_service.get_problem_by_id(
        db_session, submission.problem_id
    )
    tests = json.loads(problem.tests)
    submissions = []
    for test in tests:
        submissions.append(
            {
                "language_id": submission.language_id,
                "source_code": submission.code,
                "stdin": test["input"],
                "expected_output": test["output"],
                "cpu_time_limit": problem.time_limit,
                "memory_limit": problem.memory_limit * 1024,
            }
        )

    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST"),
        "Content-Type": "application/json",
    }

    submissions_batch_response = requests.post(
        f"{settings.code_exe_url}/submissions/batch",
        json={"submissions": submissions},
        headers=headers,
    )

    submission_tokens = [i["token"] for i in submissions_batch_response.json()]

    PROCESSING_STATUS_ID = 1
    ACCEPTED_STATUS_ID = 3
    status_id = -1
    status_description = ""
    stderr = ""
    while status_id < ACCEPTED_STATUS_ID:
        submissions_response = requests.get(
            f"{settings.code_exe_url}/submissions/batch",
            params={"tokens": ",".join(submission_tokens), "base64_encoded": "true"},
            headers=headers,
        )
        submissions_info = submissions_response.json()

        statuses = []
        for test_number, submission_info in enumerate(submissions_info["submissions"]):
            curr_status_id = submission_info["status"]["id"]
            curr_status_description = submission_info["status"]["description"]
            curr_stderr = submission_info["stderr"]
            statuses.append(
                (curr_status_id, curr_status_description, test_number, curr_stderr)
            )
        if all([i[0] == ACCEPTED_STATUS_ID for i in statuses]):
            status_id = ACCEPTED_STATUS_ID
            status_description = "Accepted"
        elif any([i[0] < ACCEPTED_STATUS_ID for i in statuses]):
            status_id = PROCESSING_STATUS_ID
            status_description = "Processing"
        else:
            for i in statuses:
                if i[0] > ACCEPTED_STATUS_ID:
                    status_id = i[0]
                    status_description = f"Test {i[2] + 1}: {i[1]}"
                    stderr = curr_stderr
                    break

        yield f"event: locationUpdate\ndata: {status_description}{'. ' + base64_to_string(stderr) if stderr else ''}\n\n"
        await asyncio.sleep(5)

    stderr = base64_to_string(stderr) if stderr else ""
    query = (
        update(Submission)
        .filter_by(id=submission_id)
        .values(status=status_description, stderr=stderr)
    )
    await db_session.execute(query)    
    await db_session.commit()


async def get_submissions(
    db_session: AsyncSession, user_id: uuid.UUID, problem_id: uuid.UUID, offset: int, limit: int
) -> list[Submission]:
    query = (
        select(Submission)
        .filter_by(user_id=user_id, problem_id=problem_id)
        .order_by(Submission.submitted_at.desc())
        .offset(offset)
        .limit(limit)
    )
    try:
        res = await db_session.execute(query)
    except SQLAlchemyError:
        raise OffsetAndLimitMustNotBeNegative
    return res.scalars().all()
