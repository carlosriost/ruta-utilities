"""Nivel 2 de madurez VPO (Safety / Utilities): gestión proactiva."""

from app.seed.vpo.builder import block_node, req, zone

NODES = [
    block_node(
        slug="n2-seguridad-operacional",
        title="Seguridad operacional",
        description="Champions, estrés térmico e izajes artesanales.",
        block="Operational Safety Management",
        icon="shield",
        requirements=[
            req(
                "R.1.1.1.5",
                "Safety Champions en cada área",
                "Cada área nombra al menos un Safety Champion, con tiempo dedicado fuera de sus "
                "responsabilidades de producción para ejercer el rol. Sus competencias se alinean "
                "con Seguridad de Zona (al menos nivel avanzado de Safety en SKAP).",
            ),
            req(
                "R.1.1.2.10",
                "Toolkits de evaluación de riesgos en 60% o más",
                "Los GOP, toolkits y tableros que apoyan la evaluación de riesgos están en al "
                "menos 60%, con glidepaths para cerrar las brechas.",
            ),
            req(
                "R.1.1.9.5",
                "Estructuras de izaje fabricadas en planta",
                "No se usan estructuras de izaje hechas en casa salvo que un experto acreditado "
                "las apruebe por escrito, antes del primer uso y después de cada modificación "
                "importante.",
            ),
            req(
                "R.1.1.10.1",
                "Gestión del estrés térmico",
                "Una evaluación identifica los peligros por calor (límites legales o ISO 7243, "
                "tipo de trabajo, duración, ciclos de trabajo y descanso, agua disponible, "
                "temperatura, humedad, ventilación, uniformes y PPE, sol directo). Los controles "
                "quedan en un SOP: información sobre síntomas, acceso a agua e hidratación, "
                "pausas y rotación, zonas frescas o con sombra y PPE adaptado.",
            ),
            req(
                "R.1.1.11.5",
                "Formulario de seguridad del trabajador temporal",
                "Cada temporal firma un formulario que cubre el área, las tareas y equipos, los "
                "peligros y medidas preventivas, la vigilancia de salud y la declaración de que "
                "recibió y entendió la formación y de que solo hará las tareas asignadas.",
            ),
        ],
        objective="Conocer los controles proactivos del nivel 2 en seguridad operacional.",
        body=(
            "El nivel 2 agrega personas y controles que se anticipan al problema.\n\n"
            "* Safety Champions: al menos uno por área, con tiempo dedicado real para el rol.\n"
            "* Estrés térmico: en salas de calderas y compresores el calor es un riesgo de "
            "salud que se evalúa y se controla con agua, pausas, rotación y zonas frescas.\n"
            "* Izajes: una estructura fabricada en la planta solo se puede usar si un experto "
            "acreditado la aprobó por escrito.\n"
            "* Temporales: cada uno firma un formulario con sus tareas, peligros y formación."
        ),
    ),
    block_node(
        slug="n2-reporte-incidentes",
        title="Reporte de incidentes",
        description="Safety Alerts, rutinas y proceso MDI.",
        block="Incident Reporting & Management",
        icon="file",
        requirements=[
            req(
                "R.1.2.1.8",
                "Safety Alert tras el RCA",
                "La planta envía a Seguridad de Zona, para validación, un Safety Alert en idioma "
                "local y en inglés por fatalidades, SIF reales y potenciales y LTI, apenas "
                "termina el análisis de causa raíz.",
            ),
            req(
                "R.1.2.1.10",
                "Incidentes en las rutinas de la planta",
                "La revisión de los incidentes, incluidas las enfermedades ocupacionales y los "
                "Safety Alerts de otras plantas, se integra en las rutinas: cuartos de equipo, "
                "entregas de turno y reuniones de gestión.",
            ),
            req(
                "R.1.2.1.11",
                "Aprender de los Safety Alerts",
                "La planta revisa los aprendizajes de todos los Safety Alerts que recibe, "
                "implementa los que apliquen y hace seguimiento hasta cerrar las acciones.",
            ),
            req(
                "R.1.2.1.12",
                "Proceso de trabajo restringido (MDI)",
                "Participa un profesional de la salud, las restricciones se definen caso a caso, "
                "el líder se entera y verifica que se cumplan. El trabajo desde casa como tarea "
                "modificada está prohibido salvo cargos administrativos y por un máximo de 5 días "
                "hábiles; si se excede, el caso se reclasifica como LTI.",
            ),
        ],
        objective="Entender cómo la planta convierte los incidentes en aprendizaje.",
        body=(
            "En el nivel 2 el incidente no se queda en el informe: circula y cambia la forma de "
            "trabajar.\n\n"
            "* Cuando termina el RCA se emite un Safety Alert, en español y en inglés.\n"
            "* Los incidentes (propios y de otras plantas) se revisan en el cuarto de equipo, "
            "en la entrega de turno y en las reuniones de gestión.\n"
            "* Los aprendizajes de los alertas que llegan de otras plantas se implementan y se "
            "siguen hasta cerrarlos.\n\n"
            "Cuando en tu entrega de turno se comenta un alerta de otra cervecería, la pregunta "
            "correcta es: ¿esto nos puede pasar aquí?"
        ),
    ),
    block_node(
        slug="n2-procesos-alto-riesgo",
        title="Procesos de alto riesgo",
        description="Toolkits al 70%, coordinadores e indicadores.",
        block="High Risk Processes Management",
        icon="flame",
        requirements=[
            req(
                "R.1.3.1.14",
                "Toolkit PSM NH3 en 70% o más",
                "El toolkit de amoníaco sube a al menos 70%, con glidepaths para cerrar brechas.",
            ),
            req(
                "R.1.3.1.16",
                "Toolkit SSM en 70% o más",
                "El toolkit de seguridad en vapor sube a al menos 70%, con glidepaths para cerrar "
                "brechas.",
            ),
            req(
                "R.1.3.1.18",
                "Coordinadores y comités de alto riesgo",
                "Hay coordinador de PSM NH3 (si hay amoníaco), DEPSM, SSM y ESM, y comités que se "
                "reúnen al menos cada trimestre, con tiempo y recursos para hacer su trabajo y "
                "para formarse. Una misma persona puede cubrir varios procesos.",
            ),
            req(
                "R.1.3.1.19",
                "Indicadores de los programas de alto riesgo",
                "La planta define y sigue indicadores en el nivel de gestión y en los cuartos de "
                "equipo y puestos de trabajo: puntaje de toolkits, cierre de planes de acción, "
                "reporte y cierre de precursores SIF, cierre de órdenes de trabajo y fugas "
                "reportadas.",
            ),
        ],
        objective="Reconocer cómo se gestionan y miden los procesos de alto riesgo en el nivel 2.",
        body=(
            "En el nivel 1 los toolkits debían llegar a 60%. En el nivel 2, PSM NH3 y SSM suben "
            "a 70%.\n\n"
            "Pero lo más importante no es el número: es que haya alguien responsable y que los "
            "indicadores se vean donde se trabaja.\n\n"
            "* Coordinador para cada proceso (una persona puede cubrir varios) y comités que se "
            "reúnen al menos cada trimestre.\n"
            "* Indicadores en el cuarto de equipo: puntaje de toolkits, cierre de acciones, "
            "precursores SIF y fugas reportadas.\n\n"
            "Las fugas reportadas son un indicador clave en Utilities: reportarlas temprano es "
            "lo que evita que se conviertan en emergencias."
        ),
    ),
    block_node(
        slug="n2-ergonomia",
        title="Ergonomía y cargas",
        description="Evaluación MHA y EWRA.",
        block="Material Handling and Ergonomics",
        icon="package",
        requirements=[
            req(
                "R.1.5.1.1",
                "Evaluaciones MHA y EWRA",
                "La planta hace y documenta la evaluación de manipulación de materiales (MHA) y "
                "la evaluación ergonómica de los puestos de trabajo (EWRA).",
            ),
            req(
                "R.1.5.1.4",
                "Formación en manipulación de cargas y ergonomía",
                "A partir de la MHA y la EWRA, la planta forma al FLTM en manipulación manual y "
                "ergonomía con apoyo de SKAP, con refuerzo al menos cada 3 años.",
            ),
        ],
        objective="Entender cómo se evalúan las cargas y los puestos de trabajo.",
        body=(
            "Levantar sacos de sal para el ablandador, mover canecas de químicos, trabajar "
            "agachado en una válvula: son tareas que no causan accidentes, pero sí lesiones que "
            "aparecen con los años.\n\n"
            "El nivel 2 pide dos evaluaciones:\n\n"
            "* MHA: evaluación de la manipulación de materiales.\n"
            "* EWRA: evaluación ergonómica de los puestos de trabajo.\n\n"
            "Con sus resultados se define la formación del FLTM en manipulación manual y "
            "ergonomía."
        ),
    ),
    block_node(
        slug="n2-sustancias-peligrosas",
        title="Sustancias peligrosas",
        description="Mantenimiento y CIP sin fugas.",
        block="Hazardous Substances",
        icon="flask",
        requirements=[
            req(
                "R.1.6.1.21",
                "Mantenimiento e integridad de sistemas con químicos",
                "Hay un programa de inspección, pruebas y mantenimiento preventivo, y un programa "
                "detallado de integridad mecánica, para mantener el almacenamiento y la operación "
                "seguros y asegurar estaciones de CIP sin fugas.",
            ),
        ],
        objective="Entender por qué una fuga pequeña en el CIP no es un tema menor.",
        body=(
            "Las estaciones de CIP manejan soda cáustica y ácidos a temperatura. Una fuga "
            "pequeña, un goteo en una brida o una bomba que 'siempre ha goteado' son el inicio "
            "de una quemadura química o de una falla mayor.\n\n"
            "El nivel 2 exige un programa de inspección, pruebas y mantenimiento preventivo, y "
            "un programa de integridad mecánica, con una meta explícita: estaciones de CIP sin "
            "fugas."
        ),
    ),
    block_node(
        slug="n2-lototo",
        title="LOTOTO y máquinas",
        description="El bloqueo entra al monitoreo.",
        block="LOTOTO and Machine Safety",
        icon="lock",
        requirements=[
            req(
                "R.1.7.1.10",
                "SAM, LOTOTO y jogging en el monitoreo de seguridad",
                "La verificación de las actividades de SAM, LOTOTO y jogging está incorporada en "
                "el proceso de monitoreo de seguridad.",
            ),
        ],
        objective="Entender por qué el bloqueo se verifica en campo y no solo en el procedimiento.",
        body=(
            "Tener un buen procedimiento de LOTOTO no garantiza que se aplique bien todos los "
            "días. Por eso, en el nivel 2, el bloqueo entra en la matriz de monitoreo de "
            "seguridad.\n\n"
            "Eso significa que un líder puede llegar mientras haces un bloqueo y revisar "
            "contigo: si identificaste todas las energías, si el candado y la tarjeta están "
            "puestos, si comprobaste la energía cero y cómo se maneja la entrega de turno.\n\n"
            "No es una auditoría para buscar errores: es la oportunidad de corregir a tiempo lo "
            "que podría costar una mano o una vida."
        ),
    ),
    block_node(
        slug="n2-espacios-confinados",
        title="Espacios confinados",
        description="Un SOP por cada espacio.",
        block="Confined Spaces",
        icon="cylinder",
        requirements=[
            req(
                "R.1.10.1.6",
                "SOP específico para cada espacio confinado",
                "Cada espacio confinado tiene su propio SOP, vinculado con su procedimiento de "
                "LOTOTO, que detalla peligros, medidas de control, formación necesaria, "
                "requisitos de permiso y supervisión, y la respuesta de emergencia y rescate.",
            ),
            req(
                "R.1.10.1.7",
                "Espacios confinados en las rutinas de monitoreo",
                "La entrada a espacios confinados forma parte de las rutinas de monitoreo de "
                "seguridad.",
            ),
        ],
        objective="Saber qué contiene el SOP de cada espacio confinado.",
        body=(
            "En el nivel 0 la planta identifica y rotula sus espacios confinados. En el nivel 2 "
            "cada uno tiene su propio procedimiento.\n\n"
            "No es lo mismo entrar a un tanque de agua tratada que a un tanque que contenía "
            "químicos o a un foso donde puede acumularse CO2. Cada SOP detalla:\n\n"
            "* Los peligros de ese espacio en particular y cómo se controlan.\n"
            "* Su procedimiento de LOTOTO asociado.\n"
            "* La formación, el permiso y la supervisión necesarios.\n"
            "* La respuesta de emergencia y el rescate."
        ),
    ),
    block_node(
        slug="n2-contratistas",
        title="Contratistas",
        description="Charlas de seguridad diarias.",
        block="Contractor and Service Providers Management",
        icon="users",
        requirements=[
            req(
                "R.1.12.1.15",
                "Charlas de seguridad diarias (paso 8)",
                "Se hacen charlas de seguridad (toolbox) para discutir cada día los aspectos de "
                "seguridad de las tareas, las medidas de control y temas que aumenten la "
                "conciencia de seguridad.",
            ),
        ],
        objective="Reconocer el valor de la charla diaria antes de empezar el trabajo.",
        body=(
            "La charla de seguridad (toolbox meeting) es el paso 8 de la gestión de "
            "contratistas y ocurre todos los días, antes de empezar.\n\n"
            "Sirve para tres cosas: repasar qué se va a hacer hoy, recordar los peligros y "
            "controles de esas tareas y hablar de temas que suben la conciencia de seguridad, "
            "como un alerta reciente.\n\n"
            "Si trabajas cerca de una obra en tu área, participar en la charla te permite saber "
            "qué van a hacer ese día y qué riesgos te pueden alcanzar."
        ),
    ),
    block_node(
        slug="n2-salud-ocupacional",
        title="Salud ocupacional",
        description="Equipos de control y medición calibrados.",
        block="Occupational Health",
        icon="health",
        requirements=[
            req(
                "R.1.13.1.7",
                "Medidas técnicas contra enfermedades ocupacionales",
                "Los equipos instalados para reducir el riesgo de enfermedades ocupacionales "
                "entran en la inspección de equipos críticos del área. Los equipos de medición "
                "de exposición (sonómetros, luxómetros) y los médicos (audiómetros, espirómetros) "
                "están calibrados, con los programas cargados en el sistema de órdenes de trabajo.",
            ),
        ],
        objective="Entender por qué los controles de salud también necesitan mantenimiento.",
        body=(
            "En el nivel 1 la planta identifica los peligros para la salud. En el nivel 2 se "
            "asegura de que las medidas técnicas realmente funcionen.\n\n"
            "Una cabina acústica, un sistema de extracción o un encerramiento de compresores "
            "reducen la exposición solo si se mantienen. Por eso entran en la inspección de "
            "equipos críticos del área.\n\n"
            "Lo mismo aplica a los equipos con los que se mide: un sonómetro descalibrado puede "
            "indicar que el ruido está bien cuando no lo está. Sonómetros, luxómetros, "
            "audiómetros y espirómetros se calibran, y sus programas viven en el sistema de "
            "órdenes de trabajo."
        ),
    ),
    block_node(
        slug="n2-seguridad-vial",
        title="Seguridad vial",
        description="Conducción defensiva fuera de la planta.",
        block="Road & Driving Safety",
        icon="car",
        requirements=[
            req(
                "R.1.15.1.1",
                "Formación en conducción defensiva",
                "Quien conduzca un vehículo de la empresa, arrendado o propio por motivos "
                "laborales recibe formación en conducción defensiva: cumplimiento de las normas "
                "de tránsito, uso del cinturón, política de alcohol, tiempos de descanso y "
                "fatiga, y distracciones como el uso del celular.",
            ),
        ],
        objective="Aplicar las reglas de conducción defensiva en desplazamientos de trabajo.",
        body=(
            "Los desplazamientos por trabajo son uno de los riesgos más subestimados: ir a otra "
            "planta, recoger un repuesto o atender una urgencia de noche.\n\n"
            "VPO exige formación en conducción defensiva para quien conduce por motivos "
            "laborales, sea el vehículo de la empresa, arrendado o propio.\n\n"
            "Antes de salir, repasa esta lista."
        ),
    ),
    block_node(
        slug="n2-monitoreo-coaching",
        title="Monitoreo y coaching",
        description="JHA y comunicación de hallazgos.",
        block="Safety Monitoring & Coaching",
        icon="eye",
        requirements=[
            req(
                "R.1.16.1.6",
                "Estrategia y SOP de JHA",
                "La planta define los cargos, prioriza y hace un plan para realizar análisis de "
                "peligros por tarea (JHA) detallados, y lo ejecuta. El plan asegura que todos "
                "los cargos queden cubiertos en un máximo de 3 años.",
            ),
            req(
                "R.1.16.1.7",
                "Comunicación de los hallazgos",
                "Los hallazgos positivos y negativos del monitoreo y el coaching se comunican en "
                "los puestos de trabajo y en los cuartos de equipo.",
            ),
        ],
        objective="Conocer el alcance del JHA y dónde se comunican los hallazgos.",
        body=(
            "El JHA (Job Hazard Analysis) analiza en detalle los peligros de un cargo: qué hace "
            "esa persona paso a paso y qué puede salir mal.\n\n"
            "En el nivel 2 la planta prioriza y planifica los JHA de forma que todos los cargos "
            "queden cubiertos en un máximo de 3 años.\n\n"
            "Y los resultados del monitoreo no se quedan en un informe: lo bueno y lo que hay "
            "que corregir se comunica en el puesto de trabajo y en el cuarto de equipo, donde "
            "sirve."
        ),
    ),
    block_node(
        slug="n2-cultura-seguridad",
        title="Cultura de seguridad",
        description="Comunicación, observaciones y campañas.",
        block="Behavioral Safety Culture",
        icon="handshake",
        requirements=[
            req(
                "R.1.17.5.2",
                "Estrategia de comunicación en seguridad",
                "Todos los grupos de interés reciben la información relevante: Safety Alerts "
                "(casi accidentes, incidentes, emergencias y sus acciones), resultados de "
                "evaluaciones de cultura y encuestas, resultados de evaluaciones de riesgo, "
                "resultados del coaching y monitoreo, comités de seguridad y cambios en los "
                "requisitos.",
            ),
            req(
                "R.1.17.6.1",
                "Observaciones de comportamiento (SBO) para líderes",
                "Los líderes se forman en el proceso de SBO (el personal nuevo en 6 meses), el "
                "área de ES los acompaña y valida sus habilidades, hay una meta mensual por "
                "líder con seguimiento, se da retroalimentación a la persona observada, se "
                "analizan tendencias con plan de acción y ES hace verificaciones de calidad.",
            ),
            req(
                "R.1.17.7.1",
                "Campañas y Día de la Seguridad",
                "La planta organiza campañas de seguridad y salud y el Día o la Semana de la "
                "Seguridad (28 de abril), con temas elegidos según los requisitos globales y de "
                "Zona y el análisis de tendencias de los datos de seguridad.",
            ),
        ],
        objective="Conocer las prácticas de cultura de seguridad que agrega el nivel 2.",
        body=(
            "El nivel 2 hace visible la seguridad:\n\n"
            "* Una estrategia de comunicación para que los alertas, los resultados de las "
            "evaluaciones y los cambios de requisitos lleguen a todos.\n"
            "* Observaciones de comportamiento (SBO) hechas por los líderes, con meta mensual, "
            "retroalimentación a la persona observada y análisis de tendencias.\n"
            "* Campañas de seguridad y salud, y el Día de la Seguridad cada 28 de abril.\n\n"
            "Una SBO no es una inspección: la conversación posterior, en la que te explican qué "
            "vieron y escuchan por qué trabajas así, es la parte que cambia comportamientos."
        ),
    ),
]


ZONE = zone(
    level=2,
    name="Gestión proactiva",
    description=(
        "Nivel 2 de VPO: la planta se adelanta a los problemas. Champions, indicadores, "
        "observaciones de comportamiento, JHA y aprendizaje de los incidentes."
    ),
    theme="amber",
    icon="target",
    nodes=NODES,
)
