import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, timestamp


class Role(Base):
    __tablename__ = "role"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    permissions = mapped_column(JSON, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str]
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("role.id"))
    rating: Mapped[int] = mapped_column(default=0)
    registered_at: Mapped[timestamp]

    submissions: Mapped[list["Submission"]] = relationship(back_populates="user")
    contests: Mapped[list["Contest"]] = relationship(
        back_populates="users", secondary="contest_user"
    )
    problems: Mapped[list["Problem"]] = relationship(back_populates="author")
    role: Mapped["Role"] = relationship(back_populates="users")
