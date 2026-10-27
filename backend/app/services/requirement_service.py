"""Marcado de temas: la unica mutacion del recorrido.

Marcar un tema guarda (o borra) la marca, recalcula el cumplimiento, comprueba
si se abre un nivel nuevo y evalua las insignias. Todo ocurre en UNA
transaccion: o se aplica completo, o no se aplica nada.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import NodeLockedError, NotFoundError
from app.models.course import CourseNode
from app.models.enums import NodeStatus
from app.models.user import User
from app.repositories.course_repository import CourseRepository
from app.repositories.progress_repository import ProgressRepository, utcnow
from app.schemas.node import RequirementUpdateRequest, RequirementUpdateResponse
from app.schemas.progress import StateChange
from app.services.badge_service import BadgeService
from app.services.progress_service import ProgressService


class RequirementService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.courses = CourseRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.progress = ProgressService(db)
        self.badges = BadgeService(db)

    def set_status(
        self, user: User, node_id: int, code: str, payload: RequirementUpdateRequest
    ) -> RequirementUpdateResponse:
        node = self._open_node(user, node_id)

        codes = {r["code"] for r in (node.activity.requirements if node.activity else [])}
        if code not in codes:
            raise NotFoundError(f"El tema {code} no pertenece a este punto.")

        if payload.meets:
            self.progress_repo.mark_as_met(user.id, node.id, code)
        else:
            self.progress_repo.unmark(user.id, code)

        change = self._build_state_change(user, node)
        self.db.commit()
        return RequirementUpdateResponse(code=code, meets=payload.meets, state=change)

    # -- Utilidades --------------------------------------------------------
    def _open_node(self, user: User, node_id: int) -> CourseNode:
        node = self.courses.get_node(node_id)
        if node is None:
            raise NotFoundError(f"El punto {node_id} no existe.")

        state = self.progress.compute_state(user)
        node_state = state.node_states[node_id]
        if node_state.status is NodeStatus.LOCKED:
            raise NodeLockedError(
                node_state.locked_reason or "Este punto todavia esta bloqueado."
            )
        return node

    def _build_state_change(self, user: User, node: CourseNode) -> StateChange:
        """Recalcula todo y arma la respuesta que consumira React."""
        state = self.progress.compute_state(user)
        newly_unlocked = self.progress.sync_phase_progress(user, state)
        new_badges = self.badges.evaluate(user, state)

        unlocked_phase = newly_unlocked[0] if newly_unlocked else None
        previous_name = None
        if unlocked_phase is not None:
            previous_name = next(
                (
                    p.phase.name
                    for p in state.phases
                    if p.phase.order_index == unlocked_phase.order_index - 1
                ),
                None,
            )

        node_state = state.node_states[node.id]
        return StateChange(
            node_status=node_state.status.value,
            node_met=node_state.met,
            node_failed=node_state.failed,
            node_total=node_state.total,
            phase_progress=state.phase_percent(node.phase_id),
            general_progress=self.progress.summary(user, state).general_progress,
            new_phase_unlocked=unlocked_phase is not None,
            unlocked_phase_id=unlocked_phase.id if unlocked_phase else None,
            unlocked_phase_name=unlocked_phase.name if unlocked_phase else None,
            previous_phase_name=previous_name,
            new_badges=[BadgeService.to_schema(b, utcnow()) for b in new_badges],
            course_compliant=state.course_compliant,
            next_node_id=state.next_node.id if state.next_node else None,
        )
