"""Reinicio del avance registrado."""

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.badge_repository import BadgeRepository
from app.repositories.progress_repository import ProgressRepository


class DemoService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.progress = ProgressRepository(db)
        self.badges = BadgeRepository(db)

    def reset_progress(self, user: User) -> None:
        """Borra SOLO el avance del usuario.

        Se conservan intactos: usuario, niveles, puntos, temas y la
        definicion de las insignias.
        """
        self.progress.delete_all_progress(user.id)
        self.badges.delete_user_badges(user.id)
        self.db.commit()
