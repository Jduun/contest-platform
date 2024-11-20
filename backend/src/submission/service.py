import asyncio
import json
import uuid
from typing import Any

import requests
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

import src.problem.service as problem_service
from src.config import settings
from src.problem.models import Problem
from src.submission.models import Submission
from src.submission.schemas import SubmissionAdd


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


async def submit_code_using_sse(
    db_session: AsyncSession, submission_add: SubmissionAdd, user_id: uuid.UUID
):
    error_occurs = False
    problem: Problem = await problem_service.get_problem_by_id(
        db_session, submission_add.problem_id
    )
    tests = json.loads(problem.tests)
    submission_status = ""
    for i, test in enumerate(tests):
        if error_occurs:
            break
        submission_response = requests.post(
            f"{settings.code_exe_url}/submissions",
            data={
                "source_code": submission_add.code,
                "language_id": submission_add.language_id,
                "stdin": test["input"],
            },
        )
        submission_token = submission_response.json().get("token")
        IN_QUEUE_STATUS_ID = 1
        ACCEPTED_STATUS_ID = 3
        status_id = IN_QUEUE_STATUS_ID
        submission_status = ""
        stderr = ""
        while status_id < ACCEPTED_STATUS_ID:
            submission_result = requests.get(
                f"{settings.code_exe_url}/submissions/{submission_token}"
            )
            status = submission_result.json().get("status")
            status_id = status["id"]
            status_description = status["description"]
            stderr = submission_result.json().get("stderr")
            expected_output: str = submission_result.json().get("stdout")

            if expected_output:
                expected_output = expected_output.strip()

            real_output = test["output"]

            if status_id == ACCEPTED_STATUS_ID:
                if expected_output != real_output:
                    submission_status = f"Test {i}: Failed"
                    error_occurs = True
                elif i == len(tests) - 1:
                    submission_status = "Accepted"
                else:
                    submission_status = f"Test {i}: Passed"
            else:
                submission_status = f"Test {i}: {status_description}"
                if status_id > ACCEPTED_STATUS_ID:
                    error_occurs = True

            yield f"event: locationUpdate\ndata: {submission_status}\n\n"

            if error_occurs:
                break
            # await asyncio.sleep(0.5)

    if stderr is None:
        stderr = ""
    submission = await add_submission(
        db_session, submission_add, user_id, submission_status, stderr
    )


async def add_submission(
    db_session: AsyncSession,
    submission_add: SubmissionAdd,
    user_id: uuid.UUID,
    status: str,
    stderr: str,
) -> Submission:
    query = (
        insert(Submission)
        .values(
            **submission_add.model_dump(), user_id=user_id, status=status, stderr=stderr
        )
        .returning(Submission)
    )
    res = await db_session.execute(query)
    await db_session.commit()
    return res.scalars().first()
