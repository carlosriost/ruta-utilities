"""Insignias y su asignacion a usuarios."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Badge(Base, TimestampMixin):
    """Definicion de una insignia. Las reglas las evalua FastAPI."""

    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    icon: Mapped[str] = mapped_column(String(40), nullable=False, default="award")
    theme: Mapped[str] = mapped_column(String(24), nullable=False, default="amber")
    #: Regla evaluada por :mod:`app.services.badge_service` (ver ``BadgeRule``).
    rule_type: Mapped[str] = mapped_column(String(40), nullable=False)
    #: Referencia opcional de la regla (p. ej. el slug de la fase).
    rule_ref: Mapped[str | None] = mapped_column(String(80), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    awards = relationship(
        "UserBadge", back_populates="badge", cascade="all, delete-orphan"
    )


class UserBadge(Base):
    """Insignia obtenida por un usuario."""

    __tablename__ = "user_badges"
    __table_args__ = (
        UniqueConstraint("user_id", "badge_id", name="uq_user_badges_user_badge"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    badge_id: Mapped[int] = mapped_column(
        ForeignKey("badges.id", ondelete="CASCADE"), nullable=False
    )
    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="awards")
