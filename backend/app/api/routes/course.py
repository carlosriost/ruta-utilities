"""Mapa del curso: fases y nodos con el progreso del usuario."""

from fastapi import APIRouter

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.course import CourseResponse, PhaseDetailResponse
from app.services.course_service import CourseService

router = APIRouter(tags=["Curso"])


@router.get(
    "/course",
    response_model=CourseResponse,
    summary="Mapa completo con el progreso del usuario",
    description=(
        "Devuelve todas las fases con sus nodos y el estado calculado por el "
        "backend (LOCKED / AVAILABLE / IN_PROGRESS / COMPLETED), ademas del "
        "resumen general. Es la unica llamada que necesita el mapa."
    ),
)
def get_course(user: CurrentUser, db: DbSession) -> CourseResponse:
    return CourseService(db).get_course(user)


@router.get(
    "/phases",
    response_model=list[PhaseDetailResponse],
    summary="Listado de fases con su estado",
)
def list_phases(user: CurrentUser, db: DbSession) -> list[PhaseDetailResponse]:
    return CourseService(db).list_phases(user)


@router.get(
    "/phases/{phase_id}",
    response_model=PhaseDetailResponse,
    summary="Detalle de una fase",
    responses={404: {"description": "La fase no existe."}},
)
def get_phase(phase_id: int, user: CurrentUser, db: DbSession) -> PhaseDetailResponse:
    return CourseService(db).get_phase(user, phase_id)
