"""Avance del usuario: marcas por tema y estado de cada nivel.

Cada tema es binario y el valor por defecto es "no cumple": por eso solo se
persiste la EXCEPCION, es decir, los temas marcados como cumplidos. Que exista
una fila en ``requirement_marks`` para (usuario, codigo) significa "cumple";
que no exista significa "no cumple". No hay un tercer estado de "sin marcar".

El estado de un punto del mapa y el porcentaje de cada nivel se derivan de
estas marcas en :mod:`app.services.progress_service`, de modo que no puede
existir un estado persistido incoherente con las reglas.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class RequirementMark(Base, TimestampMixin):
    """Un tema marcado como cumplido. Su ausencia significa "no cumple"."""

    __tablename__ = "requirement_marks"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="uq_requirement_marks_user_code"),
        Index("ix_requirement_marks_user_node", "user_id", "node_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    node_id: Mapped[int] = mapped_column(
        ForeignKey("course_nodes.id", ondelete="CASCADE"), nullable=False
    )
    #: Codigo oficial del requisito VPO (por ejemplo "R.1.7.1.1").
    code: Mapped[str] = mapped_column(String(24), nullable=False)

    user = relationship("User", back_populates="marks")


class UserPhaseProgress(Base, TimestampMixin):
    """Foto del estado de un nivel: si esta abierto y su cumplimiento."""

    __tablename__ = "user_phase_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "phase_id", name="uq_phase_progress_user_phase"),
        Index("ix_user_phase_progress_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    phase_id: Mapped[int] = mapped_column(
        ForeignKey("phases.id", ondelete="CASCADE"), nullable=False
    )
    unlocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unlocked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user = relationship("User", back_populates="phase_progress")
    phase = relationship("Phase")
