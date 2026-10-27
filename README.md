# Ruta Utilities

**Lista de verificación interactiva** de los requisitos VPO del pilar Safety,
con forma de mapa: cada punto agrupa los requisitos de un bloque y cada
requisito se marca como **cumple (✓)** o **no cumple (✗)**.

No es un curso ni una evaluación: sirve para saber, de un vistazo, qué
requisitos de los niveles 0 a 4 están cumplidos y cuáles no.

El contenido son los **requisitos VPO del pilar Safety** de la autoevaluación
de la planta, redactados en español y conservando su código `R.x.x.x.x`.

**No hay inicio de sesión ni datos personales**: el recorrido es el mismo para
cualquier operario.

Se entrega de dos formas:

| | Para qué | Cómo se abre |
| --- | --- | --- |
| **Archivo descargable** | Subirlo a SharePoint para que cada persona lo descargue y lo haga | Un solo `.html`, sin instalar nada, sin conexión |
| **GitHub Pages** | Un link público con **un solo avance compartido** por todo el equipo | La misma página, con el avance en Firebase Firestore |
| **Versión servida** | Base para la versión corporativa con Entra ID y avance centralizado | React + FastAPI + PostgreSQL |

El contenido es el mismo en las dos: se escribe una sola vez y se publica en
ambas (ver [sección 5](#5-la-versión-descargable-sharepoint)).

Esta es una **demo funcional completa**, no una maqueta: React consume una API
REST real, FastAPI aplica todas las reglas del juego y PostgreSQL es la única
fuente de verdad del contenido y del progreso.

```
React + TypeScript  →  API REST  →  FastAPI  →  SQLAlchemy  →  PostgreSQL
   (representa)                    (decide)                    (persiste)
```

---

## Índice

1. [Requisitos](#1-requisitos)
2. [Puesta en marcha rápida](#2-puesta-en-marcha-rápida)
3. [PostgreSQL: instalación local o Docker](#3-postgresql-instalación-local-o-docker)
4. [Backend paso a paso](#4-backend-paso-a-paso)
5. [La versión descargable (SharePoint)](#5-la-versión-descargable-sharepoint)
6. [Frontend paso a paso](#6-frontend-paso-a-paso)
7. [URLs](#7-urls)
8. [Cómo usar la demo](#8-cómo-usar-la-demo)
9. [Arquitectura](#9-arquitectura)
10. [Modelo de datos](#10-modelo-de-datos)
10.1. [De dónde sale el contenido](#101-de-dónde-sale-el-contenido)
11. [Reglas del juego](#11-reglas-del-juego)
12. [API REST](#12-api-rest)
13. [Migraciones con Alembic](#13-migraciones-con-alembic)
14. [Tests](#14-tests)
15. [Cómo modificar la demo](#15-cómo-modificar-la-demo)
16. [Integración con Microsoft Entra ID](#16-integración-con-microsoft-entra-id)
17. [Despliegue posterior](#17-despliegue-posterior)
18. [Solución de problemas](#18-solución-de-problemas)

---

## 1. Requisitos

| Herramienta | Versión recomendada | Para qué |
| --- | --- | --- |
| Python | 3.11 o superior | Backend FastAPI |
| Node.js | 18 o superior | Frontend React |
| PostgreSQL | 14 o superior | Base de datos |
| Docker *(opcional)* | cualquiera reciente | Alternativa para levantar solo PostgreSQL |

Docker **no es obligatorio**: es únicamente una alternativa a instalar
PostgreSQL en tu equipo.

---

## 2. Puesta en marcha rápida

```bash
# 1. Base de datos (opción Docker; ver sección 3 para la opción local)
docker compose up -d postgres

# 2. Backend
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
copy .env.example .env          # Windows   (cp .env.example .env en Unix)
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8001

# 3. Frontend (en otra terminal)
cd frontend
npm install
npm run dev
```

Abre <http://localhost:5174>: la aplicación entra directo al mapa, sin login.

Para generar el archivo descargable: `cd frontend && npm run build:offline`.

---

## 3. PostgreSQL: instalación local o Docker

### Opción A — PostgreSQL instalado en tu equipo

Crea la base de datos de la demo y la de tests:

```sql
CREATE DATABASE ruta_utilities;
CREATE DATABASE ruta_utilities_test;
```

Desde la terminal:

```bash
psql -U postgres -c "CREATE DATABASE ruta_utilities;"
psql -U postgres -c "CREATE DATABASE ruta_utilities_test;"
```

> **Si aparece** `discordancia en la version de collation de la base de datos
> patron template1` (habitual en Windows tras una actualizacion del sistema),
> crea las bases indicando `template0`:
>
> ```sql
> CREATE DATABASE ruta_utilities TEMPLATE template0;
> CREATE DATABASE ruta_utilities_test TEMPLATE template0;
> ```
>
> Evita tener que ejecutar `ALTER DATABASE template1 REFRESH COLLATION VERSION`
> sobre la base plantilla del sistema.

> En Windows, `psql` suele estar en
> `C:\Program Files\PostgreSQL\17\bin\psql.exe`. También puedes crearlas desde
> pgAdmin con clic derecho sobre *Databases → Create → Database*.

Luego ajusta `DATABASE_URL` en `backend/.env` con **tu** usuario y contraseña.

### Opción B — Solo PostgreSQL con Docker

```bash
docker compose up -d postgres
```

`docker-compose.yml` levanta únicamente la base de datos (React y FastAPI se
ejecutan directamente en tu equipo). Incluye:

- variables `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (configurables
  en el `.env` de la raíz),
- un **volumen persistente** (`ruta_utilities_data`), así que los datos
  sobreviven a reinicios del contenedor,
- creación automática de la base de datos de tests.

Comandos útiles:

```bash
docker compose ps                 # estado
docker compose logs -f postgres   # logs
docker compose stop postgres      # detener (conserva los datos)
docker compose down               # eliminar el contenedor (conserva el volumen)
docker compose down -v            # eliminar TAMBIÉN los datos
```

> Si ya tienes PostgreSQL ocupando el puerto 5432, cambia `POSTGRES_PORT` en el
> `.env` de la raíz (por ejemplo `5433`) y ajusta el puerto en `DATABASE_URL`.

---

## 4. Backend paso a paso

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copia la configuración de ejemplo y edítala:

```bash
copy .env.example .env
```

`backend/.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ruta_utilities
TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ruta_utilities_test
APP_ENV=development
FRONTEND_URL=http://localhost:5174
AUTH_PROVIDER=demo
DEMO_TOKEN_SECRET=cambia-esto-en-tu-entorno
```

> **Nunca** hay credenciales en el código: toda la configuración viene de
> variables de entorno y `backend/.env` está en `.gitignore`.

Crea las tablas y carga el contenido:

```bash
alembic upgrade head     # migraciones
python -m app.seed       # contenido del curso (idempotente)
```

El seed imprime un resumen:

```
Seed completado. Contenido en PostgreSQL:
  users        1
  phases       4
  nodes        54
  activities   54
  questions    125
  options      420
  badges       5
  requisitos   168
```

Arranca la API:

```bash
uvicorn app.main:app --reload --port 8001
```

---

## 5. La versión descargable (SharePoint)

El entregable principal es **un único archivo HTML autocontenido**: se sube a
SharePoint, la persona lo descarga, lo abre con doble clic y hace el recorrido.
Sin instalar nada, sin usuario y sin conexión a internet.

```bash
cd frontend
npm run build:offline
```

Genera `frontend/dist-offline/RutaUtilities.html` (~690 KB). Ese es el archivo
que se sube.

**Qué lleva dentro:** el curso completo (niveles, puntos, preguntas y los
requisitos VPO), la aplicación, los estilos y hasta las tipografías, todo
incrustado. No hace ni una sola petición de red.

**Cómo funciona el avance:** se guarda en el navegador de cada persona
(`localStorage`), con los mismos umbrales por nivel. Si el
navegador no permite guardar (ventana de incógnito), la aplicación lo advierte
arriba en vez de perder el avance en silencio.

**Cómo publicarlo en SharePoint:** súbelo a una biblioteca de documentos y
comparte el enlace indicando *Descargar*. Conviene decir explícitamente
"descarga el archivo y ábrelo", porque algunas configuraciones de SharePoint
muestran los HTML como texto en lugar de abrirlos.

### Límites que conviene conocer

- **El avance es local.** Vive en el navegador de cada persona: no hay reporte
  central de quién completó qué. Si se necesita, esa es la versión servida.
- **Las respuestas están en el archivo.** Sin servidor, la corrección ocurre en
  el navegador, así que quien abra el código fuente puede verlas. Es inevitable
  en un archivo offline y no afecta al objetivo formativo.
- **Un archivo por persona.** Si alguien lo abre desde dos equipos, el avance no
  se sincroniza.
- **Actualizar el contenido = volver a publicar el archivo.** Quien ya lo tenga
  descargado seguirá con la versión vieja hasta que baje la nueva.

### Cómo se compila

| Paso | Qué hace |
| --- | --- |
| `python -m app.seed.export_json` | Vuelca el contenido de `content.py` a `frontend/src/offline/course.json` |
| `npm run build:offline` | Empaqueta todo en un solo HTML (`vite.offline.config.ts`) |
| `npm run check:offline` | Recorre el curso completo sin navegador y verifica las reglas |
| `npm run check:render` | Abre el archivo ya compilado en un DOM simulado y comprueba que se dibuje |

Las reglas del juego viven en `frontend/src/offline/engine.ts`, que es la copia
de las de FastAPI para poder funcionar sin servidor. Por eso tiene su propia
verificación: `npm run check:offline` recorre los cinco niveles y comprueba
desbloqueos, insignias y reinicio.

### Publicar en GitHub Pages (avance compartido)

`npm run build:pages` compila esta misma versión como `frontend/dist-pages/index.html`.
La diferencia es el avance: en vez de quedarse en cada navegador, se guarda en
**un único documento de Firestore** (`ruta-utilities/progreso`) y se actualiza en
vivo para todas las personas que tengan el link (`frontend/src/offline/sharedStore.ts`).
El archivo descargable no incluye Firebase y sigue funcionando sin conexión.

Puesta en marcha (una sola vez):

1. **Firebase:** en [console.firebase.google.com](https://console.firebase.google.com)
   crea un proyecto, entra a *Firestore Database → Crear base de datos* y, en
   *Reglas*, pega el contenido de [`firestore.rules`](firestore.rules) y publica.
2. **App web:** en *Configuración del proyecto → Tus apps* registra una app web
   (`</>`) y copia `apiKey`, `authDomain`, `projectId` y `appId`.
3. **GitHub:** en el repositorio, *Settings → Secrets and variables → Actions →
   Variables*, crea `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`,
   `FIREBASE_PROJECT_ID` y `FIREBASE_APP_ID` con esos valores.
4. *Settings → Pages → Source:* **GitHub Actions**. Cada push a `main` ejecuta
   [`deploy-pages.yml`](.github/workflows/deploy-pages.yml) y publica en
   `https://<usuario>.github.io/<repositorio>/`.

Para compilar en tu equipo, copia `frontend/.env.pages.example` como
`frontend/.env.pages` y llena los mismos cuatro valores.

**Ten en cuenta:** no hay inicio de sesión, así que cualquiera con el link puede
marcar temas y *Reiniciar mi progreso* borra el avance de todos. Las reglas solo
permiten tocar ese documento y con la forma que espera la aplicación.

---

## 6. Frontend paso a paso

```bash
cd frontend
npm install
npm run dev
```

La URL de la API se configura en `frontend/.env`:

```dotenv
VITE_API_URL=http://localhost:8001/api
```

Otros comandos:

```bash
npm run build       # compila y verifica TypeScript
npm run typecheck   # solo verificación de tipos
npm run preview     # sirve la build de producción
```

---

## 7. URLs

| Servicio | URL |
| --- | --- |
| Frontend | <http://localhost:5174> |
| Backend | <http://localhost:8001> |
| Swagger UI | <http://localhost:8001/docs> |
| ReDoc | <http://localhost:8001/redoc> |
| Health check | <http://localhost:8001/health> |
| PostgreSQL | `localhost:5432` |

> Se usan 5174 y 8001 (no los 5173 / 8000 habituales de Vite y uvicorn) para no
> chocar con otros servicios locales, como Docker Desktop. Si necesitas otros
> puertos: `server.port` en `frontend/vite.config.ts`, `VITE_API_URL` en
> `frontend/.env`, `FRONTEND_URL` en `backend/.env` y `--port` al arrancar uvicorn.

### Probar la API desde Swagger

1. Ejecuta `POST /api/auth/demo-login`.
2. Copia el `access_token` de la respuesta.
3. Pulsa **Authorize** (arriba a la derecha) y pégalo.
4. Ya puedes llamar al resto de endpoints.

---

## 8. Cómo se usa

1. **Abrir** — no hay pantalla de acceso ni datos personales: la aplicación
   abre directamente en el mapa y es igual para cualquier persona del área.
2. **Mapa** — resumen arriba (cumplimiento, temas que cumplen, brechas,
   insignias) y debajo el mapa con los cinco niveles VPO.
3. **Abrir un punto** — haz clic en cualquier punto del nivel abierto. Dentro
   de un nivel no hay orden obligatorio: se revisa en el orden que convenga.
4. **Marcar los temas** — cada tema muestra su código `R.x.x.x.x`, su título y
   qué significa. Se marca con **Cumple** o **No cumple**; al pulsar de nuevo
   el botón activo, el tema vuelve a quedar sin marcar.
5. **Ver el avance** — el punto muestra *3 de 5 cumplen*, y el mapa marca con
   un chulito verde los puntos donde todo cumple y con una equis roja los que
   quedaron con brechas.
6. **Abrir el siguiente nivel** — ocurre solo cuando el nivel actual alcanza su
   umbral de cumplimiento (100%, 90%, 80%, 70%).
7. **Insignias** — se conceden automáticamente al alcanzar el umbral de un
   nivel y aparecen como aviso flotante.
8. **Persistencia** — cierra y vuelve a abrir: el avance sigue donde estaba.
9. **Reiniciar** — al final de *Mi progreso*, en *Reiniciar el recorrido* (pide
   confirmación). Borra las marcas, nunca el contenido.

### Herramientas de desarrollo

Con `npm run dev` aparece abajo a la izquierda un botón **Dev** con atajos para
marcar el punto actual, cumplir el nivel abierto o reiniciar. **Todas marcan
los temas por la vía normal**; ninguna falsea el estado de React. No se
incluyen en la build de producción (`import.meta.env.DEV`).

---
## 9. Arquitectura

```
ruta-utilities/
├── backend/
│   ├── app/
│   │   ├── main.py              # ensamblaje: CORS, errores, routers
│   │   ├── core/
│   │   │   ├── config.py        # settings desde variables de entorno
│   │   │   ├── constants.py     # regla del umbral, textos de feedback
│   │   │   ├── errors.py        # errores de dominio → códigos HTTP
│   │   │   └── security.py      # IdentityProvider (demo / Entra ID)
│   │   ├── api/
│   │   │   ├── dependencies.py  # get_db, get_current_user
│   │   │   └── routes/          # auth, users, course, nodes, progress, badges, demo
│   │   ├── models/              # SQLAlchemy 2.x
│   │   ├── schemas/             # Pydantic
│   │   ├── repositories/        # acceso a datos
│   │   ├── services/            # LÓGICA DEL JUEGO
│   │   ├── db/                  # engine, session, Base
│   │   └── seed/                # contenido + carga idempotente
│   ├── alembic/                 # migraciones
│   ├── tests/                   # pytest contra base de datos de tests
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/          # UI reutilizable + ilustraciones
│       ├── features/
│       │   ├── auth/  map/  course/  progress/  profile/  badges/
│       ├── pages/               # Mapa, Progreso, Insignias, Acerca
│       ├── offline/             # motor, contenido y entrada del archivo descargable
│       ├── services/            # apiClient + authApi/courseApi/progressApi/badgeApi
│       ├── context/             # AuthProvider, CourseProvider
│       ├── hooks/  types/  utils/
├── docker-compose.yml
└── README.md
```

### Quién hace qué

**FastAPI decide** (nada de esto vive en React):

- progreso ponderado por fase y general,
- qué nodos están bloqueados, disponibles, en curso o completados,
- cuál es el siguiente punto del recorrido,
- si una respuesta es correcta,
- cuándo se desbloquea una fase,
- cuándo se concede una insignia,

**React representa** ese estado y lo anima.

**PostgreSQL persiste** todo en la versión servida. En el archivo descargable
no hay servidor: las mismas reglas corren en `frontend/src/offline/engine.ts` y
el avance se guarda en `localStorage`.

### Transacciones

Completar una actividad implica guardar la respuesta, actualizar el progreso,
recalcular desbloqueos y conceder insignias. Todo ocurre en **una sola
transacción** (`app/services/activity_service.py`): o se aplica completo, o no
se aplica nada.

---

## 10. Modelo de datos

| Tabla | Contenido |
| --- | --- |
| `users` | Registro que asocia las marcas (uno solo, sin uso en la interfaz) |
| `phases` | Niveles VPO, con `order_index` y `unlock_threshold` |
| `course_nodes` | Puntos del mapa (bloques VPO), con `icon` y `weight` = número de temas |
| `activities` | Contexto del punto: objetivo, cuerpo y `payload` JSONB con los temas |
| `requirement_marks` | **La única tabla de avance**: un tema marcado `MEETS` o `FAILS` |
| `user_phase_progress` | Foto del estado de cada nivel: desbloqueo y cumplimiento |
| `badges` | Definición de insignias y su regla |
| `user_badges` | Insignias obtenidas |

Detalles de diseño:

- Los temas viven en `activities.payload->'requirements'` como
  `{code, title, detail}`: el contenido está en PostgreSQL, no en componentes
  React.
- El estado de un punto (`PENDING`, `IN_PROGRESS`, `REVIEWED`) y el porcentaje
  de un nivel **no se guardan**: se derivan de las marcas en cada petición, de
  modo que no puede existir un estado persistido incoherente con las reglas.
- Claves foráneas con `ON DELETE CASCADE`, restricciones `UNIQUE` (un tema solo
  puede tener una marca por persona) e índices por las columnas que se
  consultan.

---
## 10.1. De dónde sale el contenido

El curso es la autoevaluación VPO de la planta (pilar **Safety**, Medellín).
Cubre **185 requisitos**: los **168 marcados `Utilities = Y`** más los **17 del
nivel 4**.

> **Sobre el nivel 4:** en la autoevaluación sus 17 requisitos están marcados
> `Utilities = N`, es decir, hoy no se evalúan para el área. Se incluyen como
> nivel aspiracional y la zona lo advierte en su descripción. Para sacarlos,
> basta quitar `NIVEL_4` de `PHASES` en `backend/app/seed/content.py` y volver a
> ejecutar el seed.

| VPO | Ruta Utilities |
| --- | --- |
| Nivel de madurez (0 a 3) | Zona del mapa |
| Bloque (LOTOTO, Espacios confinados…) | Punto de aprendizaje |
| Requisito `R.x.x.x.x` | Ficha dentro del punto, con su código |

| Nivel | Zona | Requisitos | Puntos |
| --- | --- | --- | --- |
| 0 | Cimientos de seguridad | 57 | 14 |
| 1 | Control del riesgo | 65 | 14 |
| 2 | Gestión proactiva | 27 | 12 |
| 3 | Dueños del territorio | 19 | 10 |
| 4 | Referente en seguridad | 17 *(no aplicables)* | 10 |

Cada requisito se reescribió en español de operario conservando las siglas
oficiales (LOTOTO, SAM, SKAP, SIF, SAFE form, MOC, PPE/CPE, PSM NH3, SSM, ESM,
DEPSM) y su código, para poder rastrearlo hasta la auditoría.

```
backend/app/seed/
├── content.py            # arma PHASES y BADGES
└── vpo/
    ├── catalog.json      # los 185 requisitos oficiales (código, nivel, bloque)
    ├── builder.py        # helpers: req(), choice(), true_false(), pesos
    └── nivel_0.py … nivel_4.py
```

`catalog.json` es la fuente de verdad de la trazabilidad: los tests comprueban
que el curso cubra los 185 requisitos, **exactamente una vez cada uno** y en su
nivel y bloque correctos. Si mañana cambia la autoevaluación, actualiza ese
archivo y los tests te dirán qué falta.

---

## 11. Reglas

Centralizadas en `backend/app/services/progress_service.py` y, para el archivo
descargable, en `frontend/src/offline/engine.ts`.

**Estado de un tema.** `MEETS` (cumple), `FAILS` (no cumple) o sin marcar. Solo
se guarda lo que alguien marcó: lo no marcado no existe en la base.

**Estado de un punto.** Se deriva de sus temas:

| Estado | Cuándo |
| --- | --- |
| `LOCKED` | Su nivel todavía no está abierto |
| `PENDING` | Ningún tema marcado |
| `IN_PROGRESS` | Algunos temas marcados |
| `REVIEWED` | Todos los temas marcados (cumplan o no) |

**Cumplimiento de un nivel.** Temas cumplidos ÷ total de temas del nivel. Un
tema marcado como *no cumple* cuenta como revisado, pero no suma al
cumplimiento.

**Umbrales (la regla que abre el siguiente nivel).** Bajan con la madurez: lo
básico se exige completo, lo avanzado admite brechas.

| Nivel | Temas | Umbral para abrir el siguiente |
| --- | --- | --- |
| 0 · Cimientos de seguridad | 57 | **100%** |
| 1 · Control del riesgo | 65 | **90%** |
| 2 · Gestión proactiva | 27 | **80%** |
| 3 · Dueños del territorio | 19 | **70%** |
| 4 · Referente en seguridad | 17 | **70%** |

Los umbrales están en un único lugar (`UNLOCK_THRESHOLDS` en
`backend/app/seed/vpo/builder.py`) y se guardan como columna de cada nivel. No
aparecen escritos a mano en ningún componente.

**Dentro de un nivel abierto no hay orden obligatorio:** cualquier punto se
puede abrir y marcar. Lo que se bloquea es el nivel siguiente.

**Insignias:**

| Insignia | Regla |
| --- | --- |
| Primer paso | Revisar el primer punto completo |
| Cimientos VPO | El nivel 0 alcanza su umbral |
| Control del riesgo | El nivel 1 alcanza su umbral |
| Gestión proactiva | El nivel 2 alcanza su umbral |
| Dueños del territorio | El nivel 3 alcanza su umbral |
| Maestro Utilities | Los cinco niveles alcanzan su umbral |

---
## 12. API REST

| Método | Ruta | Descripción |
| --- | --- | --- |
| `POST` | `/api/auth/demo-login` | Resuelve la sesión técnica (sin credenciales) |
| `GET` | `/api/auth/me` | Registro de la sesión actual |
| `GET` | `/api/users/me` | Igual que el anterior |
| `GET` | `/api/course` | Mapa completo con estado y resumen |
| `GET` | `/api/phases` | Niveles con su estado |
| `GET` | `/api/phases/{phase_id}` | Detalle de un nivel |
| `GET` | `/api/nodes/{node_id}` | Punto con su contexto y sus temas |
| `PUT` | `/api/nodes/{node_id}/requirements/{code}` | Marca un tema |
| `GET` | `/api/progress/me` | Avance completo |
| `GET` | `/api/badges/me` | Insignias |
| `POST` | `/api/demo/reset` | Borra todas las marcas |
| `GET` | `/health` | Estado del servicio y de PostgreSQL |

Marcar un tema acepta `MEETS`, `FAILS` o `PENDING` (esta última borra la
marca):

```json
PUT /api/nodes/1/requirements/R.1.1.2.1
{ "status": "MEETS" }
```

```json
{
  "code": "R.1.1.2.1",
  "status": "MEETS",
  "state": {
    "node_status": "IN_PROGRESS",
    "node_reviewed": false,
    "node_met": 1,
    "node_total": 12,
    "phase_progress": 2,
    "general_progress": 1,
    "new_phase_unlocked": false,
    "new_badges": [],
    "course_compliant": false,
    "next_node_id": 1
  }
}
```

Códigos usados: `200`, `401` (sin token o inválido), `403` (el nivel todavía
está bloqueado), `404` (el punto o el tema no existen), `422` (estado no
válido), `500` (error interno, siempre con mensaje amigable).

**CORS** está limitado a `http://localhost:5174` (configurable con
`FRONTEND_URL`); no se usa `*`.

---
## 13. Migraciones con Alembic

La estructura oficial de la base de datos son las migraciones. No se depende de
`create_all()`.

Hay dos migraciones: `0001_initial` crea el esquema y
`0002_requirement_marks` lo convierte en lista de verificación (crea
`requirement_marks` y elimina las tablas de preguntas y respuestas).

```bash
cd backend
alembic upgrade head                                   # aplicar
alembic revision --autogenerate -m "descripcion"       # crear tras cambiar modelos
alembic downgrade -1                                   # deshacer la última
alembic current                                        # revisión aplicada
alembic history                                        # historial
```

La URL de conexión la lee `alembic/env.py` desde `DATABASE_URL`; **no** está
escrita en `alembic.ini`.

Orden de la primera instalación:

```
crear base de datos → configurar .env → alembic upgrade head → seed → uvicorn
```

---

## 14. Tests

```bash
cd backend
pytest              # toda la suite
pytest -v           # detallado
pytest tests/test_unlocking.py
```

Los tests se ejecutan contra `TEST_DATABASE_URL`, **nunca** contra la base
principal: si ambas coinciden, la suite se detiene antes de empezar.

**41 tests.** Cubren: sesión técnica, exigencia de token, persistencia de una
marca, que *no cumple* no sume al cumplimiento, desmarcar un tema, acceso libre
dentro de un nivel abierto, punto de nivel bloqueado, tema que no pertenece al
punto, estado inválido, el 100% que exige el nivel 0, el 90% del nivel 1,
concesión de insignias (y que no se repitan) y reinicio que borra las marcas
conservando el catálogo.

`tests/test_vpo_content.py` vigila la trazabilidad con el estándar: que estén
los 185 requisitos sin repetirse, cada uno en su nivel y bloque, que los
umbrales sean 100/90/80/70/70, que el peso de un punto sea su número de temas,
que no queden cuestionarios en el contenido y que todo icono usado esté
registrado en el frontend. Estos no necesitan base de datos.

El archivo descargable lleva su propia copia de las reglas, así que se verifica
aparte, sin navegador:

```bash
cd frontend
npm run check:offline   # recorre los 5 niveles y comprueba las reglas
npm run check:render    # abre el HTML compilado y comprueba que se dibuje
```

---

## 15. Cómo modificar la demo

| Qué quieres cambiar | Dónde |
| --- | --- |
| **Usuario demo** | `backend/.env` (`DEMO_USER_NAME`, `DEMO_USER_AREA`, `DEMO_USER_PLANT`, `DEMO_USER_ROLE`) y vuelve a ejecutar `python -m app.seed` |
| **Contenido de un nivel** | `backend/app/seed/vpo/nivel_0.py` … `nivel_4.py` → `python -m app.seed` y `python -m app.seed.export_json` |
| **Añadir un punto** | Nuevo `block_node(...)` en la lista `NODES` del nivel; el peso y el `order_index` se calculan solos |
| **Editar un tema** | `req("R.x.x.x.x", título, detalle)` dentro del bloque correspondiente |
| **Añadir un requisito** | `req("R.x.x.x.x", título, detalle)` en el bloque + la fila correspondiente en `app/seed/vpo/catalog.json` |
| **Umbrales por nivel** | `UNLOCK_THRESHOLDS` en `backend/app/seed/vpo/builder.py` |
| **Insignias** | `BADGES` en `backend/app/seed/content.py` + regla en `backend/app/services/badge_service.py` |
| **Mascota** | `frontend/src/components/MascotGuide.tsx` → sustituir solo `MascotAvatar` |
| **Logotipo** | `BrandMark` en `frontend/src/components/UserHeader.tsx` |
| **Colores / branding** | `frontend/tailwind.config.js`, `frontend/src/index.css` y `frontend/src/utils/theme.ts` |
| **Iconos** | Clave en el nivel (`icon="flame"`) + registro en `frontend/src/utils/icons.ts` |
| **Conexión a PostgreSQL** | `DATABASE_URL` en `backend/.env` |
| **URL de la API** | `VITE_API_URL` en `frontend/.env` |

> El seed **sincroniza** el catálogo: actualiza por `slug` lo que existe, crea
> lo nuevo y **elimina lo que ya no aparece** en el contenido. El progreso sobre
> los puntos que siguen existiendo nunca se toca; el de un punto eliminado
> desaparece con él, porque ese punto ya no forma parte de la ruta.

### Placeholders pendientes de reemplazo

- **Mascota "Gotix"** — personaje neutral creado para la demo. No imita ninguna
  mascota oficial. Punto exacto de reemplazo documentado en el propio archivo.
- **Logotipo "RU"** — cuadro dorado con iniciales, sustituible por la marca real.
- **Paleta** — inspirada en amarillo/dorado, azul, blanco y verde suave, sin
  copiar branding oficial. Centralizada para poder cambiarla de una vez.

---

## 16. Integración con Microsoft Entra ID

**Todavía no está implementada** (esta versión usa login demo), pero la
arquitectura ya está preparada para sustituirla sin reconstruir la aplicación.

### Backend

`backend/app/core/security.py` define el contrato:

```
IdentityProvider (protocolo)
  ├─ DemoIdentityProvider     ← activo hoy
  └─ EntraIdentityProvider    ← esqueleto listo para implementar
```

Los servicios y routers **nunca** ven un token: reciben un `User` ya resuelto
por la dependencia `get_current_user`. Para migrar:

1. Registra la aplicación en Entra ID y obtén `tenant_id` y `client_id`.
2. Implementa `EntraIdentityProvider.resolve_user`: descarga las claves públicas
   de `https://login.microsoftonline.com/<tenant>/discovery/v2.0/keys` y valida
   firma, `aud` e `iss` del access token.
3. Busca o crea el `User` usando el claim `oid` en la columna
   `users.external_id` (ya existe, es única y está indexada).
4. Cambia `AUTH_PROVIDER=entra` en `backend/.env`.

No se almacenan contraseñas corporativas: la contraseña nunca llega a esta
aplicación.

### Frontend

`frontend/src/services/auth/AuthService.ts` define la interfaz; hoy la implementa
`DemoAuthService`. Para migrar, crea `MicrosoftEntraAuthService` (por ejemplo con
MSAL) cumpliendo la misma interfaz y cambia **una línea** en
`frontend/src/context/AuthContext.tsx`:

```ts
const authService: AuthService = new MicrosoftEntraAuthService()
```

Ninguna pantalla ni componente necesita modificarse.

---

## 17. Despliegue posterior

Ideas para llevar la demo más allá del equipo local:

- **Backend**: `uvicorn app.main:app --host 0.0.0.0 --port 8000` detrás de un
  proxy inverso, o contenerizado (`Dockerfile` con `pip install -r
  requirements.txt` + uvicorn). Ejecuta `alembic upgrade head` en el arranque
  del despliegue y el seed una sola vez.
- **Frontend**: `npm run build` genera `dist/`, que es estático y puede servirse
  desde cualquier hosting o CDN. Ajusta `VITE_API_URL` antes de compilar.
- **Base de datos**: cualquier PostgreSQL gestionado; solo cambia `DATABASE_URL`.
- **Antes de producción**: `APP_ENV=production`, `DEMO_TOKEN_SECRET` real,
  `FRONTEND_URL` con el dominio definitivo y HTTPS.

---

## 18. Solución de problemas

| Síntoma | Causa probable y solución |
| --- | --- |
| `No pudimos conectar con el servidor` en el frontend | FastAPI no está corriendo. Arranca `uvicorn app.main:app --reload --port 8001` y comprueba <http://localhost:8001/health> |
| `database "ruta_utilities" does not exist` | Falta crear la base de datos (sección 3) |
| `password authentication failed` | Usuario o contraseña incorrectos en `DATABASE_URL` |
| `connection refused` en el puerto 5432 | PostgreSQL no está en ejecución, o Docker no ha levantado el contenedor |
| `No hay usuario demo en la base de datos` | Falta ejecutar `python -m app.seed` |
| `relation "users" does not exist` | Falta ejecutar `alembic upgrade head` |
| El mapa no avanza tras completar un punto | Revisa la consola del navegador; el mapa se recarga desde `/api/course` tras cada acción |
| Error de CORS | `FRONTEND_URL` en `backend/.env` debe coincidir con la URL del frontend |
| Puerto 5432 ocupado al usar Docker | Cambia `POSTGRES_PORT` en el `.env` de la raíz y en `DATABASE_URL` |
| Los tests se niegan a ejecutarse | `TEST_DATABASE_URL` es igual a `DATABASE_URL`; sepáralas |
| `discordancia en la version de collation ... template1` | Crea las bases con `TEMPLATE template0` (ver sección 3) |

---

## Estado de esta versión

Incluye: el **archivo descargable** listo para SharePoint, modelos,
migraciones, seed sincronizado, los **185 requisitos VPO de Safety** repartidos
en 5 niveles y 60 puntos, marcado ✓/✗ por tema, umbrales 100/90/80/70/70, API
REST documentada, cálculo de cumplimiento, desbloqueos, insignias, mapa
interactivo, animaciones, reinicio, 41 tests de backend y las verificaciones
del motor offline.

Pendiente para una versión posterior: autenticación con Microsoft Entra ID,
multiusuario y reportería para líderes.

No hay inicio de sesión ni datos personales en ninguna de las dos versiones.

El contenido cubre **solo el pilar Safety**. Los demás pilares VPO se pueden
añadir como niveles nuevos siguiendo el mismo patrón de `app/seed/vpo/`.