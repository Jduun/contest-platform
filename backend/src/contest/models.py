import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, timestamp, timestamp_updated


class Contest(Base):
    __tablename__ = "contest"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    start_time: Mapped[timestamp]
    end_time: Mapped[timestamp]
    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp_updated]


class ContestUser(Base):
    __tablename__ = "contest_user"

    contest_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contest.id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)


class ContestProblem(Base):
    __tablename__ = "contest_problem"

    contest_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("contest.id"), primary_key=True
    )
    problem_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("problem.id"), primary_key=True
    )
