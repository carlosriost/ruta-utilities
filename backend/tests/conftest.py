"""Configuracion de la suite de tests.

Los tests SIEMPRE se ejecutan contra ``TEST_DATABASE_URL``, una base de datos
distinta de la principal. Si ambas coinciden, la suite se detiene: nunca se
ejecuta nada destructivo contra los datos reales.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import CourseNode  # noqa: F401  registra todos los modelos
from app.seed.runner import seed

# Tablas que guardan avance del usuario: se limpian entre tests.
PROGRESS_TABLES = (
    "requirement_marks",
    "user_badges",
    "user_phase_progress",
)


def pytest_configure() -> None:
    if settings.test_database_url == settings.database_url:
        pytest.exit(
            "TEST_DATABASE_URL no puede ser igual a DATABASE_URL. "
            "Configura una base de datos de pruebas separada en backend/.env.",
            returncode=1,
        )


@pytest.fixture(scope="session")
def engine():
    test_engine = create_engine(settings.test_database_url, future=True)
    # Se recrea el esquema entero, no solo las tablas que conocen los modelos:
    # asi no sobreviven tablas ni columnas de una version anterior.
    with test_engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def seeded(engine, session_factory) -> None:
    """Carga el contenido una sola vez para toda la suite."""
    db = session_factory()
    try:
        seed(db)
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_progress(engine) -> Generator[None, None, None]:
    """Cada test empieza sin marcas, pero con el catalogo intacto."""
    with engine.begin() as connection:
        for table in PROGRESS_TABLES:
            connection.execute(text(f"DELETE FROM {table}"))
    yield


@pytest.fixture
def db(session_factory) -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(session_factory) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client: TestClient) -> TestClient:
    """Cliente ya autenticado como el usuario demo."""
    response = client.post("/api/auth/demo-login")
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
