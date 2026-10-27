"""Schemas del detalle de un punto y del marcado de sus temas."""

from pydantic import BaseModel

from app.schemas.progress import NodeStateResponse, StateChange


class RequirementResponse(BaseModel):
    """Un tema con su marca actual. Sin marcar explicitamente es "no cumple"."""

    code: str
    title: str
    detail: str
    meets: bool = False


class NodeContentResponse(BaseModel):
    """Contexto del punto y sus temas."""

    objective: str
    body: str
    #: Nombre oficial del bloque VPO, en ingles, para trazabilidad.
    vpo_block: str | None = None
    requirements: list[RequirementResponse]


class NodeDetailResponse(BaseModel):
    node: NodeStateResponse
    phase_id: int
    phase_name: str
    phase_theme: str
    content: NodeContentResponse


class RequirementUpdateRequest(BaseModel):
    """True marca el tema como cumplido; False lo vuelve al valor por defecto."""

    meets: bool


class RequirementUpdateResponse(BaseModel):
    code: str
    meets: bool
    state: StateChange
