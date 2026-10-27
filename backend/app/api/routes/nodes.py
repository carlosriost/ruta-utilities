"""Consulta de un punto y marcado de sus temas."""

from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.node import (
    NodeDetailResponse,
    RequirementUpdateRequest,
    RequirementUpdateResponse,
)
from app.services.course_service import CourseService
from app.services.requirement_service import RequirementService

router = APIRouter(prefix="/nodes", tags=["Puntos del recorrido"])

LOCKED_RESPONSE = {403: {"description": "El punto todavia esta bloqueado."}}
NOT_FOUND_RESPONSE = {404: {"description": "El punto no existe."}}


@router.get(
    "/{node_id}",
    response_model=NodeDetailResponse,
    summary="Detalle de un punto y sus temas",
    description=(
        "Devuelve el contenido almacenado en PostgreSQL: objetivo, contexto y "
        "la lista de temas (requisitos VPO) con su marca actual. `meets` es "
        "`true` si la planta lo cumple; por defecto es `false` (no cumple)."
    ),
    responses={**LOCKED_RESPONSE, **NOT_FOUND_RESPONSE},
)
def get_node(node_id: int, user: CurrentUser, db: DbSession) -> NodeDetailResponse:
    return CourseService(db).get_node_detail(user, node_id)


@router.put(
    "/{node_id}/requirements/{code}",
    response_model=RequirementUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Marcar un tema como cumplido o no cumplido",
    description=(
        "`meets: true` marca el tema como cumplido; `meets: false` lo vuelve a "
        "su valor por defecto (no cumple).\n\n"
        "FastAPI guarda la marca, recalcula el cumplimiento del nivel, "
        "comprueba si se abre el siguiente y evalua las insignias, todo en una "
        "sola transaccion."
    ),
    responses={
        **LOCKED_RESPONSE,
        404: {"description": "El punto o el tema no existen."},
    },
)
def set_requirement(
    node_id: int,
    code: str,
    payload: RequirementUpdateRequest,
    user: CurrentUser,
    db: DbSession,
) -> RequirementUpdateResponse:
    return RequirementService(db).set_status(user, node_id, code, payload)
