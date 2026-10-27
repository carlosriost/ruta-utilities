"""Dependencias compartidas por los routers."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import get_identity_provider
from app.db.session import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="Sesion demo",
    description=(
        "Token devuelto por POST /api/auth/demo-login. "
        "En Swagger usa el boton Authorize y pega el access_token."
    ),
)

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ] = None,
) -> User:
    """Resuelve al usuario autenticado mediante el proveedor de identidad.

    Cambiar AUTH_PROVIDER=entra en el futuro basta para que aqui se valide un
    token de Microsoft Entra ID: los routers y servicios no cambian.
    """
    provider = get_identity_provider()
    token = credentials.credentials if credentials else None
    return provider.resolve_user(db, token)


CurrentUser = Annotated[User, Depends(get_current_user)]
