"""Autenticacion.

El servicio no sabe si la identidad viene de la demo o de Microsoft Entra ID:
delega en el ``IdentityProvider`` configurado.
"""

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.core.security import get_identity_provider
from app.repositories.user_repository import UserRepository
from app.schemas.user import DemoLoginResponse, UserResponse


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.provider = get_identity_provider()

    def demo_login(self) -> DemoLoginResponse:
        """Resuelve al unico usuario de la demo y emite su token de sesion."""
        user = self.users.get_demo_user()
        if user is None:
            raise NotFoundError(
                "No hay usuario demo en la base de datos. Ejecuta: python -m app.seed"
            )
        token = self.provider.issue_token(user)
        return DemoLoginResponse(
            access_token=token,
            auth_provider=self.provider.name,
            user=UserResponse.model_validate(user),
        )
