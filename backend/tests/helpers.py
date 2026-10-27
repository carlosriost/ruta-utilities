"""Utilidades compartidas por los tests.

Los tests localizan los puntos por posicion, no por slug, para que el
contenido pueda cambiar sin romper la suite.
"""

from fastapi.testclient import TestClient

PHASE_0 = "nivel-0"
PHASE_1 = "nivel-1"


def get_course(client: TestClient) -> dict:
    response = client.get("/api/course")
    assert response.status_code == 200, response.text
    return response.json()


def all_nodes(course: dict) -> list[dict]:
    return [node for phase in course["phases"] for node in phase["nodes"]]


def phase_by_slug(course: dict, slug: str) -> dict:
    phase = next((p for p in course["phases"] if p["slug"] == slug), None)
    assert phase is not None, f"No existe el nivel {slug}"
    return phase


def node_at(course: dict, index: int, phase_slug: str = PHASE_0) -> dict:
    nodes = phase_by_slug(course, phase_slug)["nodes"]
    assert index < len(nodes), f"El nivel {phase_slug} no tiene {index + 1} puntos"
    return nodes[index]


def node_detail(client: TestClient, node_id: int) -> dict:
    response = client.get(f"/api/nodes/{node_id}")
    assert response.status_code == 200, response.text
    return response.json()


def codes_of(client: TestClient, node_id: int) -> list[str]:
    detail = node_detail(client, node_id)
    return [item["code"] for item in detail["content"]["requirements"]]


def mark(client: TestClient, node_id: int, code: str, meets: bool) -> dict:
    response = client.put(
        f"/api/nodes/{node_id}/requirements/{code}", json={"meets": meets}
    )
    assert response.status_code == 200, response.text
    return response.json()


def mark_node(client: TestClient, node_id: int, meets: bool = True) -> dict:
    """Marca todos los temas de un punto y devuelve el ultimo estado."""
    ultimo: dict | None = None
    for code in codes_of(client, node_id):
        ultimo = mark(client, node_id, code, meets)["state"]
    assert ultimo is not None, f"El punto {node_id} no tiene temas"
    return ultimo


def mark_phase(
    client: TestClient, phase_slug: str, meets: bool = True, limit: int | None = None
) -> dict | None:
    """Marca los temas de un nivel; ``limit`` corta tras N temas."""
    ultimo: dict | None = None
    marcados = 0
    for node in phase_by_slug(get_course(client), phase_slug)["nodes"]:
        for code in codes_of(client, node["id"]):
            if limit is not None and marcados >= limit:
                return ultimo
            ultimo = mark(client, node["id"], code, meets)["state"]
            marcados += 1
    return ultimo


def phase_codes(client: TestClient, phase_slug: str) -> list[tuple[int, str]]:
    """Todos los temas del nivel como pares (id del punto, codigo)."""
    pares = []
    for node in phase_by_slug(get_course(client), phase_slug)["nodes"]:
        pares += [(node["id"], code) for code in codes_of(client, node["id"])]
    return pares
