"""Nivel 0 de madurez VPO (Safety / Utilities): los cimientos."""

from app.seed.vpo.builder import block_node, req, zone

NODES = [
    block_node(
        slug="n0-seguridad-operacional",
        title="Seguridad operacional",
        description="Riesgos, PPE, permisos, izajes y temporales.",
        block="Operational Safety Management",
        icon="shield",
        requirements=[
            req(
                "R.1.1.2.1",
                "SOP de evaluación de riesgos implementado",
                "La planta tiene un procedimiento que define la metodología y el proceso de "
                "evaluación de riesgos, vinculado con el MOC, el mapa de procesos y los "
                "inventarios. Cubre tareas (JHA), instalaciones, máquinas y factores humanos "
                "y psicosociales.",
            ),
            req(
                "R.1.1.2.2",
                "Roles y formación en evaluación de riesgos",
                "Los roles y responsabilidades están definidos y hay un programa de formación "
                "apoyado en SKAP. El refuerzo se hace al menos cada 3 años.",
            ),
            req(
                "R.1.1.2.3",
                "Estrategia de evaluación de riesgos",
                "Hay un plan para que todas las actividades, áreas y tareas queden evaluadas "
                "según el SOP, incluidos los factores humanos y psicosociales.",
            ),
            req(
                "R.1.1.6.1",
                "Programa de PPE",
                "Los PPE requeridos salen de la evaluación de riesgos y de la ley. Mínimos "
                "globales: calzado de seguridad en producción, chaleco reflectivo en logística, "
                "gafas donde hay vidrio y protección auditiva sobre el límite legal. El programa "
                "cubre selección, entrega, reposición, inspección y señalización.",
            ),
            req(
                "R.1.1.6.2",
                "Programa de CPE",
                "La protección colectiva (CPE) también se define por evaluación de riesgos y "
                "tiene proceso de selección, inspección, mantenimiento y señalización.",
            ),
            req(
                "R.1.1.8.1",
                "SOP de permisos de trabajo",
                "Define cuándo se necesita permiso general (siempre con contratistas) y cuándo "
                "uno específico para tareas de alto riesgo: alturas sobre 2 m, izajes no "
                "rutinarios, espacios confinados, trabajo eléctrico energizado o de alta "
                "tensión, trabajo en caliente en zonas explosivas, tareas no rutinarias en NH3, "
                "recipientes a presión, vapor y condensado, sustancias peligrosas, demolición y "
                "excavación. Incluye el permiso de apertura de línea para equipos con químicos, "
                "también diluidos como los del CIP.",
            ),
            req(
                "R.1.1.8.2",
                "Roles y formación en permisos de trabajo",
                "Formación avanzada para quienes emiten permisos y básica para todo el FLTM, "
                "contratistas y proveedores incluidos. Refuerzo al menos cada 3 años.",
            ),
            req(
                "R.1.1.9.1",
                "SOP de izajes",
                "Un procedimiento describe en detalle cómo controlar los riesgos de los izajes "
                "rutinarios y no rutinarios.",
            ),
            req(
                "R.1.1.9.2",
                "Roles y formación en izajes",
                "Los roles de izaje están definidos y la formación se verifica con SKAP y con "
                "los registros de entrenamiento.",
            ),
            req(
                "R.1.1.11.1",
                "Supervisión de trabajadores temporales",
                "Los temporales se supervisan con el monitoreo de seguridad rutinario, el "
                "sistema de compañero (buddy) y la seguridad territorial.",
            ),
            req(
                "R.1.1.11.2",
                "Formación de trabajadores temporales",
                "Reciben inducción general y formación por tarea, y solo se asignan a las "
                "tareas para las que fueron formados. Si la tarea tiene SKAP, este define la "
                "formación; si no, se hace una evaluación de riesgos.",
            ),
            req(
                "R.1.1.11.3",
                "MOC al emplear temporales",
                "Los cambios en la organización, la dotación o la forma de trabajar pasan por "
                "MOC. No hace falta MOC solo por cubrir una vacante que ya existe.",
            ),
        ],
        objective=(
            "Conocer la base de la seguridad operacional VPO: evaluación de riesgos, PPE, "
            "permisos, izajes y trabajadores temporales."
        ),
        body=(
            "Este bloque es la base de todo lo demás: identificar los riesgos antes de "
            "trabajar, protegerte con el equipo correcto y no empezar una tarea peligrosa "
            "sin permiso.\n\n"
            "Tres ideas para tu día a día:\n\n"
            "* Toda tarea debe estar evaluada. Si notas un peligro nuevo, repórtalo para "
            "que se actualice la evaluación.\n"
            "* Los PPE no son opcionales: salen de la evaluación de riesgos y de la ley.\n"
            "* Las tareas de alto riesgo (alturas, izajes no rutinarios, espacios "
            "confinados, energía eléctrica, NH3, vapor, químicos) siempre llevan permiso "
            "específico.\n\n"
            "Si trabajas con personal temporal, recuerda que solo puede hacer las tareas "
            "para las que fue formado."
        ),
    ),
    block_node(
        slug="n0-reporte-incidentes",
        title="Reporte de incidentes",
        description="Qué se registra y en qué plazo.",
        block="Incident Reporting & Management",
        icon="file",
        requirements=[
            req(
                "R.1.2.1.1",
                "Registro en la herramienta global de incidentes",
                "Fatalidades, SIF reales y potenciales, precursores SIF, TRI y enfermedades "
                "ocupacionales se registran en la herramienta global como máximo 3 días después "
                "del evento, con los días perdidos (LTI) o restringidos (MDI) correctos. Aplica "
                "a todo lo que ocurre en la planta y en las bodegas T1 conectadas.",
            ),
        ],
        objective="Saber qué eventos se registran en la herramienta global y en qué plazo.",
        body=(
            "Un incidente que no se reporta no se puede investigar, y lo que no se investiga "
            "se repite.\n\n"
            "VPO exige que los eventos graves queden en la herramienta global de reporte de "
            "incidentes en un plazo máximo de 3 días:\n\n"
            "* Fatalidades y SIF (lesiones graves o fatales), reales o potenciales.\n"
            "* Precursores SIF: situaciones que pudieron terminar en una lesión grave.\n"
            "* TRI (lesiones registrables) y enfermedades ocupacionales.\n\n"
            "Tu parte empieza antes: avisa de inmediato a tu líder cuando pase algo, aunque "
            "parezca menor."
        ),
    ),
    block_node(
        slug="n0-procesos-alto-riesgo",
        title="Procesos de alto riesgo",
        description="NH3, vapor, electricidad, presión, CO2 y N2.",
        block="High Risk Processes Management",
        icon="flame",
        requirements=[
            req(
                "R.1.3.1.1",
                "Contratistas precalificados en procesos de alto riesgo",
                "Quien trabaje en NH3, equipos con riesgo de explosión de polvo, vapor y agua "
                "caliente a alta presión (HPHW), sistemas eléctricos, recipientes a presión, "
                "gases y líquidos inflamables (FCGL) o CO2/N2 debe estar precalificado, "
                "inducido y supervisado, y aprobar antes una prueba básica de conocimiento.",
            ),
            req(
                "R.1.3.1.2",
                "Permisos y SAFE form en trabajos no rutinarios",
                "Todo trabajo no rutinario en estos procesos lleva permiso específico, permiso "
                "de apertura de línea y equipo cuando aplica, y SAFE form.",
            ),
            req(
                "R.1.3.1.3",
                "MOC en procesos de alto riesgo",
                "Todo cambio, grande o pequeño y también de automatización, se identifica, "
                "evalúa, autoriza y documenta con MOC. La única excepción es el reemplazo "
                "idéntico (replacement in kind).",
            ),
            req(
                "R.1.3.1.4",
                "Plan de emergencias para procesos de alto riesgo",
                "Hay un plan actualizado, comunicado y practicado con simulacros para fugas de "
                "amoníaco, explosiones de polvo, fugas de vapor, incidentes eléctricos, "
                "explosión o implosión de recipientes, incendios de inflamables y liberación "
                "de CO2/N2.",
            ),
            req(
                "R.1.3.1.5",
                "Roles y formación en procesos de alto riesgo",
                "Operadores, técnicos, personal expuesto, PTE o coordinador PSM, brigadas y "
                "líderes tienen roles definidos y formación con SKAP, con refuerzo al menos "
                "cada 3 años.",
            ),
            req(
                "R.1.3.2.2",
                "PPE, detectores y comunicación en NH3",
                "Donde hay refrigeración con amoníaco hay PPE adecuado, detectores portátiles "
                "o personales de NH3, radios de dos vías y CPE como duchas de emergencia y "
                "lavaojos.",
            ),
            req(
                "R.1.3.5.1",
                "Permiso eléctrico específico",
                "Todo trabajo con circuitos energizados o de alta tensión requiere evaluación "
                "de riesgos y un permiso de trabajo eléctrico energizado validado por el ES "
                "Manager y el gerente eléctrico de la planta, y por ES y E&F de Zona.",
            ),
            req(
                "R.1.3.6.1",
                "Inventario de recipientes a presión, PRV y VRV",
                "Está al día el inventario de recipientes a presión, válvulas de alivio de "
                "presión (PRV) y de vacío (VRV), incluidos los discos de ruptura.",
            ),
            req(
                "R.1.3.6.2",
                "Recipientes a presión inspeccionados y certificados",
                "Recipientes, PRV, VRV y demás sistemas de seguridad se inspeccionan, calibran "
                "o certifican y mantienen según la ley, con los planes cargados en el sistema "
                "de órdenes de trabajo (SAP u otro).",
            ),
            req(
                "R.1.3.8.1",
                "Evaluación rápida de exposición a CO2 y N2",
                "Un quick-scan determina si hay riesgo de exposición a niveles altos de CO2 o "
                "N2. Si lo hay, se evalúa a fondo, se monitorea y se controla con la jerarquía "
                "de controles.",
            ),
        ],
        objective=(
            "Reconocer los procesos de alto riesgo de Utilities y las reglas básicas para "
            "intervenirlos."
        ),
        body=(
            "En Utilities convives con los procesos de mayor riesgo de la cervecería: "
            "amoníaco, vapor, electricidad, recipientes a presión, CO2 y N2.\n\n"
            "VPO los gestiona con reglas que no se negocian:\n\n"
            "* Nadie los interviene sin estar calificado. Los contratistas, además, aprueban "
            "una prueba básica antes de entrar.\n"
            "* Todo trabajo no rutinario lleva permiso específico y SAFE form.\n"
            "* Todo cambio pasa por MOC, salvo el reemplazo por una pieza idéntica.\n"
            "* Cerca del amoníaco llevas detector personal y radio, y sabes dónde están la "
            "ducha y el lavaojos.\n\n"
            "Los recipientes a presión y sus válvulas de alivio están inventariados y con "
            "inspección vigente."
        ),
    ),
    block_node(
        slug="n0-transporte-planta",
        title="Transporte en planta",
        description="Peatones, montacargas y camiones.",
        block="Workplace Transport",
        icon="truck",
        requirements=[
            req(
                "R.1.4.1.3",
                "Reglas de operación de equipos de transporte",
                "Hay reglas escritas para equipos motorizados y no motorizados: respetar flujos "
                "y velocidades, pitar y extremar la precaución en cruces, contacto visual, "
                "cinturón, nada de celular al conducir, respetar zonas rojas, estacionar en el "
                "sitio designado, inspección de 360°, conducir en reversa si la carga tapa la "
                "vista y respetar la regla de 1 metro.",
            ),
            req(
                "R.1.4.1.7",
                "Roles y formación en transporte interno",
                "Formación con SKAP para conductores, quienes cargan baterías o combustible, "
                "aseo, señaleros, almacenistas y técnicos de bodega, con refuerzo al menos cada "
                "3 años.",
            ),
            req(
                "R.1.4.1.8",
                "Eliminar la interacción peatón-montacargas",
                "Peatones y equipos se separan con pasillos protegidos con barreras, bloqueo de "
                "áreas durante las tareas, horarios sin tráfico, zonas exclusivas, vehículos "
                "seguros para desplazarse y sistemas de detección de peatones.",
            ),
            req(
                "R.1.4.1.9",
                "Procedimiento de cargue y descargue",
                "El camión se bloquea con calzos y control de llaves (el montacarguista tiene "
                "el control) y no hay conductores ni ayudantes en la zona de cargue, por "
                "ejemplo con una política de zona roja.",
            ),
        ],
        objective="Aplicar las reglas VPO para convivir de forma segura con equipos de transporte.",
        body=(
            "Montacargas, camiones y peatones compartiendo espacio es una de las "
            "combinaciones más peligrosas de una planta. Aunque tu trabajo esté en Utilities, "
            "cruzas bodegas y patios.\n\n"
            "VPO busca separar personas y máquinas, no confiar en que se vean a tiempo:\n\n"
            "* Camina solo por los pasillos peatonales protegidos.\n"
            "* Nunca entres a una zona roja de cargue.\n"
            "* Busca contacto visual con el conductor antes de cruzar.\n"
            "* Si conduces: cinturón puesto y nada de celular."
        ),
    ),
    block_node(
        slug="n0-sustancias-peligrosas",
        title="Sustancias peligrosas",
        description="PPE, CPE, inventario y cambios.",
        block="Hazardous Substances",
        icon="flask",
        requirements=[
            req(
                "R.1.6.1.1",
                "PPE para sustancias peligrosas",
                "Para manipular, cargar, descargar, usar o muestrear sustancias peligrosas, y "
                "para mantener equipos que las contengan, se usa careta de cara completa, "
                "guantes, overol y botas resistentes a químicos. También con soluciones "
                "diluidas, como las del CIP.",
            ),
            req(
                "R.1.6.1.2",
                "Cumplimiento legal en sustancias peligrosas",
                "La planta identifica la legislación aplicable al transporte, almacenamiento y "
                "uso, y tiene los permisos, licencias, formación e inspecciones que exige.",
            ),
            req(
                "R.1.6.1.3",
                "CPE para sustancias peligrosas",
                "Donde se almacenan, cargan, usan o muestrean químicos hay duchas de "
                "emergencia, lavaojos, kits antiderrames y ventilación, inspeccionados y "
                "mantenidos.",
            ),
            req(
                "R.1.6.1.4",
                "Inventario y plano de almacenamiento",
                "Hay un inventario al día de todas las sustancias peligrosas (químicos CIP, "
                "aditivos, reactivos, inflamables, gases, solventes, residuos peligrosos, NH3 y "
                "otras) con proveedor, SDS, ubicación y cantidades, incluidas las que traen "
                "contratistas y operadores logísticos (3PL).",
            ),
            req(
                "R.1.6.1.5",
                "MOC para cambios en sustancias peligrosas",
                "Pasan por MOC las sustancias nuevas y los cambios de concentración, proveedor, "
                "empaque, lugar de almacenamiento o uso, y pasar de un proceso rutinario a uno "
                "no rutinario, como dosificar a mano porque falló la dosificación automática.",
            ),
        ],
        objective="Prepararte para manipular sustancias peligrosas según VPO.",
        body=(
            "Soda cáustica, ácidos, desinfectantes del CIP, químicos de tratamiento de agua: "
            "en Utilities las sustancias peligrosas son parte del trabajo diario.\n\n"
            "VPO pide tres cosas básicas: saber qué sustancias hay y dónde (inventario con "
            "SDS), tener a mano la protección colectiva (ducha, lavaojos, kit antiderrames) y "
            "usar siempre el PPE para químicos, también con soluciones diluidas.\n\n"
            "Ojo con los cambios: si falla la dosificación automática y toca dosificar a "
            "mano, eso ya es un cambio que requiere MOC."
        ),
    ),
    block_node(
        slug="n0-lototo",
        title="LOTOTO y máquinas",
        description="SAM, bloqueo de energías y jogging.",
        block="LOTOTO and Machine Safety",
        icon="lock",
        requirements=[
            req(
                "R.1.7.1.1",
                "SOP general de SAM, LOTOTO y jogging",
                "El procedimiento describe los 6 pasos de SAM, los 9 pasos de LOTOTO, la "
                "diferencia entre personal autorizado y afectado, el bloqueo múltiple, la "
                "entrega de turno y el jogging.",
            ),
            req(
                "R.1.7.1.2",
                "AB InBev bloquea primero, el contratista agrega su candado",
                "El personal autorizado de AB InBev hace el LOTOTO y luego cada contratista "
                "pone su propio candado. Excepciones: proveedores permanentes incluidos en la "
                "lista de autorizados y bloqueos que exigen una especialidad, como la acometida "
                "de alta tensión.",
            ),
            req(
                "R.1.7.1.3",
                "Formación teórica y práctica en SAM y LOTOTO",
                "Líderes, operadores y técnicos reciben formación teórica y práctica con SKAP. "
                "Deben distinguir SAM de LOTOTO, explicar sus pasos y el jogging. Refuerzo al "
                "menos cada 3 años.",
            ),
            req(
                "R.1.7.1.4",
                "Lista de personal autorizado para LOTOTO",
                "La lista indica para qué energías (eléctrica, mecánica, NH3...) y qué grupos "
                "de equipos está autorizada cada persona. Un proveedor solo entra a la lista si "
                "completó la formación de LOTOTO y SAM.",
            ),
        ],
        objective="Dominar las reglas VPO de bloqueo de energías antes de intervenir un equipo.",
        body=(
            "Bloquear las energías antes de intervenir un equipo es una de las reglas que más "
            "vidas salva en una planta industrial.\n\n"
            "VPO trabaja con dos procesos que debes saber distinguir:\n\n"
            "* SAM, con 6 pasos.\n"
            "* LOTOTO (Lock Out, Tag Out, Test Out), con 9 pasos: desenergizar, bloquear, "
            "etiquetar y comprobar que no queda energía.\n\n"
            "Solo bloquea quien está autorizado para esa energía y ese equipo. Si hay "
            "contratistas, primero bloquea AB InBev y después cada contratista pone su propio "
            "candado."
        ),
    ),
    block_node(
        slug="n0-trabajo-alturas",
        title="Trabajo en alturas",
        description="Permiso y protección desde 2 metros.",
        block="Working at heights",
        icon="mountain",
        requirements=[
            req(
                "R.1.8.1.1",
                "Permiso de trabajo en alturas",
                "Se requiere permiso para trabajar junto a desniveles de más de 2 m (o menos si "
                "la ley lo exige), armar, modificar, desarmar o usar andamios, usar plataformas "
                "elevadoras y acceder a techos. Hay excepciones puntuales para personal propio "
                "formado que figure en una lista.",
            ),
            req(
                "R.1.8.1.3",
                "Protección contra caídas desde 2 metros",
                "Todo el FLTM, contratistas incluidos, usa protección contra caídas en cualquier "
                "trabajo a más de 2 m, o menos si la ley lo exige.",
            ),
        ],
        objective="Aplicar la regla de los 2 metros en permisos y protección contra caídas.",
        body=(
            "Las caídas de altura están entre las principales causas de lesiones graves y "
            "fatales en la industria.\n\n"
            "En VPO el número clave es 2 metros:\n\n"
            "* Desde 2 m (o menos si la ley local lo pide) se necesita permiso de trabajo.\n"
            "* Desde 2 m se usa siempre protección contra caídas, también los contratistas.\n\n"
            "Subir a un techo, aunque sea solo para inspeccionar o limpiar canales, también "
            "requiere evaluación de riesgos, método de trabajo y permiso."
        ),
    ),
    block_node(
        slug="n0-espacios-confinados",
        title="Espacios confinados",
        description="Permiso, supervisión y rescate.",
        block="Confined Spaces",
        icon="cylinder",
        requirements=[
            req(
                "R.1.10.1.1",
                "Permiso para entrar a espacios confinados",
                "Toda entrada a un espacio confinado requiere permiso de trabajo.",
            ),
            req(
                "R.1.10.1.2",
                "Supervisión permanente y rescate",
                "Mientras haya alguien adentro, la supervisión es permanente e incluye apoyo de "
                "emergencia. Hay un equipo de rescate formado y al menos un simulacro de rescate "
                "al año.",
            ),
            req(
                "R.1.10.1.3",
                "Inventario y programa de espacios confinados",
                "Una evaluación de riesgos identifica todos los espacios confinados, también los "
                "que podrían llegar a serlo, y da lugar a un inventario y un SOP. Todos están "
                "rotulados.",
            ),
            req(
                "R.1.10.1.4",
                "Roles y formación en espacios confinados",
                "Quienes entran, supervisan o responden a emergencias tienen formación con "
                "SKAP, con refuerzo al menos cada 3 años.",
            ),
        ],
        objective="Entrar y supervisar espacios confinados con las reglas VPO.",
        body=(
            "Tanques, cisternas, fosos, torres de enfriamiento: en Utilities abundan los "
            "espacios confinados. Adentro puede faltar oxígeno, acumularse gases o ser muy "
            "difícil salir o rescatar a alguien.\n\n"
            "Las reglas VPO son claras:\n\n"
            "* Nunca se entra sin permiso de trabajo.\n"
            "* Nunca se deja a alguien adentro sin supervisión permanente.\n"
            "* Hay un equipo de rescate formado que practica al menos una vez al año.\n"
            "* Todos los espacios confinados están identificados y rotulados."
        ),
    ),
    block_node(
        slug="n0-emergencias",
        title="Emergencias",
        description="Roles y formación para responder.",
        block="Emergency Preparedness and Response",
        icon="siren",
        requirements=[
            req(
                "R.1.11.1.3",
                "Roles y formación en respuesta a emergencias",
                "Los roles de emergencia están definidos y hay formación con SKAP para todo el "
                "FLTM, para quienes tienen un rol específico (brigada, evacuación, primeros "
                "auxilios, corte de energías) y para los líderes. Refuerzo al menos cada 3 años.",
            ),
        ],
        objective="Saber quién se forma en respuesta a emergencias y con qué roles.",
        body=(
            "En una emergencia no hay tiempo para aprender: cada persona debe saber de "
            "antemano qué le toca hacer.\n\n"
            "VPO exige roles definidos y formación para tres grupos:\n\n"
            "* Todo el FLTM, sin excepción.\n"
            "* Quienes tienen un rol específico: brigada, evacuación, primeros auxilios y "
            "corte de energías.\n"
            "* Los líderes.\n\n"
            "En Utilities el corte de energías es un rol crítico. Pregunta a tu líder cuál es "
            "el tuyo."
        ),
    ),
    block_node(
        slug="n0-contratistas",
        title="Contratistas",
        description="Los 10 pasos de la gestión de contratistas.",
        block="Contractor and Service Providers Management",
        icon="users",
        requirements=[
            req(
                "R.1.12.1.1",
                "Permiso general para trabajos de contratistas",
                "Antes de empezar se revisan el plan de seguridad y el método de trabajo, y se "
                "emite un permiso general o documento de inicio. Un proveedor permanente (por "
                "ejemplo, de montacargas) no lo necesita; uno que viene cada 2 semanas (por "
                "ejemplo, control de plagas) sí.",
            ),
            req(
                "R.1.12.1.2",
                "Permiso específico para tareas críticas (paso 7)",
                "Además del permiso general, las tareas críticas tienen permiso específico, "
                "alineado con el plan de seguridad y el método de trabajo.",
            ),
            req(
                "R.1.12.1.3",
                "Inducción general y por tarea (paso 4)",
                "Contratistas y proveedores reciben inducción general de seguridad y otra "
                "específica de su tarea. Los visitantes reciben inducción general.",
            ),
            req(
                "R.1.12.1.4",
                "Supervisión de seguridad (paso 6)",
                "Hay supervisión en todo momento, también de noche, fines de semana y festivos: "
                "supervisión para todo trabajo de contratistas, permanente en tareas críticas y "
                "una estructura de seguridad en proyectos grandes.",
            ),
            req(
                "R.1.12.1.5",
                "SOP de contratistas con 10 pasos",
                "1 comunicación entre áreas, 2 precalificación, 3 plan de seguridad y método de "
                "trabajo, 4 inducción, 5 verificación de competencias y equipos, 6 supervisión, "
                "7 permisos de trabajo, 8 charlas de seguridad y carteleras, 9 inspecciones y "
                "auditorías, 10 evaluación final.",
            ),
            req(
                "R.1.12.1.6",
                "Verificación de competencias (paso 5)",
                "Se valida y documenta la formación y certificación en tareas especializadas: "
                "espacios confinados, andamios, plataformas, grúas, montacargas, soldadura, "
                "procesos de alto riesgo, fuentes radiactivas o retiro de asbesto, entre otras.",
            ),
            req(
                "R.1.12.1.7",
                "Última verificación en tareas críticas",
                "Justo antes de una tarea crítica se hace una última verificación en el sitio "
                "de trabajo.",
            ),
            req(
                "R.1.12.1.8",
                "Formación de quienes gestionan contratistas",
                "Quienes contratan, inducen y supervisan contratistas, los gerentes de proyecto "
                "y los planeadores de mantenimiento tienen formación con SKAP, con refuerzo al "
                "menos cada 3 años.",
            ),
        ],
        objective="Conocer los 10 pasos VPO para trabajar con contratistas de forma segura.",
        body=(
            "Muchos trabajos de alto riesgo en Utilities los hacen contratistas: reparación "
            "de calderas, montaje de tuberías, trabajos eléctricos. Su seguridad también es "
            "responsabilidad de la planta.\n\n"
            "VPO organiza la gestión de contratistas en 10 pasos. Los que más vas a ver:\n\n"
            "* Paso 4: nadie trabaja sin inducción general y de su tarea.\n"
            "* Paso 6: siempre hay supervisión, también de noche, fines de semana y festivos.\n"
            "* Paso 7: permiso general para todo trabajo y permiso específico para las tareas "
            "críticas.\n"
            "* Paso 8: charla de seguridad (toolbox) antes de empezar."
        ),
    ),
    block_node(
        slug="n0-gestion-sif",
        title="Gestión SIF",
        description="Reglas que Salvan Vidas.",
        block="SIF Management",
        icon="warning",
        requirements=[
            req(
                "R.1.14.1.1",
                "Reglas que Salvan Vidas",
                "Las Reglas que Salvan Vidas (Life Saving Rules) se comunican en carteleras, "
                "inducción y formación, junto con las consecuencias disciplinarias. El FLTM "
                "sabe explicar por qué existen, qué peligros controlan y qué pasa si no se "
                "aplican. La planta identifica y elimina lo que impide cumplirlas.",
            ),
        ],
        objective="Aplicar las Reglas que Salvan Vidas incluso cuando algo dificulta cumplirlas.",
        body=(
            "SIF significa lesión grave o fatal (Serious Injury or Fatality). Las Reglas que "
            "Salvan Vidas existen porque cada una responde a situaciones que ya le costaron "
            "la vida a alguien.\n\n"
            "VPO espera que puedas explicar de cada regla:\n\n"
            "* Por qué existe.\n"
            "* Qué peligro controla y qué medida la cumple.\n"
            "* Qué consecuencias tiene no aplicarla.\n\n"
            "Si algo te impide cumplir una regla (falta un candado, no hay arnés), repórtalo: "
            "la planta debe resolverlo de inmediato."
        ),
    ),
    block_node(
        slug="n0-monitoreo-coaching",
        title="Monitoreo y coaching",
        description="Ninguna área ni turno sin cubrir.",
        block="Safety Monitoring & Coaching",
        icon="eye",
        requirements=[
            req(
                "R.1.16.1.1",
                "Programa de monitoreo y coaching de seguridad",
                "Los líderes siguen una matriz de monitoreo que cubre todas las áreas y turnos, "
                "también noches, fines de semana y periodos de baja actividad (sin zonas "
                "grises). Define frecuencias, incluye salud ocupacional y conversaciones de "
                "seguridad con coaching y reconocimiento.",
            ),
            req(
                "R.1.16.1.2",
                "Roles y formación en monitoreo y coaching",
                "Quienes participan en el monitoreo y coaching tienen roles definidos y "
                "formación con SKAP, con refuerzo al menos cada 3 años.",
            ),
        ],
        objective="Entender cómo funciona el monitoreo de seguridad y qué son las zonas grises.",
        body=(
            "El monitoreo de seguridad no busca culpables: es la presencia de los líderes en "
            "planta para ver cómo se trabaja, reconocer lo que se hace bien y corregir a "
            "tiempo.\n\n"
            "La clave de VPO son las zonas grises: ningún área ni turno puede quedar sin "
            "cubrir. Eso incluye la noche, el fin de semana y los periodos de baja actividad, "
            "justo cuando en Utilities suele haber menos gente y más mantenimiento."
        ),
    ),
    block_node(
        slug="n0-cultura-seguridad",
        title="Cultura de seguridad",
        description="Comportamiento y Política Global.",
        block="Behavioral Safety Culture",
        icon="handshake",
        requirements=[
            req(
                "R.1.17.1.1",
                "Formación en seguridad basada en el comportamiento",
                "Todos los empleados reciben formación en seguridad basada en el comportamiento "
                "con SKAP, con roles definidos y refuerzo al menos cada 3 años.",
            ),
            req(
                "R.1.17.2.1",
                "Política Global de Seguridad",
                "La Política Global de Seguridad de AB InBev es la base de la gestión de "
                "seguridad de la planta, forma parte de la inducción y el FLTM la conoce.",
            ),
        ],
        objective="Entender el papel del comportamiento y de la Política Global de Seguridad.",
        body=(
            "Las normas y los equipos de protección controlan muchos riesgos, pero al final "
            "cada persona decide cómo trabaja.\n\n"
            "Por eso VPO pide dos cosas desde el nivel 0:\n\n"
            "* Formación en seguridad basada en el comportamiento para todos, con refuerzo "
            "al menos cada 3 años.\n"
            "* Conocer la Política Global de Seguridad de AB InBev, que se presenta desde la "
            "inducción y guía la mejora continua de condiciones y comportamientos.\n\n"
            "Pregúntate: ¿sabrías explicar la política de seguridad con tus palabras a alguien "
            "que acaba de llegar?"
        ),
    ),
    block_node(
        slug="n0-cumplimiento-legal",
        title="Cumplimiento legal",
        description="Requisitos legales, licencias y permisos.",
        block="Facility compliance",
        icon="scale",
        requirements=[
            req(
                "R.1.18.1.1",
                "Requisitos legales de seguridad y salud identificados",
                "La planta identifica los requisitos legales de seguridad y salud en el trabajo "
                "que le aplican, incluidos los de sus licencias y permisos.",
            ),
        ],
        objective="Reconocer que detrás de muchos registros e inspecciones hay una obligación legal.",
        body=(
            "Cumplir la ley es el piso, no el techo. VPO pide que la planta sepa exactamente "
            "qué requisitos legales de seguridad y salud en el trabajo le aplican, incluidos "
            "los que vienen con sus licencias y permisos.\n\n"
            "En Utilities muchas de estas obligaciones te tocan de cerca: inspección de "
            "recipientes a presión, trabajo en alturas, manejo de químicos, exposición al "
            "ruido.\n\n"
            "Cuando un procedimiento te pide un registro, una inspección o una certificación, "
            "muchas veces detrás hay un requisito legal."
        ),
    ),
]


ZONE = zone(
    level=0,
    name="Cimientos de seguridad",
    description=(
        "Nivel 0 de VPO: lo mínimo que toda planta debe tener funcionando. Evaluación de "
        "riesgos, permisos, bloqueo de energías, protección y reporte de incidentes."
    ),
    theme="mint",
    icon="shield",
    nodes=NODES,
)
