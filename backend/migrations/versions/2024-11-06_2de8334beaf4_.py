"""empty message

Revision ID: 2de8334beaf4
Revises: 
Create Date: 2024-11-06 11:29:37.503108

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from src.auth.roles import Roles

# revision identifiers, used by Alembic.
revision: str = "2de8334beaf4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contest",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "start_time", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "end_time", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    role_table = op.create_table(
        "role",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column(
            "registered_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "contest_user",
        sa.Column("contest_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contest_id"],
            ["contest.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("contest_id", "user_id"),
    )
    op.create_table(
        "problem",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("author_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("statement", sa.String(), nullable=False),
        sa.Column("memory_limit", sa.Integer(), nullable=False),
        sa.Column("time_limit", sa.Integer(), nullable=False),
        sa.Column(
            "difficulty",
            sa.Enum("easy", "medium", "hard", name="difficulty"),
            nullable=False,
        ),
        sa.Column("is_in_contest", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("tests", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "contest_problem",
        sa.Column("contest_id", sa.Uuid(), nullable=False),
        sa.Column("problem_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contest_id"],
            ["contest.id"],
        ),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problem.id"],
        ),
        sa.PrimaryKeyConstraint("contest_id", "problem_id"),
    )
    op.create_table(
        "submission",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("problem_id", sa.Uuid(), nullable=False),
        sa.Column(
            "submitted_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problem.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.bulk_insert(
        role_table,
        [
            {
                "id": uuid.uuid4(),
                "name": Roles.user,
            },
            {
                "id": uuid.uuid4(),
                "name": Roles.organizer,
            },
            {
                "id": uuid.uuid4(),
                "name": Roles.admin,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("submission")
    op.drop_table("contest_problem")
    op.drop_table("problem")
    op.drop_table("contest_user")
    op.drop_table("user")
    op.drop_table("role")
    op.drop_table("contest")

    op.execute("drop type difficulty")
