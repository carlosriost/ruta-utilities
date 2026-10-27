"""Insignias del usuario."""

from fastapi import APIRouter

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.badge import BadgeCollectionResponse
from app.services.badge_service import BadgeService
from app.services.course_service import CourseService

router = APIRouter(prefix="/badges", tags=["Insignias"])


@router.get(
    "/me",
    response_model=BadgeCollectionResponse,
    summary="Insignias del operario",
    description=(
        "Devuelve el catalogo completo indicando cuales ya obtuvo el usuario. "
        "Las reglas se reevaluan en cada consulta, nunca en el frontend."
    ),
)
def read_my_badges(user: CurrentUser, db: DbSession) -> BadgeCollectionResponse:
    state = CourseService(db).state_for(user)
    service = BadgeService(db)
    service.evaluate(user, state)
    db.commit()
    return service.collection_for(user)
