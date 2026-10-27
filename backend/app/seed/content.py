"""Contenido de la Ruta Utilities.

El curso son los requisitos VPO del pilar Safety que aplican al area de
Utilities (columna "Utilities = Y" de la autoevaluacion de la planta). Cada
nivel de madurez VPO (0 a 3) es una zona del mapa y cada bloque VPO es un punto
de aprendizaje.

Este archivo es la UNICA fuente del contenido: el seed lo vuelca en PostgreSQL
y a partir de ahi la aplicacion lee siempre desde la base de datos.

Para editar el curso, modifica ``app/seed/vpo/nivel_*.py`` y vuelve a ejecutar
``python -m app.seed``. El seed sincroniza el catalogo: actualiza lo que existe,
crea lo nuevo y elimina lo que ya no aparece aqui.

``app/seed/vpo/catalog.json`` guarda la lista oficial de requisitos (codigo,
nivel y bloque) y los tests comprueban que el curso los cubra todos.

Claves de icono: se traducen a iconos de lucide-react en
``frontend/src/utils/icons.ts``.
"""

from app.models.enums import BadgeRule
from app.seed.vpo.nivel_0 import ZONE as NIVEL_0
from app.seed.vpo.nivel_1 import ZONE as NIVEL_1
from app.seed.vpo.nivel_2 import ZONE as NIVEL_2
from app.seed.vpo.nivel_3 import ZONE as NIVEL_3
from app.seed.vpo.nivel_4 import ZONE as NIVEL_4

PHASES: list[dict] = [NIVEL_0, NIVEL_1, NIVEL_2, NIVEL_3, NIVEL_4]

BADGES: list[dict] = [
    {
        "slug": "primer-paso",
        "name": "Primer paso",
        "description": "Marcaste tu primer tema como cumplido.",
        "icon": "rocket",
        "theme": "mint",
        "rule_type": BadgeRule.FIRST_REQUIREMENT_MET.value,
        "rule_ref": None,
    },
    {
        "slug": "cimientos-vpo",
        "name": "Cimientos VPO",
        "description": "El nivel 0 cumple el 100% de sus temas.",
        "icon": "shield",
        "theme": "mint",
        "rule_type": BadgeRule.PHASE_COMPLIANT.value,
        "rule_ref": "nivel-0",
    },
    {
        "slug": "control-del-riesgo",
        "name": "Control del riesgo",
        "description": "El nivel 1 alcanza el 90% de cumplimiento.",
        "icon": "gauge",
        "theme": "sky",
        "rule_type": BadgeRule.PHASE_COMPLIANT.value,
        "rule_ref": "nivel-1",
    },
    {
        "slug": "gestion-proactiva",
        "name": "Gestión proactiva",
        "description": "El nivel 2 alcanza el 80% de cumplimiento.",
        "icon": "target",
        "theme": "amber",
        "rule_type": BadgeRule.PHASE_COMPLIANT.value,
        "rule_ref": "nivel-2",
    },
    {
        "slug": "duenos-del-territorio",
        "name": "Dueños del territorio",
        "description": "El nivel 3 alcanza el 70% de cumplimiento.",
        "icon": "handshake",
        "theme": "grape",
        "rule_type": BadgeRule.PHASE_COMPLIANT.value,
        "rule_ref": "nivel-3",
    },
    {
        "slug": "maestro-utilities",
        "name": "Maestro Utilities",
        "description": "Los cinco niveles alcanzan su umbral de cumplimiento.",
        "icon": "trophy",
        "theme": "teal",
        "rule_type": BadgeRule.COURSE_COMPLIANT.value,
        "rule_ref": None,
    },
]
