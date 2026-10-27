"""Nivel 1 de madurez VPO (Safety / Utilities): control del riesgo."""

from app.seed.vpo.builder import block_node, req, zone

NODES = [
    block_node(
        slug="n1-seguridad-operacional",
        title="Seguridad operacional",
        description="SAFE form, inventarios, izajes y trabajo en solitario.",
        block="Operational Safety Management",
        icon="shield",
        requirements=[
            req(
                "R.1.1.2.6",
                "SAFE form en tareas no rutinarias",
                "Toda actividad no rutinaria, también de contratistas y proveedores, usa SAFE "
                "form, con foco en mantenimiento y en tareas de alto riesgo SIF.",
            ),
            req(
                "R.1.1.2.7",
                "Inventarios al día",
                "Hay inventarios actualizados de sustancias peligrosas, espacios confinados y "
                "sus equipos, máquinas fijas, torres de enfriamiento y condensadores "
                "evaporativos, equipos para trabajo en alturas, techos, equipos de transporte y "
                "herramientas eléctricas portátiles.",
            ),
            req(
                "R.1.1.2.8",
                "Los gerentes son dueños de la evaluación de riesgos",
                "Revisan las evaluaciones y SOP existentes, evalúan equipos y procesos nuevos "
                "como parte del MOC y actualizan las evaluaciones cuando aparecen peligros "
                "nuevos.",
            ),
            req(
                "R.1.1.2.9",
                "El FLTM conoce sus riesgos y controles",
                "El FLTM, contratistas y proveedores incluidos, sabe explicar los riesgos de su "
                "área o tarea y las medidas que los controlan.",
            ),
            req(
                "R.1.1.3.1",
                "Equipos de seguridad certificados",
                "Solo se usan equipos de seguridad certificados según normas ISO, IEC o "
                "nacionales equivalentes: válvulas de seguridad, paneles de alivio de explosión, "
                "detectores, cortinas de luz, PLC de seguridad, PPE, componentes eléctricos, "
                "herramientas manuales y equipos de izaje. Las brechas se cierran con un plan.",
            ),
            req(
                "R.1.1.3.2",
                "Sueño y estrategia de seguridad",
                "La planta define su sueño y estrategia de seguridad, alineados con la Zona y "
                "Global, y los convierte en programas, proyectos y planes de acción.",
            ),
            req(
                "R.1.1.5.1",
                "GTS para equipos nuevos y usados",
                "Las especificaciones técnicas globales (GTS) se aplican en la compra y puesta "
                "en marcha de equipos nuevos o de segunda mano, también si se trasladan entre "
                "plantas o dentro de la planta, y en edificios, áreas y procesos nuevos.",
            ),
            req(
                "R.1.1.8.4",
                "Lista de autorizados para permisos de trabajo",
                "Existe y está al día la lista de personas autorizadas en el proceso de "
                "permisos de trabajo.",
            ),
            req(
                "R.1.1.9.3",
                "Equipos de izaje en buen estado",
                "Todos los equipos de izaje (grúas, polipastos, eslingas, puntos de anclaje, "
                "entre otros) están inventariados, rotulados y ordenados (5S), con inspección "
                "formal al menos anual y revisión antes de cada uso.",
            ),
            req(
                "R.1.1.9.4",
                "Izajes no rutinarios de contratistas",
                "Tienen plan de seguridad y método de trabajo, también cerca de líneas "
                "eléctricas. Los contratistas están precalificados, inducidos, supervisados y "
                "aprueban una prueba básica.",
            ),
            req(
                "R.1.1.11.4",
                "Seguridad en el contrato con la agencia de temporales",
                "No hay temporales sin contrato. El contrato describe área, tareas y equipos, "
                "peligros y medidas preventivas, vigilancia de salud y competencias requeridas.",
            ),
            req(
                "R.1.1.12.1",
                "Trabajo en solitario",
                "Una evaluación identifica las tareas que se hacen en solitario y si es seguro "
                "hacerlas así. Los controles quedan en un SOP: comunicación, verificaciones "
                "periódicas, localización, alarmas de hombre caído o sin movimiento, formación, "
                "PPE y primeros auxilios.",
            ),
        ],
        objective=(
            "Aplicar las herramientas del nivel 1 para controlar el riesgo en las tareas del "
            "día a día."
        ),
        body=(
            "En el nivel 1 la planta ya no solo tiene procedimientos: los usa para controlar "
            "el riesgo todos los días.\n\n"
            "Lo que cambia para ti:\n\n"
            "* Toda tarea no rutinaria, sobre todo de mantenimiento, empieza con un SAFE form.\n"
            "* Debes poder explicar los riesgos de tu área y cómo se controlan.\n"
            "* Antes de usar un equipo de izaje lo revisas; además, tiene inspección formal "
            "anual.\n"
            "* Si trabajas solo, por ejemplo en una ronda nocturna, debe haber comunicación, "
            "verificaciones o alarmas definidas en un SOP."
        ),
    ),
    block_node(
        slug="n1-reporte-incidentes",
        title="Reporte de incidentes",
        description="24 horas, 7 días y Guardians.",
        block="Incident Reporting & Management",
        icon="file",
        requirements=[
            req(
                "R.1.2.1.3",
                "Notificación en 24 horas",
                "El gerente del área notifica en 24 horas a Seguridad de Zona y Global cada "
                "fatalidad, SIF real, TRI y SIF potencial. Las fatalidades y los SIF reales se "
                "informan de inmediato al VP de Supply de Zona y a los directores de Seguridad "
                "de Zona y Global.",
            ),
            req(
                "R.1.2.1.4",
                "Investigación en 7 días",
                "Cada fatalidad, SIF real, TRI y SIF potencial tiene investigación, análisis de "
                "causa raíz (RCA) y plan de acción en 7 días, con participación del FLTM y del "
                "afectado si es posible. Para FAI y precursores SIF se usa al menos el Problem "
                "Terminator o una herramienta de Zona similar.",
            ),
            req(
                "R.1.2.1.5",
                "Seguimiento de las acciones del RCA",
                "Las acciones correctivas se definen con la jerarquía de controles, cubren los "
                "bloques VPO relevantes y se siguen hasta cerrarse.",
            ),
            req(
                "R.1.2.1.6",
                "Casi accidentes y condiciones inseguras en Guardians",
                "Casi accidentes, condiciones y comportamientos inseguros y lesiones de primeros "
                "auxilios (FAI) se reportan en un sistema auditable. Guardians es la herramienta "
                "oficial donde ya está implementada.",
            ),
        ],
        objective="Conocer los plazos de notificación e investigación y qué se reporta en Guardians.",
        body=(
            "En el nivel 1 el reporte deja de ser solo un registro: se convierte en "
            "aprendizaje con plazos claros.\n\n"
            "* 24 horas: notificación de fatalidades, SIF reales y potenciales y TRI.\n"
            "* 7 días: investigación, análisis de causa raíz (RCA) y plan de acción.\n"
            "* Las acciones se definen con la jerarquía de controles y se siguen hasta "
            "cerrarse.\n\n"
            "Para ti lo más importante: los casi accidentes, las condiciones inseguras y los "
            "comportamientos de riesgo también se reportan en Guardians. Cada reporte puede "
            "evitar una lesión."
        ),
    ),
    block_node(
        slug="n1-procesos-alto-riesgo",
        title="Procesos de alto riesgo",
        description="Toolkits, NH3, vapor, presión e inflamables.",
        block="High Risk Processes Management",
        icon="flame",
        requirements=[
            req(
                "R.1.3.1.6",
                "Señalización de procesos de alto riesgo",
                "Tuberías, equipos y áreas de NH3, polvo explosivo, vapor y HPHW, electricidad, "
                "recipientes a presión (con número de equipo y fecha de calibración de PRV y "
                "VRV), inflamables y CO2/N2 están identificados, con información de peligros, "
                "medidas y respuesta a emergencias.",
            ),
            req(
                "R.1.3.1.7",
                "Toolkit PSM NH3 en 60% o más",
                "El toolkit de gestión de seguridad de procesos con amoníaco está en al menos "
                "60%, con un plan con fechas (glidepath) para cerrar brechas.",
            ),
            req(
                "R.1.3.1.9",
                "Toolkit DEPSM en 60% o más",
                "El toolkit de prevención de explosiones de polvo está en al menos 60%, con "
                "glidepath para cerrar brechas.",
            ),
            req(
                "R.1.3.1.11",
                "Toolkit SSM en 60% o más",
                "El toolkit de gestión de seguridad en vapor está en al menos 60%, con glidepath "
                "para cerrar brechas.",
            ),
            req(
                "R.1.3.1.12",
                "Toolkit ESM en 60% o más",
                "El toolkit de gestión de seguridad eléctrica está en al menos 60%, con "
                "glidepath para cerrar brechas.",
            ),
            req(
                "R.1.3.1.13",
                "Plan de acción de procesos de alto riesgo",
                "Un plan único cubre PSM NH3, DEPSM, SSM, ESM, recipientes a presión y CO2/N2, a "
                "partir de evaluaciones de riesgo, incidentes, RCA, auditorías, cambios legales, "
                "MOC y evaluaciones VPO, con glidepaths validados por la Zona.",
            ),
            req(
                "R.1.3.2.4",
                "Equipos de NH3 en reserva y fuera de servicio",
                "Los equipos de reserva se evalúan, monitorean, inspeccionan y mantienen. Los que "
                "quedan fuera de servicio se vacían por completo, se desconectan mecánica y "
                "eléctricamente y se señalizan.",
            ),
            req(
                "R.1.3.2.7",
                "Integridad mecánica del sistema de NH3",
                "Hay un programa de inspección, pruebas, mantenimiento preventivo e integridad "
                "mecánica, cargado en el sistema de órdenes de trabajo, para mantener el sistema "
                "sin fugas y en condición segura.",
            ),
            req(
                "R.1.3.3.1",
                "Evaluación de riesgo de explosión de polvo",
                "Un quick-scan identifica si se procesan materiales que puedan generar "
                "explosiones de polvo. Si es así (siempre con cereales o biomasa), se hace una "
                "evaluación a fondo con PHA y se controla con la jerarquía de controles.",
            ),
            req(
                "R.1.3.4.1",
                "Evaluación de riesgos y PHA de vapor, HPHW y condensado",
                "Los sistemas de vapor, agua caliente a alta presión y condensado tienen "
                "evaluación de riesgos con PHA, incluida la prevención del golpe de ariete, y "
                "controles según GTS y el toolkit.",
            ),
            req(
                "R.1.3.4.2",
                "Documentación y SOP de vapor",
                "La documentación de equipos, áreas y medidas de seguridad está al día y "
                "accesible, con SOP de operación, inspección, mantenimiento y prevención del "
                "golpe de ariete.",
            ),
            req(
                "R.1.3.6.3",
                "Recipientes a presión según la norma más estricta",
                "Recipientes, PRV, VRV y sistemas de seguridad se inspeccionan, calibran o "
                "certifican y mantienen según la ley o los requisitos de AB InBev, lo que sea "
                "más estricto, con los planes en el sistema de órdenes de trabajo.",
            ),
            req(
                "R.1.3.6.4",
                "Evaluación de riesgos y PHA de recipientes a presión",
                "Identifica los recipientes a presión y los que pueden quedar presurizados por "
                "accidente, cubre también el vacío y la implosión, y demuestra que las PRV, VRV "
                "y demás protecciones evitan la explosión o implosión.",
            ),
            req(
                "R.1.3.7.1",
                "Evaluación de gases y líquidos inflamables (FCGL)",
                "Un quick-scan identifica si hay FCGL; si los hay, se evalúan a fondo (con PHA "
                "para tanques a granel). Un líquido es inflamable si su punto de inflamación no "
                "supera 37,8 °C (100 °F) y combustible si es igual o mayor. Siempre aplica al NH3.",
            ),
            req(
                "R.1.3.7.2",
                "Documentación y SOP de FCGL",
                "La documentación de tanques, áreas, procesos y medidas de seguridad de FCGL "
                "está al día y accesible, con SOP de operación, inspección y mantenimiento.",
            ),
            req(
                "R.1.3.7.4",
                "Mantenimiento preventivo de FCGL",
                "Hay un programa de inspección, pruebas y mantenimiento preventivo de los "
                "equipos de FCGL, cargado en el sistema de órdenes de trabajo.",
            ),
            req(
                "R.1.3.8.2",
                "Documentación y SOP de CO2 y N2",
                "La documentación de tanques, áreas, procesos y medidas de seguridad de CO2/N2 "
                "está al día y accesible, con SOP de operación, inspección y mantenimiento.",
            ),
            req(
                "R.1.3.8.4",
                "Mantenimiento preventivo de CO2 y N2",
                "Hay un programa de inspección, pruebas y mantenimiento preventivo de los "
                "equipos de CO2/N2, cargado en el sistema de órdenes de trabajo.",
            ),
        ],
        objective="Entender cómo VPO controla los procesos de alto riesgo de Utilities en el nivel 1.",
        body=(
            "Este es el bloque más grande del nivel 1 y el más cercano a Utilities.\n\n"
            "VPO mide cada proceso de alto riesgo con un toolkit: PSM NH3 (amoníaco), DEPSM "
            "(explosión de polvo), SSM (vapor) y ESM (seguridad eléctrica). En el nivel 1 cada "
            "uno debe estar en 60% o más, con un plan para cerrar las brechas.\n\n"
            "En tu trabajo diario esto se traduce en:\n\n"
            "* Tuberías, equipos y áreas señalizados con sus peligros y qué hacer en una "
            "emergencia.\n"
            "* Equipos de NH3 fuera de servicio vaciados, desconectados y señalizados.\n"
            "* Prevención del golpe de ariete en vapor y condensado.\n"
            "* Recipientes a presión gestionados según la norma más estricta: la ley o "
            "AB InBev."
        ),
    ),
    block_node(
        slug="n1-transporte-planta",
        title="Transporte en planta",
        description="Inspección preoperacional y estanterías.",
        block="Workplace Transport",
        icon="truck",
        requirements=[
            req(
                "R.1.4.1.15",
                "Inspección preoperacional de equipos de transporte",
                "Antes de cada turno se inspeccionan y registran los equipos motorizados "
                "(camiones, montacargas, apiladores, transpaletas eléctricas, barredoras, "
                "carritos de golf) y los no motorizados (transpaletas manuales, carretillas).",
            ),
            req(
                "R.1.4.1.21",
                "Estanterías seguras y MOC",
                "Las estanterías se inspeccionan y cumplen las GTS. Hay MOC cuando se modifican, "
                "cuando cambia su capacidad de carga o tras reparar daños importantes.",
            ),
        ],
        objective="Aplicar la inspección preoperacional y el MOC de estanterías.",
        body=(
            "El nivel 1 agrega dos controles que evitan accidentes antes de que empiecen:\n\n"
            "* Inspección preoperacional: antes de cada turno se revisa y registra cada equipo "
            "de transporte, con o sin motor. Una transpaleta manual con una rueda dañada "
            "también puede lesionar a alguien.\n"
            "* Estanterías seguras: se inspeccionan, y cualquier cambio en su estructura o en "
            "el peso que soportan pasa por MOC.\n\n"
            "Si un equipo no pasó la inspección, no lo operes: repórtalo."
        ),
    ),
    block_node(
        slug="n1-sustancias-peligrosas",
        title="Sustancias peligrosas",
        description="SDS, compatibilidad, tanques y legionela.",
        block="Hazardous Substances",
        icon="flask",
        requirements=[
            req(
                "R.1.6.1.6",
                "Evaluación de riesgos de sustancias peligrosas",
                "Hay una evaluación de riesgos de seguridad y salud apoyada en el toolkit de "
                "gestión de químicos, con un plan de acción basado en la jerarquía de controles "
                "y las GTS.",
            ),
            req(
                "R.1.6.1.7",
                "Roles y formación en sustancias peligrosas",
                "Reciben formación con SKAP quienes almacenan, transportan, usan o mantienen "
                "sistemas con químicos, quienes trabajan expuestos y las brigadas, 3PL y "
                "contratistas incluidos: SOP, SDS, alarmas, manipulación, peligros, ambiente y "
                "emergencias. Refuerzo al menos cada 3 años.",
            ),
            req(
                "R.1.6.1.8",
                "SDS y fichas de una página",
                "Hay SDS al día de todas las sustancias, resumidas en fichas de una página "
                "disponibles en el cuarto de equipo, el puesto de trabajo y el punto de uso, y "
                "accesibles para primeros auxilios, brigadas, servicio médico y emergencias "
                "externas.",
            ),
            req(
                "R.1.6.1.9",
                "El FLTM conoce los peligros de sus sustancias",
                "El FLTM sabe explicar los peligros de las sustancias de su área y cómo se "
                "controlan, aplica los SOP y usa el PPE requerido, también con diluidos.",
            ),
            req(
                "R.1.6.1.10",
                "Matriz de compatibilidad",
                "Un estudio de compatibilidad de todas las sustancias, cilindros de gas "
                "incluidos, da lugar a una matriz publicada en cada lugar donde se guarda más "
                "de una sustancia, con solo las que hay allí.",
            ),
            req(
                "R.1.6.1.11",
                "Almacenamiento seguro",
                "Condiciones que evitan congelamiento o sobrecalentamiento, acceso solo para "
                "autorizados, detección y extinción de incendios, aditivos alimentarios aparte, "
                "oxidantes solo en estibas plásticas y con alivio de presión, ventilación y "
                "contención secundaria (IBC de doble pared o diques con detección de fugas y "
                "drenaje con candado).",
            ),
            req(
                "R.1.6.1.12",
                "Tanques a granel",
                "Tienen sensores de nivel alto y bajo, rebose hacia un lugar seguro, lavador de "
                "gases si el producto lo requiere, contención secundaria y ventilación. Si están "
                "presurizados, cumplen la norma de recipientes a presión y tienen válvulas de "
                "seguridad.",
            ),
            req(
                "R.1.6.1.13",
                "Cargue y descargue de sustancias peligrosas",
                "Se hace con análisis de riesgo de la tarea (JHA), LOTOTO del camión o cisterna, "
                "montacarguistas formados y autorizados, y áreas dedicadas según el toolkit de "
                "químicos.",
            ),
            req(
                "R.1.6.1.15",
                "Señalización de sustancias peligrosas",
                "Tuberías y equipos con sustancias peligrosas están señalizados, con peligros, "
                "medidas preventivas y respuesta a emergencias.",
            ),
            req(
                "R.1.6.1.16",
                "Control de legionela",
                "Todas las torres de enfriamiento y condensadores evaporativos, incluso los más "
                "pequeños, están inventariados y tienen un SOP con muestreo de legionela, "
                "tratamiento de agua, limpieza, mantenimiento y respuesta ante niveles altos.",
            ),
            req(
                "R.1.6.1.17",
                "Control de asbesto",
                "Se identifica todo el asbesto y su estado. El que representa riesgo se retira "
                "o se controla, los materiales se rotulan y no se instala asbesto nuevo salvo "
                "aplicaciones sin alternativa.",
            ),
            req(
                "R.1.6.1.18",
                "Control de PCB",
                "Se revisan transformadores, capacitores y demás equipos eléctricos con aceite "
                "para detectar PCB (askarel), con inventario y plan de reemplazo según la ley.",
            ),
        ],
        objective="Aplicar las reglas VPO de almacenamiento, compatibilidad y control de químicos.",
        body=(
            "En el nivel 1 el manejo de químicos pasa de lo básico a lo detallado: dónde se "
            "guardan, con qué se pueden guardar y cómo se cargan y descargan.\n\n"
            "Puntos clave para Utilities:\n\n"
            "* Cada sustancia tiene su SDS resumida en una ficha de una página en tu puesto.\n"
            "* Las sustancias incompatibles nunca se guardan juntas: revisa la matriz de "
            "compatibilidad.\n"
            "* Los tanques a granel tienen sensores de nivel, rebose seguro y contención "
            "secundaria.\n"
            "* Las torres de enfriamiento y condensadores evaporativos tienen control de "
            "legionela.\n"
            "* Los transformadores con aceite se revisan para detectar PCB."
        ),
    ),
    block_node(
        slug="n1-lototo",
        title="LOTOTO y máquinas",
        description="Procedimientos para equipos críticos.",
        block="LOTOTO and Machine Safety",
        icon="lock",
        requirements=[
            req(
                "R.1.7.1.6",
                "SOP específicos de bloqueo para equipos críticos",
                "Hay procedimientos detallados de SAM, LOTOTO y jogging para equipos críticos, "
                "entre ellos los de amoníaco, vapor, HWHP y condensado, CO2 y N2, alta tensión, "
                "todos los espacios confinados y cualquier equipo que se bloquee con frecuencia.",
            ),
        ],
        objective="Reconocer qué equipos de Utilities necesitan un procedimiento de bloqueo propio.",
        body=(
            "El SOP general de LOTOTO dice cómo bloquear. Pero un compresor de amoníaco no se "
            "bloquea igual que una bomba de agua.\n\n"
            "Por eso VPO exige procedimientos específicos y detallados para los equipos "
            "críticos. En Utilities eso incluye:\n\n"
            "* Recipientes y equipos con amoníaco.\n"
            "* Vapor, agua caliente a alta presión y condensado.\n"
            "* CO2 y N2.\n"
            "* Equipos eléctricos de alta tensión.\n"
            "* Todos los espacios confinados.\n\n"
            "Antes de bloquear un equipo crítico, busca su procedimiento específico."
        ),
    ),
    block_node(
        slug="n1-trabajo-alturas",
        title="Trabajo en alturas",
        description="Equipos inventariados e inspeccionados.",
        block="Working at heights",
        icon="mountain",
        requirements=[
            req(
                "R.1.8.1.11",
                "Equipos para trabajo en alturas en buen estado",
                "Hay inventario de equipos para trabajo en alturas y de techos (seguros e "
                "inseguros). Los equipos están rotulados y ordenados (5S), con inspección formal "
                "al menos anual y revisión antes de cada uso, y los techos están señalizados.",
            ),
        ],
        objective="Verificar tu equipo para trabajo en alturas antes de usarlo.",
        body=(
            "Un arnés vencido o una eslinga desgastada pueden fallar justo cuando más los "
            "necesitas.\n\n"
            "VPO exige que los equipos para trabajo en alturas estén inventariados, rotulados, "
            "bien guardados y con inspección formal al menos una vez al año. Además, cada "
            "persona los revisa antes de usarlos.\n\n"
            "Los techos también están inventariados y señalizados como seguros o inseguros."
        ),
    ),
    block_node(
        slug="n1-espacios-confinados",
        title="Espacios confinados",
        description="Medidores, ventilación y rescate.",
        block="Confined Spaces",
        icon="cylinder",
        requirements=[
            req(
                "R.1.10.1.5",
                "Equipos para espacios confinados en buen estado",
                "Hay inventario de equipos de entrada y monitoreo (medidores, ventilación, "
                "comunicación, trípodes, rescate), rotulados y ordenados (5S), con inspección "
                "formal anual, revisión antes de cada uso y calibración de los medidores de "
                "atmósfera según el fabricante.",
            ),
        ],
        objective="Asegurar que los equipos de entrada y rescate estén listos.",
        body=(
            "Dentro de un espacio confinado dependes de tus equipos: el medidor que avisa si "
            "falta oxígeno o hay gases, la ventilación, el radio y el equipo de rescate.\n\n"
            "Por eso VPO pide que estén inventariados, en orden, con inspección formal al menos "
            "anual, revisados antes de cada uso y, en el caso de los medidores de atmósfera, "
            "calibrados según el fabricante."
        ),
    ),
    block_node(
        slug="n1-emergencias",
        title="Emergencias",
        description="Simulacros, incluido el de NH3.",
        block="Emergency Preparedness and Response",
        icon="siren",
        requirements=[
            req(
                "R.1.11.1.4",
                "Simulacros de emergencia",
                "El plan de emergencias se prueba y documenta con simulacros prácticos, como los "
                "de incendio. Las plantas con refrigeración por amoníaco hacen al menos un "
                "simulacro de fuga de NH3 al año.",
            ),
        ],
        objective="Entender para qué sirven los simulacros y cuál es obligatorio en Utilities.",
        body=(
            "Un plan de emergencias que nunca se practica es solo un papel. Los simulacros "
            "muestran si las alarmas funcionan, si la gente sabe a dónde ir y si los cortes de "
            "energía se hacen a tiempo.\n\n"
            "Para Utilities hay un requisito específico: si la planta usa amoníaco como "
            "refrigerante, hace al menos un simulacro de fuga de NH3 al año."
        ),
    ),
    block_node(
        slug="n1-contratistas",
        title="Contratistas",
        description="Método de trabajo y monitoreo.",
        block="Contractor and Service Providers Management",
        icon="users",
        requirements=[
            req(
                "R.1.12.1.11",
                "Plan de seguridad y método de trabajo (paso 3)",
                "La planta valida el plan de seguridad y el método de trabajo de todo trabajo de "
                "contratistas, tanto servicios como proyectos. El método describe en detalle los "
                "peligros y controles de cada tarea.",
            ),
            req(
                "R.1.12.1.12",
                "Contratistas en las rutinas de monitoreo",
                "La seguridad de contratistas y proveedores forma parte de las rutinas de "
                "monitoreo de seguridad.",
            ),
        ],
        objective="Saber qué se revisa antes y durante el trabajo de un contratista.",
        body=(
            "Antes de que un contratista toque un equipo, la planta revisa su plan: qué va a "
            "hacer, qué peligros tiene cada tarea y cómo los va a controlar. Eso es el método "
            "de trabajo (method statement), paso 3 de la gestión de contratistas.\n\n"
            "Y una vez empieza el trabajo, los contratistas entran en las rutinas de monitoreo "
            "de seguridad, igual que el personal propio."
        ),
    ),
    block_node(
        slug="n1-salud-ocupacional",
        title="Salud ocupacional",
        description="Peligros para la salud, también de contratistas.",
        block="Occupational Health",
        icon="health",
        requirements=[
            req(
                "R.1.13.1.1",
                "Roles y formación en salud ocupacional",
                "Empleados y contratistas reciben formación con SKAP sobre los peligros para la "
                "salud y cómo controlarlos, con refuerzo al menos cada 3 años.",
            ),
            req(
                "R.1.13.1.2",
                "La salud ocupacional incluye a contratistas",
                "La evaluación de riesgos para la salud (OHHRA) y los programas cubren a "
                "contratistas en dos niveles: los peligros de la planta, como ruido o químicos, "
                "y los de su tarea, como humos de soldadura o fibras de asbesto.",
            ),
            req(
                "R.1.13.1.4",
                "El FLTM conoce los peligros para la salud",
                "El FLTM conoce los peligros para la salud de su trabajo y participa en "
                "controlarlos.",
            ),
        ],
        objective="Reconocer los peligros para la salud en Utilities y a quién cubren los programas.",
        body=(
            "Los accidentes se ven en el momento. Las enfermedades ocupacionales tardan años: "
            "pérdida auditiva por ruido, problemas respiratorios por químicos.\n\n"
            "En Utilities los peligros para la salud más comunes son el ruido de compresores y "
            "calderas, la exposición a químicos y el calor.\n\n"
            "VPO pide que conozcas esos peligros y participes en controlarlos, y que los "
            "contratistas estén cubiertos tanto frente a los peligros de la planta como a los "
            "de su propia tarea."
        ),
    ),
    block_node(
        slug="n1-gestion-sif",
        title="Gestión SIF",
        description="Reporte de precursores SIF.",
        block="SIF Management",
        icon="warning",
        requirements=[
            req(
                "R.1.14.1.2",
                "Reporte de precursores SIF",
                "La planta registra e investiga los precursores SIF en todas sus áreas, y los "
                "equipos del FLTM los analizan y toman acciones para evitar accidentes.",
            ),
        ],
        objective="Reconocer un precursor SIF y saber qué hacer con él.",
        body=(
            "Un precursor SIF es una situación de alto riesgo en la que los controles fallaron "
            "o no estaban, aunque esta vez nadie se lastimara.\n\n"
            "Son las señales de alerta más valiosas: detrás de una lesión grave casi siempre "
            "hubo precursores que nadie reportó.\n\n"
            "En el nivel 1 VPO exige registrarlos, investigarlos y que los equipos de trabajo "
            "los analicen para tomar acciones."
        ),
    ),
    block_node(
        slug="n1-cultura-seguridad",
        title="Cultura de seguridad",
        description="Seguridad territorial y autoridad para detener.",
        block="Behavioral Safety Culture",
        icon="handshake",
        requirements=[
            req(
                "R.1.17.3.1",
                "Estrategia de seguridad territorial",
                "La planta define sus territorios y dueños, implementa los prerrequisitos de "
                "seguridad territorial en todos y tiene un plan para subir su nivel. Aplica "
                "también a contratistas con territorio propio, como el taller de montacargas.",
            ),
            req(
                "R.1.17.3.3",
                "El FLTM acompaña a contratistas en su territorio",
                "El FLTM es compañero de contratistas y proveedores en su área: los orienta, les "
                "explica los SOP y vigila que trabajen seguro (LOTOTO, químicos, permisos, PPE). "
                "Todo empleado reporta y corrige un trabajo inseguro y puede detenerlo.",
            ),
            req(
                "R.1.17.4.1",
                "Reconocimiento y sanción",
                "Hay un SOP de reconocimiento y sanción, percibido como justo, para asegurar el "
                "cumplimiento de la política y el sueño de seguridad.",
            ),
            req(
                "R.1.17.9.1",
                "Taller de seguridad basada en el comportamiento",
                "El 100% de los empleados, aprendices incluidos, participa en el taller. El "
                "personal nuevo lo hace en sus primeros 6 meses y hay refuerzo al menos cada 3 "
                "años.",
            ),
        ],
        objective="Ejercer como dueño de tu territorio y usar tu autoridad para detener un trabajo.",
        body=(
            "La seguridad territorial significa que cada área tiene un dueño que la conoce "
            "mejor que nadie y la cuida.\n\n"
            "Si Utilities es tu territorio, VPO espera que:\n\n"
            "* Acompañes a los contratistas en tu área: cómo moverse y qué reglas aplican.\n"
            "* Vigiles que trabajen seguro, con foco en LOTOTO, químicos, permisos y PPE.\n"
            "* Detengas el trabajo si ves un riesgo para alguien: tienes la autoridad y la "
            "responsabilidad de hacerlo.\n\n"
            "Además, todos pasan por el taller de seguridad basada en el comportamiento; el "
            "personal nuevo, en sus primeros 6 meses."
        ),
    ),
    block_node(
        slug="n1-cumplimiento-legal",
        title="Cumplimiento legal",
        description="Cambios legales y permisos al día.",
        block="Facility compliance",
        icon="scale",
        requirements=[
            req(
                "R.1.18.1.2",
                "Seguimiento a cambios legales",
                "Hay un sistema para seguir las actualizaciones y cambios de los requisitos "
                "legales de seguridad y salud.",
            ),
            req(
                "R.1.18.1.3",
                "Permisos y licencias en el tracker global",
                "Los permisos y licencias de la planta están registrados en el Global Permits "
                "and Licenses tracker.",
            ),
            req(
                "R.1.18.1.4",
                "Renovación oportuna de permisos y licencias",
                "Las renovaciones se piden a tiempo, de modo que no haya permisos ni licencias "
                "vencidos.",
            ),
        ],
        objective="Entender cómo la planta mantiene al día sus obligaciones legales.",
        body=(
            "En el nivel 0 la planta identifica qué leyes le aplican. En el nivel 1 se asegura "
            "de que ese conocimiento no se quede viejo:\n\n"
            "* Sigue los cambios en la legislación de seguridad y salud.\n"
            "* Registra sus permisos y licencias en el tracker global.\n"
            "* Pide las renovaciones a tiempo para que nunca haya un permiso o licencia "
            "vencido.\n\n"
            "Un permiso vencido puede obligar a parar un equipo o un área. Si ves una "
            "certificación o licencia a punto de vencer, avisa."
        ),
    ),
]


ZONE = zone(
    level=1,
    name="Control del riesgo",
    description=(
        "Nivel 1 de VPO: los procesos funcionan y se controlan. Toolkits de alto riesgo, SAFE "
        "form, investigación de incidentes, químicos y seguridad territorial."
    ),
    theme="sky",
    icon="gauge",
    nodes=NODES,
)
