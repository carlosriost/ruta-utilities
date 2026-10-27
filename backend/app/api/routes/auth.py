"""Autenticacion de demostracion."""

from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.user import DemoLoginResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post(
    "/demo-login",
    response_model=DemoLoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesion en la demo",
    description=(
        "Busca en PostgreSQL al unico usuario de la demostracion (Carlos Rios) "
        "y devuelve un token de sesion. No pide correo ni contrasena.\n\n"
        "Cuando se integre Microsoft Entra ID este endpoint se sustituye por el "
        "flujo OAuth corporativo sin tocar el resto de la API."
    ),
    responses={404: {"description": "No existe el usuario demo (falta el seed)."}},
)
def demo_login(db: DbSession) -> DemoLoginResponse:
    return AuthService(db).demo_login()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Usuario de la sesion actual",
    responses={401: {"description": "Token ausente o invalido."}},
)
def read_session_user(user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(user)
