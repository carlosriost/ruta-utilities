"""Schemas del catalogo del recorrido (definicion, sin avance)."""

from pydantic import BaseModel, ConfigDict

from app.schemas.progress import NodeStateResponse, PhaseStateResponse, ProgressSummary


class PhaseResponse(BaseModel):
    """Definicion de un nivel."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str
    order_index: int
    unlock_threshold: int
    theme: str
    icon: str


class PhaseDetailResponse(PhaseResponse):
    """Nivel con sus puntos y el estado calculado."""

    state: PhaseStateResponse
    nodes: list[NodeStateResponse]


class CourseResponse(BaseModel):
    """Mapa completo: niveles, puntos y avance."""

    phases: list[PhaseDetailResponse]
    summary: ProgressSummary
