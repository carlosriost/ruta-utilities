"""Consultas sobre usuarios."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_name(self, name: str) -> User | None:
        return self.db.execute(
            select(User).where(User.name == name)
        ).scalar_one_or_none()

    def get_by_external_id(self, external_id: str) -> User | None:
        """Usado por la futura integracion con Microsoft Entra ID (claim oid)."""
        return self.db.execute(
            select(User).where(User.external_id == external_id)
        ).scalar_one_or_none()

    def get_demo_user(self) -> User | None:
        """Primer usuario registrado: en esta demo, Carlos Rios."""
        return self.db.execute(
            select(User).order_by(User.id).limit(1)
        ).scalar_one_or_none()
