"""Umbrales de cumplimiento por nivel e insignias.

Los umbrales bajan con la madurez: nivel 0 al 100%, nivel 1 al 90%, nivel 2 al
80% y nivel 3 y 4 al 70%.
"""

from fastapi.testclient import TestClient

from tests.helpers import (
    PHASE_0,
    PHASE_1,
    get_course,
    mark,
    mark_node,
    mark_phase,
    node_at,
    phase_by_slug,
    phase_codes,
)


def test_cada_nivel_declara_su_umbral(auth_client: TestClient) -> None:
    course = get_course(auth_client)

    umbrales = [phase["unlock_threshold"] for phase in course["phases"]]

    assert umbrales == [100, 90, 80, 70, 70]


def test_el_nivel_0_exige_el_100_por_ciento(auth_client: TestClient) -> None:
    temas = phase_codes(auth_client, PHASE_0)
    # Se cumplen todos menos uno (el resto ya esta en "no cumple" por defecto).
    for node_id, code in temas[:-1]:
        mark(auth_client, node_id, code, True)
    ultimo_nodo, ultimo_code = temas[-1]

    course = get_course(auth_client)
    nivel0 = phase_by_slug(course, PHASE_0)

    assert nivel0["state"]["percent"] == 98
    assert nivel0["state"]["compliant"] is False
    assert phase_by_slug(course, PHASE_1)["state"]["unlocked"] is False

    # Al cumplir tambien el ultimo tema, se abre el nivel siguiente.
    estado = mark(auth_client, ultimo_nodo, ultimo_code, True)["state"]

    assert estado["new_phase_unlocked"] is True
    assert estado["unlocked_phase_name"] == "Control del riesgo"
    assert estado["previous_phase_name"] == "Cimientos de seguridad"


def test_el_nivel_1_se_abre_con_el_90_por_ciento(auth_client: TestClient) -> None:
    mark_phase(auth_client, PHASE_0, True)

    temas = phase_codes(auth_client, PHASE_1)
    total = len(temas)
    cumplidos = 0
    pendiente: tuple[int, str] | None = None
    # Se marca todo el nivel dejando justo por debajo del 90%.
    for node_id, code in temas:
        if round((cumplidos + 1) * 100 / total) <= 89:
            mark(auth_client, node_id, code, True)
            cumplidos += 1
        else:
            pendiente = (node_id, code)  # se deja en "no cumple"

    course = get_course(auth_client)
    assert phase_by_slug(course, PHASE_1)["state"]["percent"] == 89
    assert phase_by_slug(course, PHASE_1)["state"]["compliant"] is False
    assert course["phases"][2]["state"]["unlocked"] is False

    # Un tema mas de cumplimiento cruza el umbral.
    assert pendiente is not None
    estado = mark(auth_client, pendiente[0], pendiente[1], True)["state"]

    # Con 65 temas no existe el 90% exacto: se pasa de 89% a 91%.
    assert estado["phase_progress"] >= 90
    assert estado["new_phase_unlocked"] is True
    assert estado["unlocked_phase_name"] == "Gestión proactiva"


def test_las_insignias_siguen_el_cumplimiento(auth_client: TestClient) -> None:
    # La primera marca de "cumple" en todo el recorrido concede "Primer paso".
    primero = node_at(get_course(auth_client), 0)
    primer_codigo = phase_codes(auth_client, PHASE_0)[0][1]
    primera_marca = mark(auth_client, primero["id"], primer_codigo, True)["state"]
    assert [badge["slug"] for badge in primera_marca["new_badges"]] == ["primer-paso"]

    # El resto de temas del punto no vuelve a concederla.
    mark_node(auth_client, primero["id"], True)

    # Cumplir el nivel entero concede la insignia del nivel.
    mark_phase(auth_client, PHASE_0, True)

    badges = auth_client.get("/api/badges/me").json()
    ganadas = {badge["slug"] for badge in badges["badges"] if badge["earned"]}
    assert {"primer-paso", "cimientos-vpo"} <= ganadas
    assert badges["total"] == 6


def test_una_insignia_no_se_concede_dos_veces(auth_client: TestClient) -> None:
    course = get_course(auth_client)
    mark_node(auth_client, node_at(course, 0)["id"], True)

    estado = mark_node(auth_client, node_at(course, 1)["id"], True)

    assert estado["new_badges"] == []
    badges = auth_client.get("/api/badges/me").json()
    ganadas = [b["slug"] for b in badges["badges"] if b["earned"]]
    assert ganadas.count("primer-paso") == 1


def test_el_siguiente_punto_es_el_primero_con_brechas(auth_client: TestClient) -> None:
    course = get_course(auth_client)
    # Todo empieza en "no cumple", asi que el primer punto ya tiene brechas.
    assert course["summary"]["next_node_id"] == course["phases"][0]["nodes"][0]["id"]

    mark_node(auth_client, node_at(course, 0)["id"], True)

    actualizado = get_course(auth_client)
    assert actualizado["summary"]["next_node_id"] == node_at(actualizado, 1)["id"]
