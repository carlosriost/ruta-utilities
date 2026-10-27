"""La ruta pasa de curso evaluado a lista de verificacion

Desaparecen los cuestionarios: cada punto del mapa es un bloque VPO y cada
requisito es un tema que se marca como cumplido o no cumplido. Por eso:

* se crea ``requirement_marks`` (la unica tabla de avance que queda),
* se eliminan ``questions``, ``answer_options``, ``responses`` y
  ``node_progress``, que solo servian para las preguntas y el estado derivado,
* ``course_nodes`` pierde ``activity_type`` y ``required`` (ya solo hay un tipo
  de punto y el umbral lo decide el porcentaje del nivel),
* ``activities`` pierde ``passing_score`` (no hay puntajes).

Revision ID: 0002_requirement_marks
Revises: 0001_initial
Create Date: 2026-09-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_requirement_marks"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "requirement_marks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=24), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
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
        sa.ForeignKeyConstraint(["node_id"], ["course_nodes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "code", name="uq_requirement_marks_user_code"),
    )
    op.create_index(
        "ix_requirement_marks_user_node", "requirement_marks", ["user_id", "node_id"]
    )

    op.drop_table("responses")
    op.drop_table("answer_options")
    op.drop_table("questions")
    op.drop_table("node_progress")

    op.drop_column("course_nodes", "activity_type")
    op.drop_column("course_nodes", "required")
    op.drop_column("activities", "passing_score")


def downgrade() -> None:
    op.add_column(
        "activities",
        sa.Column(
            "passing_score", sa.Integer(), nullable=False, server_default="100"
        ),
    )
    op.add_column(
        "course_nodes",
        sa.Column("required", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "course_nodes",
        sa.Column(
            "activity_type",
            sa.String(length=24),
            nullable=False,
            server_default="REQUIREMENTS",
        ),
    )

    op.create_table(
        "node_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(["node_id"], ["course_nodes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "node_id", name="uq_node_progress_user_node"),
    )
    op.create_index("ix_node_progress_user_id", "node_progress", ["user_id"])

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("question_type", sa.String(length=24), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "activity_id", "order_index", name="uq_questions_activity_order"
        ),
    )
    op.create_index("ix_questions_activity_id", "questions", ["activity_id"])

    op.create_table(
        "answer_options",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "question_id", "order_index", name="uq_answer_options_question_order"
        ),
    )
    op.create_index("ix_answer_options_question_id", "answer_options", ["question_id"])

    op.create_table(
        "responses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("node_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("answer_option_id", sa.Integer(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
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

    op.drop_index("ix_requirement_marks_user_node", table_name="requirement_marks")
    op.drop_table("requirement_marks")
