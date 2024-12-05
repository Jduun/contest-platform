import uuid
from datetime import datetime

from pydantic import BaseModel


class ContestAdd(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime


class ContestResponse(ContestAdd):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ContestResult(BaseModel):
    id: uuid.UUID
    problem_is_solved: bool
    penalty_time: int
    user_id: uuid.UUID
    problem_id: uuid.UUID
    contest_id: uuid.UUID


class SubmissionStatus(BaseModel):
    status: str
