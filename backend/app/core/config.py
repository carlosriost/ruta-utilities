"""Configuracion de la aplicacion.

Todos los valores se leen de variables de entorno (o de ``backend/.env``).
Nunca se escriben credenciales directamente en el codigo.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Ajustes de la aplicacion."""

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Base de datos ----------------------------------------------------
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/ruta_utilities"
    )
    test_database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/ruta_utilities_test"
    )

    # --- Aplicacion -------------------------------------------------------
    app_env: str = "development"
    app_name: str = "Ruta Utilities API"
    api_prefix: str = "/api"
    frontend_url: str = "http://localhost:5174"

    # --- Identidad --------------------------------------------------------
    # "demo"  -> DemoIdentityProvider (esta version)
    # "entra" -> EntraIdentityProvider (integracion futura con Microsoft Entra ID)
    auth_provider: str = "demo"
    demo_token_secret: str = "ruta-utilities-demo-secret"

    # --- Usuario demo -----------------------------------------------------
    demo_user_name: str = "Carlos Rios"
    demo_user_area: str = "Utilities"
    demo_user_plant: str = "Cerveceria Itagui"
    demo_user_role: str = "Operario"
    demo_user_email: str | None = None

    # --- Reglas de negocio ------------------------------------------------
    default_unlock_threshold: int = 90

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in {"development", "dev", "local"}

    @property
    def cors_origins(self) -> list[str]:
        """Origenes permitidos durante desarrollo (nunca se usa '*')."""
        origins = {self.frontend_url.rstrip("/")}
        if self.is_development:
            origins.update(
                {
                    "http://localhost:5174",
                    "http://127.0.0.1:5174",
                }
            )
        return sorted(origins)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
