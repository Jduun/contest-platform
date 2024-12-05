import uuid
from datetime import datetime

from pydantic import BaseModel

from src.models import Difficulty


class ProblemAdd(BaseModel):
    title: str
    statement: str
    tests: str
    memory_limit: int
    time_limit: int
    difficulty: Difficulty
    is_public: bool


class ProblemUpdate(ProblemAdd):
    id: uuid.UUID
    ...


class ProblemResponse(ProblemUpdate):
    author_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
