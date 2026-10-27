"""Motor de avance: el corazon de las reglas.

TODA la logica vive aqui (no en React):

* cuantos temas de cada punto cumplen (el resto, por defecto, no cumple)
* el cumplimiento de cada nivel y el general
* que nivel esta abierto, segun el umbral del nivel anterior
* cual es el siguiente punto que todavia tiene brechas

El estado de un punto y el porcentaje de un nivel NO se persisten: se derivan
en cada peticion a partir de las marcas, de modo que no puede existir un
estado guardado incoherente con las reglas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.course import CourseNode, Phase
from app.models.enums import NodeStatus
from app.models.progress import RequirementMark
from app.models.user import User
from app.repositories.badge_repository import BadgeRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.progress_repository import ProgressRepository, utcnow
from app.schemas.progress import (
    NodeStateResponse,
    PhaseStateResponse,
    ProgressResponse,
    ProgressSummary,
)

LOCKED_BY_PHASE = "Completa el nivel anterior para desbloquear esta zona."


def _percent(part: int, total: int) -> int:
    if total <= 0:
        return 0
    return max(0, min(100, round(part * 100 / total)))


@dataclass
class NodeState:
    """Estado calculado de un punto del mapa."""

    node: CourseNode
    status: NodeStatus
    total: int
    met: int
    locked_reason: str | None = None

    @property
    def failed(self) -> int:
        """Temas que no cumplen: todo lo que no esta marcado explicitamente."""
        return self.total - self.met

    @property
    def is_compliant(self) -> bool:
        return self.total > 0 and self.met == self.total


@dataclass
class PhaseState:
    """Estado calculado de un nivel."""

    phase: Phase
    unlocked: bool
    total: int
    met: int
    compliant_nodes: int
    nodes: list[NodeState] = field(default_factory=list)

    @property
    def failed(self) -> int:
        return self.total - self.met

    @property
    def percent(self) -> int:
        """Cumplimiento: temas cumplidos sobre el total del nivel."""
        return _percent(self.met, self.total)

    @property
    def compliant(self) -> bool:
        """El nivel alcanza el umbral que exige VPO para pasar al siguiente."""
        return self.percent >= self.phase.unlock_threshold


@dataclass
class CourseState:
    """Fotografia completa del recorrido."""

    phases: list[PhaseState]
    node_states: dict[int, NodeState]
    started_at: datetime | None
    next_node: CourseNode | None
    current_phase: Phase | None

    @property
    def course_compliant(self) -> bool:
        return bool(self.phases) and all(p.compliant for p in self.phases)

    def phase_state(self, phase_id: int) -> PhaseState | None:
        return next((p for p in self.phases if p.phase.id == phase_id), None)

    def phase_percent(self, phase_id: int) -> int:
        state = self.phase_state(phase_id)
        return state.percent if state else 0


class ProgressService:
    """Calcula el estado del recorrido y lo sincroniza con PostgreSQL."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.courses = CourseRepository(db)
        self.progress = ProgressRepository(db)
        self.badges = BadgeRepository(db)

    # -- Calculo -----------------------------------------------------------
    def compute_state(self, user: User) -> CourseState:
        phases = self.courses.list_phases()
        met_codes = self.progress.met_codes(user.id)

        phase_states: list[PhaseState] = []
        node_states: dict[int, NodeState] = {}
        previous: PhaseState | None = None

        for phase in phases:
            # El primer nivel siempre esta abierto; los demas dependen del
            # cumplimiento del anterior.
            unlocked = previous is None or previous.compliant
            nodes = sorted(phase.nodes, key=lambda n: n.order_index)

            states: list[NodeState] = []
            for node in nodes:
                codes = [r["code"] for r in self._requirements(node)]
                met = sum(1 for code in codes if code in met_codes)
                state = NodeState(
                    node=node,
                    status=self._node_status(unlocked, len(codes), met),
                    total=len(codes),
                    met=met,
                    locked_reason=None if unlocked else LOCKED_BY_PHASE,
                )
                states.append(state)
                node_states[node.id] = state

            phase_state = PhaseState(
                phase=phase,
                unlocked=unlocked,
                total=sum(s.total for s in states),
                met=sum(s.met for s in states),
                compliant_nodes=sum(1 for s in states if s.is_compliant),
                nodes=states,
            )
            phase_states.append(phase_state)
            previous = phase_state

        return CourseState(
            phases=phase_states,
            node_states=node_states,
            started_at=self._started_at(met_codes),
            next_node=self._next_node(phase_states),
            current_phase=self._current_phase(phase_states),
        )

    @staticmethod
    def _requirements(node: CourseNode) -> list[dict]:
        activity = node.activity
        if activity is None:
            return []
        return activity.requirements

    @staticmethod
    def _node_status(unlocked: bool, total: int, met: int) -> NodeStatus:
        if not unlocked:
            return NodeStatus.LOCKED
        if total > 0 and met < total:
            return NodeStatus.HAS_GAPS
        return NodeStatus.COMPLIANT

    @staticmethod
    def _started_at(met_codes: dict[str, RequirementMark]) -> datetime | None:
        stamps = [mark.created_at for mark in met_codes.values() if mark.created_at]
        return min(stamps) if stamps else None

    @staticmethod
    def _next_node(phase_states: list[PhaseState]) -> CourseNode | None:
        """Primer punto abierto que todavia tiene brechas."""
        for phase_state in phase_states:
            if not phase_state.unlocked:
                continue
            for node_state in phase_state.nodes:
                if not node_state.is_compliant:
                    return node_state.node
        return None

    @staticmethod
    def _current_phase(phase_states: list[PhaseState]) -> Phase | None:
        current: Phase | None = None
        for phase_state in phase_states:
            if not phase_state.unlocked:
                break
            current = phase_state.phase
            if phase_state.compliant_nodes < len(phase_state.nodes):
                break
        return current

    # -- Sincronizacion con user_phase_progress ----------------------------
    def sync_phase_progress(self, user: User, state: CourseState) -> list[Phase]:
        """Guarda el estado de cada nivel y devuelve los recien abiertos.

        El primer nivel nunca se reporta como recien abierto: siempre lo esta
        y no debe disparar la animacion de nueva zona.
        """
        newly_unlocked: list[Phase] = []
        now = utcnow()

        for phase_state in state.phases:
            record = self.progress.get_or_create_phase_progress(
                user.id, phase_state.phase.id
            )
            was_unlocked = record.unlocked
            record.percent = phase_state.percent

            if phase_state.unlocked and not was_unlocked:
                record.unlocked = True
                record.unlocked_at = record.unlocked_at or now
                if phase_state.phase.order_index > 0:
                    newly_unlocked.append(phase_state.phase)
            elif not phase_state.unlocked:
                record.unlocked = False

            if phase_state.compliant and record.completed_at is None:
                record.completed_at = now
            elif not phase_state.compliant:
                record.completed_at = None

        self.db.flush()
        return newly_unlocked

    # -- Serializacion -----------------------------------------------------
    @staticmethod
    def node_schema(state: NodeState) -> NodeStateResponse:
        node = state.node
        return NodeStateResponse(
            id=node.id,
            phase_id=node.phase_id,
            slug=node.slug,
            title=node.title,
            description=node.description,
            icon=node.icon,
            order_index=node.order_index,
            total_requirements=state.total,
            met=state.met,
            failed=state.failed,
            status=state.status.value,
            locked_reason=state.locked_reason,
        )

    @staticmethod
    def phase_schema(state: PhaseState) -> PhaseStateResponse:
        return PhaseStateResponse(
            phase_id=state.phase.id,
            unlocked=state.unlocked,
            percent=state.percent,
            met=state.met,
            failed=state.failed,
            total_requirements=state.total,
            compliant_nodes=state.compliant_nodes,
            total_nodes=len(state.nodes),
            compliant=state.compliant,
            unlock_threshold=state.phase.unlock_threshold,
            locked_reason=state.nodes[0].locked_reason if state.nodes else None,
        )

    def summary(self, user: User, state: CourseState) -> ProgressSummary:
        total = sum(p.total for p in state.phases)
        met = sum(p.met for p in state.phases)
        return ProgressSummary(
            general_progress=_percent(met, total),
            met_requirements=met,
            failed_requirements=total - met,
            total_requirements=total,
            compliant_nodes=sum(p.compliant_nodes for p in state.phases),
            total_nodes=sum(len(p.nodes) for p in state.phases),
            badges_earned=len(self.badges.list_user_badges(user.id)),
            badges_total=len(self.badges.list_badges()),
            current_phase_id=state.current_phase.id if state.current_phase else None,
            current_phase_name=(
                state.current_phase.name if state.current_phase else None
            ),
            next_node_id=state.next_node.id if state.next_node else None,
            next_node_title=state.next_node.title if state.next_node else None,
            unlocked_phases=sum(1 for p in state.phases if p.unlocked),
            total_phases=len(state.phases),
            started_at=state.started_at,
            course_compliant=state.course_compliant,
        )

    def progress_response(self, user: User, state: CourseState) -> ProgressResponse:
        return ProgressResponse(
            summary=self.summary(user, state),
            phases=[self.phase_schema(p) for p in state.phases],
            nodes=[self.node_schema(n) for p in state.phases for n in p.nodes],
        )
