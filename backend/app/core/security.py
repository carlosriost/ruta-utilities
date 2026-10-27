"""Identidad del usuario.

Este modulo aisla COMO se identifica a quien llama a la API del resto de la
aplicacion. Hoy existe un proveedor de demostracion; manana se anade uno que
valide un token de Microsoft Entra ID sin tocar servicios ni routers.

    IdentityProvider (protocolo)
      |- DemoIdentityProvider    -> token opaco firmado, resuelve al usuario demo
      |- EntraIdentityProvider   -> pendiente: valida el JWT de Entra ID (oid/upn)

Los servicios solo reciben un ``User`` ya resuelto.
"""

from __future__ import annotations

import hmac
from hashlib import sha256
from typing import Protocol

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import UnauthorizedError
from app.models.user import User
from app.repositories.user_repository import UserRepository

TOKEN_PREFIX = "demo"


def _signature(payload: str) -> str:
    return hmac.new(
        settings.demo_token_secret.encode("utf-8"),
        payload.encode("utf-8"),
        sha256,
    ).hexdigest()[:32]


class IdentityProvider(Protocol):
    """Contrato que debe cumplir cualquier proveedor de identidad."""

    name: str

    def issue_token(self, user: User) -> str:
        """Emite un token de sesion para el usuario indicado."""

    def resolve_user(self, db: Session, token: str | None) -> User:
        """Resuelve el usuario a partir del token recibido."""


class DemoIdentityProvider:
    """Proveedor de demostracion.

    El token es opaco y va firmado con HMAC para que no pueda falsificarse
    trivialmente, pero no pretende sustituir a un JWT corporativo.
    Formato: ``demo.<user_id>.<firma>``
    """

    name = "demo"

    def issue_token(self, user: User) -> str:
        payload = f"{TOKEN_PREFIX}.{user.id}"
        return f"{payload}.{_signature(payload)}"

    def resolve_user(self, db: Session, token: str | None) -> User:
        if not token:
            raise UnauthorizedError(
                "Falta el token de sesion. Inicia sesion en /api/auth/demo-login."
            )
        parts = token.split(".")
        if len(parts) != 3 or parts[0] != TOKEN_PREFIX:
            raise UnauthorizedError("Token de sesion invalido.")
        payload = f"{parts[0]}.{parts[1]}"
        if not hmac.compare_digest(parts[2], _signature(payload)):
            raise UnauthorizedError("Token de sesion invalido.")
        try:
            user_id = int(parts[1])
        except ValueError as exc:
            raise UnauthorizedError("Token de sesion invalido.") from exc

        user = UserRepository(db).get(user_id)
        if user is None:
            raise UnauthorizedError("El usuario del token ya no existe.")
        return user


class EntraIdentityProvider:
    """Integracion futura con Microsoft Entra ID.

    Pasos previstos cuando se active (ver README, seccion "Microsoft Entra ID"):

    1. Registrar la aplicacion en Entra ID y obtener ``tenant_id`` y ``client_id``.
    2. Descargar las claves publicas de
       ``https://login.microsoftonline.com/<tenant>/discovery/v2.0/keys``.
    3. Validar aqui la firma, el ``aud`` y el ``iss`` del access token.
    4. Buscar o crear el ``User`` usando el claim ``oid`` en ``User.external_id``.

    Ningun otro modulo necesita cambiar: los servicios ya reciben un ``User``.
    """

    name = "entra"

    def issue_token(self, user: User) -> str:  # pragma: no cover - no implementado
        raise NotImplementedError(
            "Con Microsoft Entra ID el token lo emite Microsoft, no esta API."
        )

    def resolve_user(
        self, db: Session, token: str | None
    ) -> User:  # pragma: no cover - no implementado
        raise NotImplementedError(
            "Pendiente: validar el JWT de Microsoft Entra ID y mapear el claim oid."
        )


def get_identity_provider() -> IdentityProvider:
    """Devuelve el proveedor configurado en ``AUTH_PROVIDER``."""
    if settings.auth_provider.lower() == "entra":
        return EntraIdentityProvider()
    return DemoIdentityProvider()
