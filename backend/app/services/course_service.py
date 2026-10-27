"""Lectura del curso ya combinada con el progreso del usuario."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import NodeLockedError, NotFoundError
from app.models.enums import NodeStatus
from app.models.user import User
from app.repositories.course_repository import CourseRepository
from app.repositories.progress_repository import ProgressRepository
from app.schemas.course import CourseResponse, PhaseDetailResponse
from app.schemas.node import (
    NodeContentResponse,
    NodeDetailResponse,
    RequirementResponse,
)
from app.services.progress_service import CourseState, ProgressService


class CourseService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.courses = CourseRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.progress = ProgressService(db)

    # -- Estado sincronizado ----------------------------------------------
    def state_for(self, user: User) -> CourseState:
        """Calcula el estado y persiste la foto de cada fase."""
        state = self.progress.compute_state(user)
        self.progress.sync_phase_progress(user, state)
        self.db.commit()
        return state

    # -- Mapa completo -----------------------------------------------------
    def get_course(self, user: User) -> CourseResponse:
        state = self.state_for(user)
        return CourseResponse(
            phases=[self._phase_detail(p) for p in state.phases],
            summary=self.progress.summary(user, state),
        )

    def list_phases(self, user: User) -> list[PhaseDetailResponse]:
        state = self.state_for(user)
        return [self._phase_detail(p) for p in state.phases]

    def get_phase(self, user: User, phase_id: int) -> PhaseDetailResponse:
        state = self.state_for(user)
        phase_state = state.phase_state(phase_id)
        if phase_state is None:
            raise NotFoundError(f"La fase {phase_id} no existe.")
        return self._phase_detail(phase_state)

    def _phase_detail(self, phase_state) -> PhaseDetailResponse:
        phase = phase_state.phase
        return PhaseDetailResponse(
            id=phase.id,
            slug=phase.slug,
            name=phase.name,
            description=phase.description,
            order_index=phase.order_index,
            unlock_threshold=phase.unlock_threshold,
            theme=phase.theme,
            icon=phase.icon,
            state=ProgressService.phase_schema(phase_state),
            nodes=[ProgressService.node_schema(n) for n in phase_state.nodes],
        )

    # -- Detalle de un punto ------------------------------------------------
    def get_node_detail(self, user: User, node_id: int) -> NodeDetailResponse:
        node = self.courses.get_node(node_id)
        if node is None:
            raise NotFoundError(f"El punto {node_id} no existe.")

        state = self.state_for(user)
        node_state = state.node_states[node_id]
        if node_state.status is NodeStatus.LOCKED:
            raise NodeLockedError(
                node_state.locked_reason or "Este punto todavia esta bloqueado."
            )

        activity = self.courses.get_activity_for_node(node_id)
        met_codes = self.progress_repo.met_codes(user.id)
        payload = (activity.payload or {}) if activity else {}

        return NodeDetailResponse(
            node=ProgressService.node_schema(node_state),
            phase_id=node.phase_id,
            phase_name=node.phase.name,
            phase_theme=node.phase.theme,
            content=NodeContentResponse(
                objective=activity.objective if activity else "",
                body=activity.body if activity else "",
                vpo_block=payload.get("vpo_block"),
                requirements=[
                    RequirementResponse(
                        code=item["code"],
                        title=item["title"],
                        detail=item["detail"],
                        meets=item["code"] in met_codes,
                    )
                    for item in payload.get("requirements", [])
                ],
            ),
        )
