import uuid

from sqlalchemy import JSON, Column, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, Difficulty, timestamp, timestamp_updated


class Problem(Base):
    __tablename__ = "problem"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(255), unique=True)
    statement: Mapped[str]
    tests: Mapped[str]
    memory_limit: Mapped[int]
    time_limit: Mapped[int]
    difficulty: Mapped[Difficulty]
    is_public: Mapped[bool]
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp_updated]

    submissions: Mapped[list["Submission"]] = relationship(back_populates="problem")
    author: Mapped["User"] = relationship(back_populates="problems", lazy="joined")
    contest_results: Mapped[list["ContestResult"]] = relationship(
        back_populates="problem"
    )

    def __str__(self):
        return self.title
