"""Exporta el recorrido a JSON para la version descargable (un solo HTML).

    python -m app.seed.export_json

El contenido sigue siendo el de ``content.py``: este script solo lo aplana con
identificadores numericos, igual que haria PostgreSQL, para que la version
offline no necesite ni base de datos ni backend.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.core.constants import DEFAULT_UNLOCK_THRESHOLD
from app.seed.content import BADGES, PHASES

DESTINO = Path(__file__).resolve().parents[3] / "frontend/src/offline/course.json"


def build() -> dict:
    phases = []
    node_id = 0

    for phase_index, phase in enumerate(PHASES, start=1):
        nodes = []
        for order, node in enumerate(phase["nodes"]):
            node_id += 1
            activity = node["activity"]
            payload = activity["payload"]
            nodes.append(
                {
                    "id": node_id,
                    "phase_id": phase_index,
                    "slug": node["slug"],
                    "title": node["title"],
                    "description": node.get("description", ""),
                    "icon": node.get("icon", "book"),
                    "order_index": order,
                    "objective": activity.get("objective", ""),
                    "body": activity.get("body", ""),
                    "vpo_block": payload.get("vpo_block"),
                    "requirements": payload["requirements"],
                }
            )

        phases.append(
            {
                "id": phase_index,
                "slug": phase["slug"],
                "name": phase["name"],
                "description": phase["description"],
                "order_index": phase["order_index"],
                "unlock_threshold": phase.get(
                    "unlock_threshold", DEFAULT_UNLOCK_THRESHOLD
                ),
                "theme": phase.get("theme", "sky"),
                "icon": phase.get("icon", "compass"),
                "nodes": nodes,
            }
        )

    badges = [
        {
            "id": index,
            "slug": badge["slug"],
            "name": badge["name"],
            "description": badge["description"],
            "icon": badge["icon"],
            "theme": badge.get("theme", "amber"),
            "rule_type": badge["rule_type"],
            "rule_ref": badge.get("rule_ref"),
        }
        for index, badge in enumerate(BADGES, start=1)
    ]

    return {"phases": phases, "badges": badges}


def run() -> None:
    course = build()
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(
        json.dumps(course, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    nodes = [node for phase in course["phases"] for node in phase["nodes"]]
    temas = sum(len(node["requirements"]) for node in nodes)
    print(f"Escrito {DESTINO}")
    print(
        f"  {len(course['phases'])} niveles | {len(nodes)} puntos | "
        f"{temas} temas | {len(course['badges'])} insignias"
    )
    print(f"  {DESTINO.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    run()
