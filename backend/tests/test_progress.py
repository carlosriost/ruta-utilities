"""Marcado de temas, estado de los puntos y persistencia en PostgreSQL.

El valor por defecto de un tema es "no cumple": solo se persiste la
excepcion (los temas marcados como cumplidos).
"""

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.progress import RequirementMark
from tests.helpers import (
    all_nodes,
    codes_of,
    get_course,
    mark,
    mark_node,
    node_at,
    node_detail,
)


def test_estado_inicial_todo_en_no_cumple(auth_client: TestClient) -> None:
    course = get_course(auth_client)
    resumen = course["summary"]

    assert resumen["general_progress"] == 0
    assert resumen["met_requirements"] == 0
    assert resumen["failed_requirements"] == 185
    assert resumen["total_requirements"] == 185
    assert resumen["total_nodes"] == 60
    # Sin marcar nada, todos los puntos abiertos ya tienen brechas (todo
    # cuenta como "no cumple" desde el primer momento).
    assert all(
        node["status"] == "HAS_GAPS"
        for node in all_nodes(course)
        if node["status"] != "LOCKED"
    )
    # Solo el primer nivel esta abierto.
    assert course["phases"][0]["state"]["unlocked"] is True
    assert course["phases"][1]["state"]["unlocked"] is False


def test_todos_los_puntos_del_nivel_abierto_son_accesibles(
    auth_client: TestClient,
) -> None:
    """La lista se puede recorrer en cualquier orden, no hay secuencia forzada."""
    course = get_course(auth_client)

    for node in course["phases"][0]["nodes"]:
        assert node["status"] == "HAS_GAPS"
        assert auth_client.get(f"/api/nodes/{node['id']}").status_code == 200


def test_un_tema_sin_tocar_ya_aparece_como_no_cumple(auth_client: TestClient) -> None:
    node = node_at(get_course(auth_client), 0)

    detalle = node_detail(auth_client, node["id"])

    assert all(item["meets"] is False for item in detalle["content"]["requirements"])


def test_marcar_un_tema_persiste_en_postgres(
    auth_client: TestClient, db: Session
) -> None:
    node = node_at(get_course(auth_client), 0)
    code = codes_of(auth_client, node["id"])[0]

    respuesta = mark(auth_client, node["id"], code, True)

    assert respuesta["meets"] is True
    assert respuesta["state"]["node_met"] == 1

    guardada = db.execute(
        select(RequirementMark).where(RequirementMark.code == code)
    ).scalar_one()
    assert guardada.node_id == node["id"]


def test_desmarcar_borra_la_fila_y_vuelve_al_defecto(
    auth_client: TestClient, db: Session
) -> None:
    node = node_at(get_course(auth_client), 0)
    code = codes_of(auth_client, node["id"])[0]
    mark(auth_client, node["id"], code, True)

    respuesta = mark(auth_client, node["id"], code, False)

    assert respuesta["meets"] is False
    assert respuesta["state"]["node_met"] == 0
    detalle = node_detail(auth_client, node["id"])
    assert detalle["content"]["requirements"][0]["meets"] is False
    assert (
        db.execute(
            select(RequirementMark).where(RequirementMark.code == code)
        ).scalar_one_or_none()
        is None
    )


def test_el_punto_cumple_al_marcar_todos_sus_temas(auth_client: TestClient) -> None:
    node = node_at(get_course(auth_client), 0)

    estado = mark_node(auth_client, node["id"], True)

    assert estado["node_status"] == "COMPLIANT"
    assert estado["node_met"] == node["total_requirements"]
    assert estado["node_failed"] == 0


def test_el_cumplimiento_del_nivel_es_la_proporcion_de_temas(
    auth_client: TestClient,
) -> None:
    course = get_course(auth_client)
    total = course["phases"][0]["state"]["total_requirements"]
    node = node_at(course, 0)

    estado = mark_node(auth_client, node["id"], True)

    esperado = round(node["total_requirements"] * 100 / total)
    assert estado["phase_progress"] == esperado


def test_un_punto_de_nivel_bloqueado_no_se_puede_abrir_ni_marcar(
    auth_client: TestClient,
) -> None:
    course = get_course(auth_client)
    bloqueado = course["phases"][1]["nodes"][0]

    assert bloqueado["status"] == "LOCKED"
    assert auth_client.get(f"/api/nodes/{bloqueado['id']}").status_code == 403
    respuesta = auth_client.put(
        f"/api/nodes/{bloqueado['id']}/requirements/R.1.1.2.6",
        json={"meets": True},
    )
    assert respuesta.status_code == 403


def test_un_tema_de_otro_punto_es_rechazado(auth_client: TestClient) -> None:
    course = get_course(auth_client)
    primero, segundo = node_at(course, 0), node_at(course, 1)
    ajeno = codes_of(auth_client, segundo["id"])[0]

    respuesta = auth_client.put(
        f"/api/nodes/{primero['id']}/requirements/{ajeno}", json={"meets": True}
    )

    assert respuesta.status_code == 404


def test_un_body_invalido_es_rechazado(auth_client: TestClient) -> None:
    node = node_at(get_course(auth_client), 0)
    code = codes_of(auth_client, node["id"])[0]

    respuesta = auth_client.put(
        f"/api/nodes/{node['id']}/requirements/{code}", json={"meets": "tal vez"}
    )

    assert respuesta.status_code == 422
