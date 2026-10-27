"""Nivel 3 de madurez VPO (Safety / Utilities): dueños del territorio."""

from app.seed.vpo.builder import block_node, req, zone

NODES = [
    block_node(
        slug="n3-seguridad-operacional",
        title="Seguridad operacional",
        description="El FLTM se apropia de riesgos, permisos e izajes.",
        block="Operational Safety Management",
        icon="shield",
        requirements=[
            req(
                "R.1.1.2.11",
                "El FLTM participa en la evaluación de riesgos",
                "El FLTM participa activamente: revisa las evaluaciones y SOP existentes, "
                "interviene en las evaluaciones de equipos y procesos nuevos (como parte del "
                "MOC) y las actualiza cuando observa peligros nuevos, con foco en las tareas no "
                "rutinarias.",
            ),
            req(
                "R.1.1.2.12",
                "Toolkits de evaluación de riesgos en 70% o más",
                "Los GOP, toolkits y tableros que apoyan la evaluación de riesgos llegan a al "
                "menos 70%, con glidepaths para cerrar las brechas.",
            ),
            req(
                "R.1.1.3.7",
                "Priorización del CAPEX de seguridad",
                "El CAPEX de seguridad se prioriza según la matriz global de priorización y solo "
                "se piden en la canasta ESL los proyectos de requisitos ambientales, de "
                "seguridad y legales.",
            ),
            req(
                "R.1.1.8.5",
                "El dueño del territorio revisa los permisos",
                "El dueño del territorio de seguridad revisa (firma o queda formalmente "
                "informado) los permisos de trabajo de las tareas que se hacen en su área.",
            ),
            req(
                "R.1.1.9.6",
                "Los izajes los asume el dueño del territorio",
                "No acepta izajes no rutinarios en su área sin permiso válido, verifica que "
                "estén dadas las condiciones antes de que empiecen y es dueño de la inspección "
                "de los equipos de izaje.",
            ),
        ],
        objective="Asumir la seguridad de tu territorio en riesgos, permisos e izajes.",
        body=(
            "El nivel 3 es el de la apropiación: la seguridad deja de ser algo que revisa el "
            "área de ES y pasa a ser de quien trabaja en el territorio.\n\n"
            "Como dueño de tu área, VPO espera que:\n\n"
            "* Participes en las evaluaciones de riesgo, sobre todo de las tareas no rutinarias, "
            "y las actualices cuando veas un peligro nuevo.\n"
            "* Revises los permisos de trabajo de las tareas que se hacen en tu territorio.\n"
            "* No aceptes izajes no rutinarios sin permiso válido y verifiques las condiciones "
            "antes de que empiecen."
        ),
    ),
    block_node(
        slug="n3-procesos-alto-riesgo",
        title="Procesos de alto riesgo",
        description="Toolkits al 80% y gestión en el MCRS.",
        block="High Risk Processes Management",
        icon="flame",
        requirements=[
            req(
                "R.1.3.1.21",
                "Toolkit PSM NH3 en 80% o más",
                "El toolkit de amoníaco llega a al menos 80%, con glidepaths para cerrar brechas.",
            ),
            req(
                "R.1.3.1.23",
                "Toolkit SSM en 80% o más",
                "El toolkit de seguridad en vapor llega a al menos 80%, con glidepaths para "
                "cerrar brechas.",
            ),
            req(
                "R.1.3.1.24",
                "Toolkit ESM en 80% o más",
                "El toolkit de seguridad eléctrica llega a al menos 80%, con glidepaths para "
                "cerrar brechas.",
            ),
            req(
                "R.1.3.1.25",
                "Alto riesgo en el MCRS",
                "El estado de los programas de alto riesgo (PSM NH3, DEPSM, SSM, ESM, CO2 y N2 y "
                "recipientes a presión) forma parte del sistema de rutinas de gestión (MCRS) de "
                "la planta y de las áreas.",
            ),
        ],
        objective="Reconocer la exigencia máxima de los toolkits y su lugar en las rutinas.",
        body=(
            "El recorrido de los toolkits marca la madurez de la planta: 60% en el nivel 1, 70% "
            "en el nivel 2 y 80% en el nivel 3 para PSM NH3, SSM y ESM.\n\n"
            "Pero el cambio de fondo del nivel 3 es otro: el estado de los programas de alto "
            "riesgo entra en el MCRS, el sistema de rutinas de gestión.\n\n"
            "Es decir, deja de ser un tema que se revisa cuando llega la auditoría y pasa a "
            "verse en las reuniones periódicas de la planta y de cada área, junto con la "
            "producción y la calidad."
        ),
    ),
    block_node(
        slug="n3-ergonomia",
        title="Ergonomía y cargas",
        description="Controles reales y buenas prácticas.",
        block="Material Handling and Ergonomics",
        icon="package",
        requirements=[
            req(
                "R.1.5.1.2",
                "Controles para reducir lesiones ergonómicas",
                "A partir de la MHA y la EWRA, la planta reduce los riesgos con medidas técnicas "
                "(según las GTS), organizativas y de personas, usando la jerarquía de controles: "
                "ayudas para levantar, adaptar el puesto, reducir el peso, reducir movimientos "
                "repetitivos, rotar personas, formación en técnicas y acondicionamiento físico.",
            ),
            req(
                "R.1.5.1.3",
                "El FLTM aplica las buenas prácticas",
                "El FLTM demuestra conocimiento sobre manipulación segura de materiales y usa "
                "las ayudas para levantar y las herramientas ergonómicas que la planta provee.",
            ),
        ],
        objective="Usar las ayudas disponibles y aplicar la jerarquía de controles en cargas.",
        body=(
            "En el nivel 2 la planta evalúa. En el nivel 3 cambia las condiciones y tú aplicas "
            "las buenas prácticas.\n\n"
            "La jerarquía de controles aplicada a cargas significa, en orden: eliminar el "
            "levantamiento (ayudas mecánicas), reducir el peso, adaptar el puesto, reducir la "
            "repetición, rotar personas y, solo al final, entrenar la técnica.\n\n"
            "Si la planta puso una ayuda para levantar y no se usa, el control no existe."
        ),
    ),
    block_node(
        slug="n3-lototo",
        title="LOTOTO y máquinas",
        description="El dueño del equipo pone su candado.",
        block="LOTOTO and Machine Safety",
        icon="lock",
        requirements=[
            req(
                "R.1.7.1.13",
                "El dueño del equipo asume el LOTOTO",
                "El dueño del equipo o del territorio se apropia del LOTOTO durante el "
                "mantenimiento, con su propio candado y tarjeta. Los bloqueos en curso se "
                "comunican en el puesto de trabajo, en el cuarto de equipo, en el área de "
                "permisos o en el tablero principal de LOTOTO, según el alcance del bloqueo.",
            ),
        ],
        objective="Asumir el bloqueo de los equipos de tu territorio y comunicarlo.",
        body=(
            "En el nivel 3 el bloqueo ya no es solo cosa de mantenimiento: el dueño del equipo "
            "pone su propio candado y su propia tarjeta durante la intervención.\n\n"
            "Además, los bloqueos en curso se comunican donde la gente los pueda ver: en el "
            "puesto de trabajo, en el cuarto de equipo, en el área de permisos o en el tablero "
            "principal de LOTOTO, según el tamaño del bloqueo.\n\n"
            "Así, quien llega al turno siguiente sabe qué equipos están intervenidos y por qué "
            "no debe intentar arrancarlos."
        ),
    ),
    block_node(
        slug="n3-trabajo-alturas",
        title="Trabajo en alturas",
        description="El territorio responde por las alturas.",
        block="Working at heights",
        icon="mountain",
        requirements=[
            req(
                "R.1.8.1.15",
                "El dueño del territorio asume el trabajo en alturas",
                "No acepta trabajos en altura en su área sin permiso válido, verifica que estén "
                "dadas las condiciones antes de que empiecen y es dueño de la inspección de los "
                "equipos para trabajo en alturas.",
            ),
        ],
        objective="Verificar permisos y condiciones antes de un trabajo en altura en tu área.",
        body=(
            "El nivel 3 traslada la responsabilidad a quien está siempre en el área.\n\n"
            "Como dueño del territorio, antes de que alguien suba en tu zona:\n\n"
            "* Verificas que haya permiso de trabajo válido.\n"
            "* Verificas que estén dadas las condiciones: equipo inspeccionado, puntos de "
            "anclaje, delimitación del área debajo.\n"
            "* Eres dueño de la inspección de los equipos para trabajo en alturas de tu área.\n\n"
            "Nadie conoce mejor que tú los riesgos de trabajar sobre una tubería de vapor o "
            "junto a una descarga de válvula de seguridad."
        ),
    ),
    block_node(
        slug="n3-espacios-confinados",
        title="Espacios confinados",
        description="El territorio responde por las entradas.",
        block="Confined Spaces",
        icon="cylinder",
        requirements=[
            req(
                "R.1.10.1.8",
                "El dueño del territorio asume los espacios confinados",
                "No acepta entradas a espacios confinados en su área sin permiso válido, verifica "
                "que estén dadas las condiciones antes de que empiecen y es dueño de la "
                "inspección de los equipos de entrada y de rescate.",
            ),
        ],
        objective="Asumir como propias las entradas a espacios confinados de tu área.",
        body=(
            "La misma lógica del trabajo en alturas aplica a los espacios confinados: en el "
            "nivel 3 el dueño del territorio responde por lo que pasa en su área.\n\n"
            "Antes de que alguien entre a un tanque o a un foso de tu zona, verificas el permiso "
            "y las condiciones: mediciones de atmósfera, ventilación, bloqueo del equipo, "
            "vigilante asignado y equipo de rescate disponible.\n\n"
            "Además, eres dueño de la inspección de los equipos de entrada y rescate."
        ),
    ),
    block_node(
        slug="n3-emergencias",
        title="Emergencias",
        description="Tu territorio, listo para responder.",
        block="Emergency Preparedness and Response",
        icon="siren",
        requirements=[
            req(
                "R.1.11.1.12",
                "El dueño del territorio asume la respuesta a emergencias",
                "Se asegura de que los equipos de respuesta a emergencias de su área sean de "
                "fácil acceso y de que las rutas de evacuación estén libres de obstáculos.",
            ),
        ],
        objective="Revisar que tu área esté lista para una emergencia.",
        body=(
            "En una emergencia, los segundos que se pierden buscando un extintor tapado por "
            "estibas o esquivando un obstáculo en la ruta de evacuación pueden ser decisivos.\n\n"
            "En el nivel 3 esa revisión no es de alguien externo: es del dueño del territorio, "
            "es decir, tuya.\n\n"
            "Haz esta ronda por tu área."
        ),
    ),
    block_node(
        slug="n3-contratistas",
        title="Contratistas",
        description="Integrados en las rutinas del área.",
        block="Contractor and Service Providers Management",
        icon="users",
        requirements=[
            req(
                "R.1.12.1.17",
                "Contratistas en las rutinas del área",
                "Los contratistas y proveedores están totalmente integrados en las rutinas de "
                "seguridad del puesto de trabajo y del cuarto de equipo del área.",
            ),
        ],
        objective="Integrar a contratistas y proveedores en las rutinas de seguridad del área.",
        body=(
            "En los niveles anteriores el contratista se induce, se supervisa y se monitorea. "
            "En el nivel 3 deja de ser alguien de afuera al que se vigila y pasa a formar parte "
            "de las rutinas del área.\n\n"
            "Eso significa que participa en las reuniones de seguridad del cuarto de equipo, "
            "en las charlas del puesto de trabajo y en la revisión de los alertas e "
            "indicadores, igual que el personal propio.\n\n"
            "La lógica es simple: si comparten los riesgos del área, deben compartir también "
            "las conversaciones sobre cómo controlarlos."
        ),
    ),
    block_node(
        slug="n3-monitoreo-coaching",
        title="Monitoreo y coaching",
        description="Caminatas de la alta gerencia.",
        block="Safety Monitoring & Coaching",
        icon="eye",
        requirements=[
            req(
                "R.1.16.1.10",
                "Caminatas de seguridad de la alta gerencia",
                "El equipo directivo de la planta (director o gerente y sus reportes directos) "
                "hace y documenta al menos una caminata de seguridad cada trimestre, y la planta "
                "organiza monitoreo y coaching entre áreas al menos cada trimestre.",
            ),
        ],
        objective="Conocer el compromiso de la alta gerencia con el monitoreo en el nivel 3.",
        body=(
            "El nivel 3 involucra a la alta gerencia en el terreno:\n\n"
            "* Al menos una caminata de seguridad trimestral del equipo directivo de la planta, "
            "documentada.\n"
            "* Monitoreo y coaching entre áreas, también al menos cada trimestre.\n\n"
            "El monitoreo cruzado tiene una ventaja: alguien de otra área ve con ojos nuevos lo "
            "que en Utilities ya se volvió costumbre."
        ),
    ),
    block_node(
        slug="n3-cumplimiento-legal",
        title="Cumplimiento legal",
        description="La ley, dentro de las rutinas diarias.",
        block="Facility compliance",
        icon="scale",
        requirements=[
            req(
                "R.1.18.1.5",
                "Formación legal para los líderes",
                "La planta forma a los líderes en los requisitos legales que le aplican, con "
                "foco en su responsabilidad personal en caso de incumplimiento. El personal "
                "nuevo se forma dentro de sus primeros 6 meses.",
            ),
            req(
                "R.1.18.1.6",
                "Requisitos legales dentro de las rutinas",
                "Los requisitos legales y los de permisos y licencias están incorporados en los "
                "procesos del área y de la planta (SOP, sistema de órdenes de trabajo, listas de "
                "chequeo, formación) y se ejecutan: evaluaciones de riesgo, estudios, equipos de "
                "control, reportes, calibración, inspección y mantenimiento, monitoreo y "
                "certificaciones.",
            ),
        ],
        objective="Ver cómo la ley deja de ser un documento y se vuelve rutina de trabajo.",
        body=(
            "En el nivel 3 el cumplimiento legal deja de vivir en una carpeta y se integra en "
            "la forma de trabajar.\n\n"
            "* Los líderes se forman en los requisitos legales aplicables, con foco en su "
            "responsabilidad personal si no se cumplen. Los nuevos, en sus primeros 6 meses.\n"
            "* Las obligaciones legales quedan dentro de los SOP, las órdenes de trabajo, las "
            "listas de chequeo y la formación.\n\n"
            "Cuando el sistema de órdenes de trabajo genera automáticamente la inspección de un "
            "recipiente a presión, ahí hay un requisito legal convertido en rutina."
        ),
    ),
]


ZONE = zone(
    level=3,
    name="Dueños del territorio",
    description=(
        "Nivel 3 de VPO: la seguridad la asume quien trabaja en el área. Permisos, alturas, "
        "espacios confinados, bloqueos y emergencias con dueño claro."
    ),
    theme="grape",
    icon="trophy",
    nodes=NODES,
)
