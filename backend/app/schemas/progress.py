"""Schemas de avance. Todos los porcentajes los calcula el backend."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.badge import BadgeResponse


class NodeStateResponse(BaseModel):
    """Punto del mapa con el estado de sus temas."""

    id: int
    phase_id: int
    slug: str
    title: str
    description: str
    icon: str
    order_index: int
    total_requirements: int
    met: int = 0
    failed: int = 0
    status: str = Field(examples=["LOCKED", "COMPLIANT", "HAS_GAPS"])
    locked_reason: str | None = None


class PhaseStateResponse(BaseModel):
    """Estado calculado de un nivel."""

    phase_id: int
    unlocked: bool
    #: Cumplimiento: temas cumplidos sobre el total del nivel.
    percent: int = Field(ge=0, le=100)
    met: int
    failed: int
    total_requirements: int
    #: Puntos donde todos los temas cumplen.
    compliant_nodes: int
    total_nodes: int
    #: El nivel alcanza su umbral de cumplimiento.
    compliant: bool
    unlock_threshold: int
    locked_reason: str | None = None


class ProgressSummary(BaseModel):
    """Resumen global mostrado en el mapa y en la pagina de avance."""

    general_progress: int = Field(ge=0, le=100)
    met_requirements: int
    failed_requirements: int
    total_requirements: int
    compliant_nodes: int
    total_nodes: int
    badges_earned: int
    badges_total: int
    current_phase_id: int | None = None
    current_phase_name: str | None = None
    next_node_id: int | None = None
    next_node_title: str | None = None
    unlocked_phases: int
    total_phases: int
    started_at: datetime | None = None
    course_compliant: bool = False


class ProgressResponse(BaseModel):
    """Avance completo del usuario."""

    summary: ProgressSummary
    phases: list[PhaseStateResponse]
    nodes: list[NodeStateResponse]


class StateChange(BaseModel):
    """Cambios producidos al marcar un tema.

    Se devuelve en cada mutacion para que React actualice el mapa sin recargar.
    """

    node_status: str
    node_met: int = 0
    node_failed: int = 0
    node_total: int = 0
    phase_progress: int = Field(ge=0, le=100)
    general_progress: int = Field(ge=0, le=100)
    new_phase_unlocked: bool = False
    unlocked_phase_id: int | None = None
    unlocked_phase_name: str | None = None
    previous_phase_name: str | None = None
    new_badges: list[BadgeResponse] = []
    course_compliant: bool = False
    next_node_id: int | None = None
