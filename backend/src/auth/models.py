import uuid
from typing import Optional

from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, timestamp


class Role(Base):
    __tablename__ = "role"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("role.id"))
    registered_at: Mapped[timestamp]

    role: Mapped["Role"] = relationship(back_populates="users", lazy="joined")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="user")
    problems: Mapped[list["Problem"]] = relationship(back_populates="author")
    contest_results: Mapped[list["ContestResult"]] = relationship(back_populates="user")

    def __str__(self):
        return self.username


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), primary_key=True)
    activity_calendar = Column(JSON)
    passed_contests = Column(JSON)
    avatar_url: Mapped[Optional[str]]
