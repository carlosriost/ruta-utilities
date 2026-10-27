"""Modelo de usuario."""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    """Operario que recorre la Ruta Utilities.

    La aplicacion no muestra datos personales: este registro existe solo para
    asociar las marcas de los temas. Cuando se integre Microsoft Entra ID,
    ``external_id`` guardara el ``oid`` del token corporativo.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    area: Mapped[str] = mapped_column(String(80), nullable=False)
    plant: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str | None] = mapped_column(String(180), unique=True, nullable=True)
    # Identificador del proveedor externo (Microsoft Entra ID -> claim "oid").
    external_id: Mapped[str | None] = mapped_column(
        String(120), unique=True, nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    marks = relationship(
        "RequirementMark", back_populates="user", cascade="all, delete-orphan"
    )
    phase_progress = relationship(
        "UserPhaseProgress", back_populates="user", cascade="all, delete-orphan"
    )
    badges = relationship(
        "UserBadge", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - ayuda de depuracion
        return f"<User id={self.id} name={self.name!r}>"
