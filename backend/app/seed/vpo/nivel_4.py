"""Nivel 4 de madurez VPO (Safety): referente.

OJO: en la autoevaluacion de la planta estos 17 requisitos estan marcados como
"Utilities = N", es decir, hoy no se evaluan para el area. Se incluyen como
nivel aspiracional, a peticion explicita, y asi se advierte en la descripcion
de la zona.
"""

from app.seed.vpo.builder import block_node, req, zone

NODES = [
    block_node(
        slug="n4-seguridad-operacional",
        title="Seguridad operacional",
        description="El FLTM gestiona permisos y equipos de izaje.",
        block="Operational Safety Management",
        icon="shield",
        requirements=[
            req(
                "R.1.1.2.13",
                "Toolkits de evaluación de riesgos en 80% o más",
                "Los GOP, toolkits y tableros que apoyan la evaluación de riesgos llegan a al "
                "menos 80%, con glidepaths para cerrar las brechas.",
            ),
            req(
                "R.1.1.9.7",
                "El FLTM gestiona la seguridad de los izajes",
                "El FLTM revisa y actualiza los SOP y las OPL, prepara los permisos de trabajo "
                "de los izajes de su área y es dueño de los equipos de izaje: además de la "
                "inspección, su almacenamiento y su rotulado.",
            ),
        ],
        objective="Pasar de verificar permisos a prepararlos y mantener los equipos.",
        body=(
            "En el nivel 3 el dueño del territorio verifica los permisos. En el nivel 4 los "
            "prepara.\n\n"
            "El salto es de control a gestión: el FLTM revisa y actualiza los procedimientos "
            "(SOP) y las lecciones de un punto (OPL) de su área, redacta los permisos de "
            "izaje y responde por los equipos completos: inspección, almacenamiento y "
            "rotulado.\n\n"
            "Quien opera todos los días es quien mejor sabe cómo debería estar escrito el "
            "procedimiento."
        ),
    ),
    block_node(
        slug="n4-procesos-alto-riesgo",
        title="Procesos de alto riesgo",
        description="Toolkits al 90%.",
        block="High Risk Processes Management",
        icon="flame",
        requirements=[
            req(
                "R.1.3.1.27",
                "Toolkit PSM NH3 en 90% o más",
                "El toolkit de amoníaco alcanza al menos 90%, con glidepaths para cerrar las "
                "brechas que queden.",
            ),
            req(
                "R.1.3.1.29",
                "Toolkit SSM en 90% o más",
                "El toolkit de seguridad en vapor alcanza al menos 90%, con glidepaths para "
                "cerrar brechas.",
            ),
            req(
                "R.1.3.1.30",
                "Toolkit ESM en 90% o más",
                "El toolkit de seguridad eléctrica alcanza al menos 90%, con glidepaths para "
                "cerrar brechas.",
            ),
        ],
        objective="Conocer el techo de exigencia de los toolkits de alto riesgo.",
        body=(
            "El recorrido completo de los toolkits de alto riesgo marca la madurez de la "
            "planta:\n\n"
            "* Nivel 1: 60%\n"
            "* Nivel 2: 70%\n"
            "* Nivel 3: 80%\n"
            "* Nivel 4: 90%\n\n"
            "Llegar al 90% en PSM NH3, SSM y ESM significa que casi todo lo que el estándar "
            "global espera de un sistema de amoníaco, de vapor y eléctrico ya está "
            "implementado y funcionando."
        ),
    ),
    block_node(
        slug="n4-ergonomia",
        title="Ergonomía y cargas",
        description="El FLTM propone y mide.",
        block="Material Handling and Ergonomics",
        icon="package",
        requirements=[
            req(
                "R.1.5.1.5",
                "Participación activa del FLTM en ergonomía",
                "El FLTM propone medidas para reducir los riesgos de manipulación de cargas y "
                "ergonomía, usa el mapa de riesgos ergonómicos de su área y define y sigue "
                "indicadores para medir el impacto de esas medidas.",
            ),
        ],
        objective="Pasar de aplicar las medidas a proponerlas y medir su efecto.",
        body=(
            "En el nivel 3 usas las ayudas que la planta puso. En el nivel 4 propones las "
            "que faltan.\n\n"
            "VPO espera tres cosas del FLTM:\n\n"
            "* Proponer medidas concretas para reducir el esfuerzo y las posturas forzadas.\n"
            "* Usar el mapa de riesgos ergonómicos del área para saber dónde están los "
            "puntos críticos.\n"
            "* Definir y seguir indicadores que muestren si las medidas funcionaron.\n\n"
            "Una propuesta con un indicador detrás es mucho más difícil de ignorar."
        ),
    ),
    block_node(
        slug="n4-lototo",
        title="LOTOTO y máquinas",
        description="Máquinas certificadas y tableros sombra.",
        block="LOTOTO and Machine Safety",
        icon="lock",
        requirements=[
            req(
                "R.1.7.1.15",
                "Máquinas nivel 1 y 2 según el estándar de seguridad de máquinas",
                "Todas las máquinas de nivel 1 y 2 del Global Heat Map cumplen la norma "
                "GTS.GEN.SFT.GSP.007 de seguridad de máquinas.",
            ),
            req(
                "R.1.7.1.16",
                "Equipo de bloqueo específico en tableros sombra",
                "Los equipos críticos tienen su equipo de SAM y LOTOTO específico dispuesto en "
                "tableros sombra: recipientes de cocimiento, dosificación, transferencia de "
                "materias primas, amoníaco, vapor y condensado, CO2 y N2, lavadoras y "
                "pasteurizadores, máquinas de acceso corporal en envasado, llenadoras, "
                "prensas, AGV, alta tensión y todos los espacios confinados.",
            ),
        ],
        objective="Reconocer el estándar de máquinas y el tablero sombra de bloqueo.",
        body=(
            "El nivel 4 cierra el círculo del bloqueo con dos medidas físicas:\n\n"
            "* Las máquinas de nivel 1 y 2 del Global Heat Map cumplen la norma global de "
            "seguridad de máquinas (GTS.GEN.SFT.GSP.007).\n"
            "* Cada equipo crítico tiene su propio equipo de bloqueo en un tablero sombra: "
            "candados, tarjetas y dispositivos de aislamiento con su silueta marcada.\n\n"
            "El tablero sombra no es orden por estética: de un vistazo se ve si falta un "
            "dispositivo, y nadie tiene que improvisar un bloqueo porque no encontró el "
            "elemento correcto."
        ),
    ),
    block_node(
        slug="n4-trabajo-alturas",
        title="Trabajo en alturas",
        description="El FLTM prepara los permisos.",
        block="Working at heights",
        icon="mountain",
        requirements=[
            req(
                "R.1.8.1.16",
                "El FLTM gestiona la seguridad del trabajo en alturas",
                "Revisa y actualiza los SOP y las OPL, prepara los permisos de trabajo en "
                "alturas de su área y es dueño de los equipos: además de la inspección, su "
                "almacenamiento y su rotulado.",
            ),
        ],
        objective="Asumir la gestión completa del trabajo en alturas del área.",
        body=(
            "Mismo salto que en izajes: del control a la gestión.\n\n"
            "En el nivel 3 verificabas que hubiera permiso. En el nivel 4 lo preparas, "
            "mantienes al día los procedimientos de tu área y respondes por los equipos de "
            "protección contra caídas, incluido cómo se guardan y se identifican.\n\n"
            "Un arnés bien guardado dura más y falla menos que uno colgado de un clavo."
        ),
    ),
    block_node(
        slug="n4-espacios-confinados",
        title="Espacios confinados",
        description="Procedimientos y permisos desde el área.",
        block="Confined Spaces",
        icon="cylinder",
        requirements=[
            req(
                "R.1.10.1.9",
                "El FLTM gestiona la seguridad de los espacios confinados",
                "Revisa y actualiza los SOP y las OPL, prepara los permisos de entrada de su "
                "área y es dueño de los equipos de espacios confinados: además de la "
                "inspección, su almacenamiento y su rotulado.",
            ),
        ],
        objective="Gestionar los procedimientos y equipos de entrada del área.",
        body=(
            "En el nivel 2 cada espacio confinado recibió su procedimiento propio. En el "
            "nivel 4 ese procedimiento lo mantiene quien trabaja en el área.\n\n"
            "El FLTM revisa y actualiza los SOP y las OPL, prepara los permisos de entrada y "
            "responde por los equipos de entrada y rescate: medidores, ventilación, trípodes "
            "y arneses, incluido cómo se guardan y se rotulan.\n\n"
            "Nadie conoce mejor las trampas de un tanque que quien lo abre cada parada."
        ),
    ),
    block_node(
        slug="n4-emergencias",
        title="Emergencias",
        description="Procedimientos y equipos del área.",
        block="Emergency Preparedness and Response",
        icon="siren",
        requirements=[
            req(
                "R.1.11.1.14",
                "El FLTM gestiona la respuesta a emergencias del área",
                "Revisa y actualiza los SOP y las OPL de respuesta a emergencias y es dueño de "
                "la inspección de los equipos de emergencia de su área.",
            ),
        ],
        objective="Mantener vivos los procedimientos y equipos de emergencia del área.",
        body=(
            "En el nivel 3 recorrías tu área para comprobar que los extintores estuvieran "
            "despejados y las rutas libres. En el nivel 4 eres dueño de la inspección de esos "
            "equipos y mantienes al día los procedimientos.\n\n"
            "Eso significa que cuando cambia algo en tu área (una línea nueva, un tanque que "
            "se mueve, una ruta que se modifica), el procedimiento de emergencia se actualiza "
            "contigo, no meses después.\n\n"
            "Un plan de emergencia desactualizado es peligroso justo por ser creíble: la "
            "gente confía en él."
        ),
    ),
    block_node(
        slug="n4-monitoreo-coaching",
        title="Monitoreo y coaching",
        description="Observación entre pares y tecnología.",
        block="Safety Monitoring & Coaching",
        icon="eye",
        requirements=[
            req(
                "R.1.16.1.11",
                "Observación entre pares y monitoreo del FLTM",
                "Hay un programa documentado de observación de comportamientos (SBO) y coaching "
                "entre pares del FLTM, con al menos el 40% del FLTM formado, y el monitoreo de "
                "seguridad del área lo asume el propio FLTM.",
            ),
            req(
                "R.1.16.1.12",
                "Tecnología para el monitoreo de seguridad",
                "Se usa tecnología para capturar, documentar y gestionar condiciones inseguras "
                "y comportamientos seguros e inseguros: cámaras inteligentes o CCTV, "
                "telemetría, sensores corporales, drones, robots de detección y sensores de "
                "presencia. El objetivo es trabajar de forma proactiva, identificando brechas "
                "antes de que ocurra el incidente.",
            ),
        ],
        objective="Entender la observación entre pares y el papel de la tecnología.",
        body=(
            "Hasta el nivel 3, quien observa es el líder. En el nivel 4 el FLTM se observa "
            "entre pares: al menos el 40% del equipo formado en observación de "
            "comportamientos (SBO) y coaching.\n\n"
            "Es un cambio grande de cultura. Que un compañero te diga 'oye, así te puedes "
            "lastimar' funciona distinto a que te lo diga el jefe, y el monitoreo del área "
            "pasa a ser del propio equipo.\n\n"
            "A esto se suma la tecnología (cámaras inteligentes, telemetría, sensores "
            "corporales, drones, sensores de presencia), siempre con el mismo propósito: "
            "detectar la brecha antes de que se convierta en un incidente."
        ),
    ),
    block_node(
        slug="n4-cultura-seguridad",
        title="Cultura de seguridad",
        description="Política aplicada, factores humanos y territorios.",
        block="Behavioral Safety Culture",
        icon="handshake",
        requirements=[
            req(
                "R.1.17.9.9",
                "El FLTM se apropia de la Política Global de Seguridad",
                "El FLTM demuestra cómo aplica la Política Global en su rutina diaria y puede "
                "responder: cómo contribuye a eliminar la exposición al riesgo, cómo ayuda VPO "
                "a mejorar la seguridad, qué significa que todos somos líderes en seguridad y "
                "qué significa no tomar atajos.",
            ),
            req(
                "R.1.17.9.11",
                "Concepto de factores humanos aplicado",
                "Los líderes usan el concepto de factores humanos en su rutina: cualquier "
                "característica de una persona que afecte su capacidad de hacer una tarea de "
                "forma segura, como fatiga, estrés, falta de experiencia, formación "
                "insuficiente, supervisión deficiente o problemas personales.",
            ),
            req(
                "R.1.17.9.12",
                "Seguridad territorial en nivel 3",
                "Al menos el 80% de los territorios alcanza como mínimo el nivel 3 de "
                "seguridad territorial, evaluado con los criterios globales.",
            ),
        ],
        objective="Aplicar la política en la rutina y reconocer los factores humanos.",
        body=(
            "El nivel 4 es el de la cultura: la seguridad deja de ser un conjunto de reglas y "
            "se vuelve la forma normal de trabajar.\n\n"
            "Tres señales de que se llegó:\n\n"
            "* Cualquiera puede explicar cómo aplica la Política Global en su turno: sin "
            "atajos, todos somos líderes en seguridad.\n"
            "* Los líderes tienen en cuenta los factores humanos: fatiga, estrés, falta de "
            "experiencia, formación insuficiente, supervisión deficiente o problemas "
            "personales.\n"
            "* Al menos el 80% de los territorios llegó al nivel 3 de seguridad territorial."
        ),
    ),
    block_node(
        slug="n4-cumplimiento-legal",
        title="Cumplimiento legal",
        description="El FLTM conoce lo que le aplica.",
        block="Facility compliance",
        icon="scale",
        requirements=[
            req(
                "R.1.18.1.7",
                "El FLTM conoce los requisitos legales de su área",
                "El FLTM tiene, por formación, conocimiento de los principales requisitos "
                "legales de seguridad y salud en el trabajo que le aplican a él y a su área.",
            ),
        ],
        objective="Cerrar el recorrido sabiendo qué exige la ley en tu área.",
        body=(
            "El cumplimiento legal recorrió todo el mapa: en el nivel 0 la planta identifica "
            "qué leyes le aplican, en el 1 las mantiene al día, en el 3 forma a los líderes y "
            "las mete en las rutinas.\n\n"
            "En el nivel 4 llega hasta el final de la línea: cada integrante del equipo sabe, "
            "por formación, cuáles son los principales requisitos legales de seguridad y "
            "salud que aplican a su trabajo y a su área.\n\n"
            "Es el cierre natural de la ruta: ya no se cumple porque alguien revisa, sino "
            "porque el equipo sabe qué se espera y por qué."
        ),
    ),
]


ZONE = zone(
    level=4,
    name="Referente en seguridad",
    description=(
        "Nivel 4 de VPO: el equipo gestiona su propia seguridad. Nota: en la autoevaluación "
        "de la planta estos requisitos figuran como no aplicables a Utilities; se incluyen "
        "como nivel aspiracional."
    ),
    theme="teal",
    icon="sparkles",
    nodes=NODES,
)
