import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Difficulty, timestamp, timestamp_updated


class Problem(Base):
    __tablename__ = "problem"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(255), unique=True)
    statement: Mapped[str]
    tests = mapped_column(JSON, nullable=False)
    memory_limit: Mapped[int]
    time_limit: Mapped[int]
    difficulty: Mapped[Difficulty]
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp_updated]
