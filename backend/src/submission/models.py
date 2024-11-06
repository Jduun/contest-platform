import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, timestamp


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("problem.id"))
    contest_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("contest.id"))
    score: Mapped[int]
    submitted_at: Mapped[timestamp]
