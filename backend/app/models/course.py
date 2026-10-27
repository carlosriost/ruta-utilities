"""Definicion del curso: niveles, puntos del mapa y sus temas."""

from typing import Any

from sqlalchemy import ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Phase(Base, TimestampMixin):
    """Nivel de madurez VPO. Es una zona del mapa."""

    __tablename__ = "phases"
    __table_args__ = (
        UniqueConstraint("order_index", name="uq_phases_order_index"),
        Index("ix_phases_order_index", "order_index"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    #: Cumplimiento minimo (%) de este nivel para abrir el siguiente.
    unlock_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    #: Clave de tema visual del frontend ("mint", "sky", "amber", "grape", "teal").
    theme: Mapped[str] = mapped_column(String(24), nullable=False, default="sky")
    icon: Mapped[str] = mapped_column(String(40), nullable=False, default="compass")

    nodes = relationship(
        "CourseNode",
        back_populates="phase",
        cascade="all, delete-orphan",
        order_by="CourseNode.order_index",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Phase {self.order_index}:{self.slug}>"


class CourseNode(Base, TimestampMixin):
    """Punto del mapa: un bloque VPO dentro de un nivel."""

    __tablename__ = "course_nodes"
    __table_args__ = (
        UniqueConstraint("phase_id", "order_index", name="uq_course_nodes_phase_order"),
        Index("ix_course_nodes_phase_id", "phase_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    phase_id: Mapped[int] = mapped_column(
        ForeignKey("phases.id", ondelete="CASCADE"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    icon: Mapped[str] = mapped_column(String(40), nullable=False, default="book")
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    #: Numero de temas del punto: el porcentaje del nivel se pondera con el.
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    phase = relationship("Phase", back_populates="nodes")
    activity = relationship(
        "Activity",
        back_populates="node",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<CourseNode {self.slug}>"


class Activity(Base, TimestampMixin):
    """Contenido de un punto: el contexto y la lista de temas.

    Los temas viven en ``payload['requirements']`` como una lista de objetos
    ``{code, title, detail}``. El contenido vive en PostgreSQL, no en
    componentes React.
    """

    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(
        ForeignKey("course_nodes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    objective: Mapped[str] = mapped_column(Text, nullable=False, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    node = relationship("CourseNode", back_populates="activity")

    @property
    def requirements(self) -> list[dict[str, str]]:
        return list((self.payload or {}).get("requirements", []))
