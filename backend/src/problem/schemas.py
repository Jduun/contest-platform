import uuid
from datetime import datetime

from pydantic import BaseModel


class ProblemAdd(BaseModel):
    title: str
    statement: str
    memory_limit: int
    time_limit: int
    difficulty: str
    is_public: bool


class ProblemUpdate(ProblemAdd):
    id: uuid.UUID
    ...


class ProblemResponse(ProblemUpdate):
    author_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
