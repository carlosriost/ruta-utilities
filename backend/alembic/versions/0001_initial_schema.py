"""Esquema inicial de Ruta Utilities

Crea el catalogo del curso (fases, nodos, actividades, preguntas y opciones),
el usuario, el progreso y las insignias.

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-07
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    ]


def upgrade() -> None:
    # ------------------------------------------------------------------ users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("area", sa.String(length=80), nullable=False),
        sa.Column("plant", sa.String(length=120), nullable=False),
        sa.Column("role", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=True),
        sa.Column("external_id", sa.String(length=120), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    # external_id es unico e indexado: SQLAlchemy lo resuelve con un unico
    # indice UNIQUE, no con una constraint separada.
    op.create_index("ix_users_external_id", "users", ["external_id"], unique=True)

    # ----------------------------------------------------------------- phases
    op.create_table(
        "phases",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("unlock_threshold", sa.Integer(), nullable=False),
        sa.Column("theme", sa.String(length=24), nullable=False),
        sa.Column("icon", sa.String(length=40), nullable=False),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("order_index", name="uq_phases_order_index"),
    )
    op.create_index("ix_phases_order_index", "phases", ["order_index"])

    # ----------------------------------------------------------------- badges
    op.create_table(
        "badges",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("icon", sa.String(length=40), nullable=False),
        sa.Column("theme", sa.String(length=24), nullable=False),
        sa.Column("rule_type", sa.String(length=40), nullable=False),
        sa.Column("rule_ref", sa.String(length=80), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )

    # ----------------------------------------------------------- course_nodes
    op.create_table(
        "course_nodes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("phase_id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("activity_type", sa.String(length=24), nullable=False),
        sa.Column("icon", sa.String(length=40), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(["phase_id"], ["phases.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint(
            "phase_id", "order_index", name="uq_course_nodes_phase_order"
        ),
    )
    op.create_index("ix_course_nodes_phase_id", "course_nodes", ["phase_id"])

    # ------------------------------------------------------------- activities
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("node_id", sa.Integer(), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("passing_score", sa.Integer(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(["node_id"], ["course_nodes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("node_id"),
    )

    # -------------------------------------------------------------- questions
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(length=24), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "activity_id", "order_index", name="uq_questions_activity_order"
        ),
    )
    op.create_index("ix_questions_activity_id", "questions", ["activity_id"])

    # ---------------------------------------------------------- answer_options
    op.create_table(
        "answer_options",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "question_id", "order_index", name="uq_answer_options_question_order"
        ),
    )
    op.create_index("ix_answer_options_question_id", "answer_options", ["question_id"])

    # ---------------------------------------------------------- node_progress
    op.create_table(
        "node_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.ForeignKeyConstraint(["node_id"], ["course_nodes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "node_id", name="uq_node_progress_user_node"),
    )
    op.create_index("ix_node_progress_user_id", "node_progress", ["user_id"])

    # ----------------------------------------------------- user_phase_progress
    op.create_table(
        "user_phase_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("phase_id", sa.Integer(), nullable=False),
        sa.Column("unlocked", sa.Boolean(), nullable=False),
        sa.Column("percent", sa.Integer(), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
        sa.ForeignKeyConstraint(["phase_id"], ["phases.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "phase_id", name="uq_phase_progress_user_phase"),
    )
    op.create_index(
        "ix_user_phase_progress_user_id", "user_phase_progress", ["user_id"]
    )

    # -------------------------------------------------------------- responses
    op.create_table(
        "responses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("answer_option_id", sa.Integer(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(
            ["answer_option_id"], ["answer_options.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["node_id"], ["course_nodes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "question_id", name="uq_responses_user_question"),
    )
    op.create_index("ix_responses_user_node", "responses", ["user_id", "node_id"])

    # ------------------------------------------------------------ user_badges
    op.create_table(
        "user_badges",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("badge_id", sa.Integer(), nullable=False),
        sa.Column(
            "awarded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["badge_id"], ["badges.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "badge_id", name="uq_user_badges_user_badge"),
    )


def downgrade() -> None:
    op.drop_table("user_badges")
    op.drop_index("ix_responses_user_node", table_name="responses")
    op.drop_table("responses")
    op.drop_index("ix_user_phase_progress_user_id", table_name="user_phase_progress")
    op.drop_table("user_phase_progress")
    op.drop_index("ix_node_progress_user_id", table_name="node_progress")
    op.drop_table("node_progress")
    op.drop_index("ix_answer_options_question_id", table_name="answer_options")
    op.drop_table("answer_options")
    op.drop_index("ix_questions_activity_id", table_name="questions")
    op.drop_table("questions")
    op.drop_table("activities")
    op.drop_index("ix_course_nodes_phase_id", table_name="course_nodes")
    op.drop_table("course_nodes")
    op.drop_table("badges")
    op.drop_index("ix_phases_order_index", table_name="phases")
    op.drop_table("phases")
    op.drop_index("ix_users_external_id", table_name="users")
    op.drop_table("users")
