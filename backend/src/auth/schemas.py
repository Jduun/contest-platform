from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserAdd(UserLogin): ...


class UserResponse(BaseModel):
    id: UUID
    username: str
    role_id: UUID
    registered_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class ProfileResponse(BaseModel):
    avatar_url: Optional[str]
    activity_calendar: Optional[dict]
    passed_contests: Optional[dict]
