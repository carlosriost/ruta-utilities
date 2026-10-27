"""Consultas sobre insignias."""

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.badge import Badge, UserBadge


class BadgeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_badges(self) -> list[Badge]:
        return list(
            self.db.execute(select(Badge).order_by(Badge.order_index)).scalars()
        )

    def get_by_slug(self, slug: str) -> Badge | None:
        return self.db.execute(
            select(Badge).where(Badge.slug == slug)
        ).scalar_one_or_none()

    def list_user_badges(self, user_id: int) -> list[UserBadge]:
        return list(
            self.db.execute(
                select(UserBadge).where(UserBadge.user_id == user_id)
            ).scalars()
        )

    def earned_map(self, user_id: int) -> dict[int, UserBadge]:
        return {ub.badge_id: ub for ub in self.list_user_badges(user_id)}

    def award(self, user_id: int, badge: Badge) -> UserBadge:
        user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
        self.db.add(user_badge)
        self.db.flush()
        return user_badge

    def delete_user_badges(self, user_id: int) -> None:
        self.db.execute(delete(UserBadge).where(UserBadge.user_id == user_id))
