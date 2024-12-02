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
