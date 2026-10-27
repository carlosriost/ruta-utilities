"""Trazabilidad del contenido con la autoevaluacion VPO.

``app/seed/vpo/catalog.json`` es la lista oficial de requisitos. Estos tests
garantizan que el recorrido los cubra todos, cada uno una sola vez y en su
nivel y bloque correctos.
"""

import json
import re
from collections import Counter
from pathlib import Path

import pytest

from app.seed.content import BADGES, PHASES
from app.seed.vpo.builder import UNLOCK_THRESHOLDS

CATALOG = json.loads(
    (Path(__file__).resolve().parents[1] / "app/seed/vpo/catalog.json").read_text(
        encoding="utf-8"
    )
)
BY_CODE = {item["code"]: item for item in CATALOG}


def _blocks():
    for phase in PHASES:
        for node in phase["nodes"]:
            yield phase, node, node["activity"]["payload"]


def test_el_recorrido_cubre_todos_los_requisitos() -> None:
    cubiertos = Counter(
        requirement["code"]
        for _, _, payload in _blocks()
        for requirement in payload["requirements"]
    )

    assert set(cubiertos) == set(BY_CODE), (
        f"faltan: {sorted(set(BY_CODE) - set(cubiertos))} | "
        f"sobran: {sorted(set(cubiertos) - set(BY_CODE))}"
    )
    repetidos = {code: n for code, n in cubiertos.items() if n > 1}
    assert not repetidos, f"requisitos repetidos: {repetidos}"


def test_cada_requisito_esta_en_su_nivel_y_bloque() -> None:
    for phase, node, payload in _blocks():
        for requirement in payload["requirements"]:
            origen = BY_CODE[requirement["code"]]
            assert origen["level"] == phase["order_index"], (
                f"{requirement['code']} es de nivel {origen['level']} "
                f"y esta en {phase['slug']}"
            )
            assert origen["block"] == payload["vpo_block"], (
                f"{requirement['code']} es del bloque {origen['block']!r} "
                f"y esta en {node['slug']}"
            )


def test_los_temas_estan_redactados_en_espanol() -> None:
    for _, node, payload in _blocks():
        for requirement in payload["requirements"]:
            assert requirement["title"], node["slug"]
            assert len(requirement["detail"]) > 40, requirement["code"]
            assert not requirement["detail"].startswith("The facility")


def test_no_quedan_cuestionarios_en_el_contenido() -> None:
    """La aplicacion es una lista de verificacion: no evalua a nadie."""
    for _, node, payload in _blocks():
        assert "questions" not in node["activity"], node["slug"]
        assert "items" not in payload, node["slug"]
        assert "passing_score" not in node["activity"], node["slug"]


@pytest.mark.parametrize("phase", PHASES, ids=lambda p: p["slug"])
def test_el_umbral_del_nivel_es_el_declarado(phase: dict) -> None:
    assert phase["unlock_threshold"] == UNLOCK_THRESHOLDS[phase["order_index"]]


def test_los_umbrales_bajan_con_la_madurez() -> None:
    umbrales = [phase["unlock_threshold"] for phase in PHASES]
    assert umbrales == [100, 90, 80, 70, 70]


@pytest.mark.parametrize("phase", PHASES, ids=lambda p: p["slug"])
def test_el_peso_de_un_punto_es_su_numero_de_temas(phase: dict) -> None:
    for node in phase["nodes"]:
        assert node["weight"] == len(node["activity"]["payload"]["requirements"])
        assert node["weight"] >= 1


def test_cada_punto_tiene_contexto() -> None:
    for _, node, _payload in _blocks():
        activity = node["activity"]
        assert activity["objective"], node["slug"]
        assert activity["body"], node["slug"]


def test_los_slugs_son_unicos() -> None:
    slugs = [node["slug"] for phase in PHASES for node in phase["nodes"]]
    assert len(slugs) == len(set(slugs))
    assert len({phase["slug"] for phase in PHASES}) == len(PHASES)
    assert len({badge["slug"] for badge in BADGES}) == len(BADGES)


def test_las_insignias_apuntan_a_niveles_existentes() -> None:
    phase_slugs = {phase["slug"] for phase in PHASES}
    for badge in BADGES:
        if badge["rule_type"] == "PHASE_COMPLIANT":
            assert badge["rule_ref"] in phase_slugs, badge["slug"]


def test_los_iconos_estan_registrados_en_el_frontend() -> None:
    icons_file = Path(__file__).resolve().parents[2] / "frontend/src/utils/icons.ts"
    if not icons_file.exists():  # backend desplegado sin el frontend
        pytest.skip("frontend/src/utils/icons.ts no disponible")

    registrados = set(
        re.findall(
            r"^\s{2}([a-z][a-zA-Z0-9]*):\s",
            icons_file.read_text(encoding="utf-8"),
            re.M,
        )
    )
    usados = (
        {node["icon"] for phase in PHASES for node in phase["nodes"]}
        | {phase["icon"] for phase in PHASES}
        | {badge["icon"] for badge in BADGES}
    )
    assert usados <= registrados, f"iconos sin registrar: {sorted(usados - registrados)}"
