"""Piezas para declarar los niveles VPO.

Cada nivel de madurez es una zona del mapa, cada bloque VPO es un punto
("bolita") y cada requisito es un tema que se marca como cumplido o no
cumplido. No hay cuestionarios: la aplicacion es una lista de verificacion.
"""

from __future__ import annotations

#: Cumplimiento minimo (%) que debe alcanzar cada nivel para abrir el siguiente.
#: Es el numero que define VPO y baja con la madurez: lo basico se exige
#: completo, lo avanzado admite brechas.
UNLOCK_THRESHOLDS: dict[int, int] = {0: 100, 1: 90, 2: 80, 3: 70, 4: 70}


def req(code: str, title: str, detail: str) -> dict:
    """Un tema: el requisito VPO con su codigo oficial."""
    return {"code": code, "title": title, "detail": detail}


def block_node(
    *,
    slug: str,
    title: str,
    description: str,
    block: str,
    icon: str,
    requirements: list[dict],
    objective: str,
    body: str,
) -> dict:
    return {
        "slug": slug,
        "title": title,
        "description": description,
        "icon": icon,
        # El peso de un punto es su numero de temas: asi el porcentaje del
        # nivel equivale a la proporcion de temas cumplidos.
        "weight": len(requirements),
        "activity": {
            "objective": objective,
            "body": body,
            "payload": {"vpo_block": block, "requirements": requirements},
        },
    }


def zone(
    *,
    level: int,
    name: str,
    description: str,
    theme: str,
    icon: str,
    nodes: list[dict],
) -> dict:
    return {
        "slug": f"nivel-{level}",
        "name": name,
        "description": description,
        "order_index": level,
        "unlock_threshold": UNLOCK_THRESHOLDS[level],
        "theme": theme,
        "icon": icon,
        "nodes": nodes,
    }
