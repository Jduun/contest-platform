from datetime import datetime
from enum import Enum
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Difficulty(Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


timestamp = Annotated[datetime, mapped_column(server_default=text("now()"))]

timestamp_updated = Annotated[
    datetime,
    mapped_column(server_default=text("now()"), onupdate=text("now()")),
]
