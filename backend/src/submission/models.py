import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, timestamp


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str]
    language_id: Mapped[int]
    status: Mapped[str]
    stderr: Mapped[str]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("problem.id"))
    submitted_at: Mapped[timestamp]

    user: Mapped["User"] = relationship(back_populates="submissions", lazy="joined")
    problem: Mapped["Problem"] = relationship(
        back_populates="submissions", lazy="joined"
    )
