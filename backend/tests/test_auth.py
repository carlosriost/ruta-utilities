"""Autenticacion de la demo."""

from fastapi.testclient import TestClient


def test_demo_login_devuelve_al_usuario_de_postgres(client: TestClient) -> None:
    response = client.post("/api/auth/demo-login")

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["auth_provider"] == "demo"
    assert body["user"]["name"]
    assert body["user"]["area"] == "Utilities"
    assert body["user"]["role"] == "Operario"


def test_endpoints_privados_exigen_token(client: TestClient) -> None:
    assert client.get("/api/users/me").status_code == 401
    assert client.get("/api/course").status_code == 401
    assert client.get("/api/progress/me").status_code == 401


def test_token_invalido_es_rechazado(client: TestClient) -> None:
    client.headers.update({"Authorization": "Bearer demo.1.firmafalsa"})
    assert client.get("/api/users/me").status_code == 401


def test_users_me_devuelve_el_perfil(auth_client: TestClient) -> None:
    response = auth_client.get("/api/users/me")

    assert response.status_code == 200
    assert response.json()["plant"]
