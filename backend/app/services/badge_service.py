"""Reglas de insignias. Se evaluan siempre en el backend."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.models.enums import BadgeRule
from app.models.user import User
from app.repositories.badge_repository import BadgeRepository
from app.schemas.badge import BadgeCollectionResponse, BadgeResponse
from app.services.progress_service import CourseState


class BadgeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.badges = BadgeRepository(db)

    # -- Evaluacion --------------------------------------------------------
    def evaluate(self, user: User, state: CourseState) -> list[Badge]:
        """Concede las insignias que el usuario acaba de merecer.

        Devuelve unicamente las nuevas, para que el frontend pueda celebrarlas.
        """
        earned = self.badges.earned_map(user.id)
        newly_awarded: list[Badge] = []

        for badge in self.badges.list_badges():
            if badge.id in earned:
                continue
            if self._is_satisfied(badge, state):
                self.badges.award(user.id, badge)
                newly_awarded.append(badge)

        if newly_awarded:
            self.db.flush()
        return newly_awarded

    @staticmethod
    def _is_satisfied(badge: Badge, state: CourseState) -> bool:
        if badge.rule_type == BadgeRule.FIRST_REQUIREMENT_MET.value:
            return any(p.met > 0 for p in state.phases)

        if badge.rule_type == BadgeRule.PHASE_COMPLIANT.value:
            phase_state = next(
                (p for p in state.phases if p.phase.slug == badge.rule_ref), None
            )
            return bool(phase_state and phase_state.compliant)

        if badge.rule_type == BadgeRule.COURSE_COMPLIANT.value:
            return state.course_compliant

        return False

    # -- Lectura -----------------------------------------------------------
    @staticmethod
    def to_schema(badge: Badge, awarded_at=None) -> BadgeResponse:
        return BadgeResponse(
            id=badge.id,
            slug=badge.slug,
            name=badge.name,
            description=badge.description,
            icon=badge.icon,
            theme=badge.theme,
            earned=awarded_at is not None,
            awarded_at=awarded_at,
        )

    def collection_for(self, user: User) -> BadgeCollectionResponse:
        earned = self.badges.earned_map(user.id)
        items = [
            self.to_schema(badge, earned[badge.id].awarded_at if badge.id in earned else None)
            for badge in self.badges.list_badges()
        ]
        return BadgeCollectionResponse(
            badges=items,
            earned=sum(1 for b in items if b.earned),
            total=len(items),
        )
