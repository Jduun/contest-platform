import uuid
from datetime import datetime

from pydantic import BaseModel


class SubmissionAdd(BaseModel):
    code: str
    problem_id: uuid.UUID
    language_id: int


class SubmissionResponse(SubmissionAdd):
    id: uuid.UUID
    status: str
    submitted_at: datetime
