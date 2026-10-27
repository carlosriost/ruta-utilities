/**
 * Motor de la version descargable.
 *
 * En la version servida por API todas las reglas viven en FastAPI. El archivo
 * descargable no tiene servidor, asi que este modulo es su unica fuente de
 * verdad: es el mismo conjunto de reglas portado desde
 * `backend/app/services/progress_service.py`, `requirement_service.py` y
 * `badge_service.py`.
 *
 * Un tema es binario y su valor por defecto es "no cumple": solo se guarda la
 * excepcion (los codigos marcados como cumplidos). El avance se guarda en
 * `localStorage`, por navegador y por equipo.
 *
 * En GitHub Pages el avance es compartido: `sharedStore.ts` conecta un destino
 * remoto (Firestore) con `connectRemote` y entrega lo que llega con `hydrate`.
 * Sin destino remoto el motor se comporta exactamente igual que antes.
 */

import type {
  Badge,
  BadgeCollection,
  CourseResponse,
  NodeDetail,
  NodeState,
  NodeStatus,
  PhaseDetail,
  ProgressResponse,
  ProgressSummary,
  Requirement,
  StateChange,
  ZoneTheme,
} from '@/types/api'
import courseData from './course.json'

const LOCKED_BY_PHASE = 'Completa el nivel anterior para desbloquear esta zona.'
const STORAGE_KEY = 'ruta-utilities.marcas.v3'

// --- Forma del contenido embebido -------------------------------------------
interface RawRequirement {
  code: string
  title: string
  detail: string
}
interface RawNode {
  id: number
  phase_id: number
  slug: string
  title: string
  description: string
  icon: string
  order_index: number
  objective: string
  body: string
  vpo_block: string | null
  requirements: RawRequirement[]
}
interface RawPhase {
  id: number
  slug: string
  name: string
  description: string
  order_index: number
  unlock_threshold: number
  theme: ZoneTheme
  icon: string
  nodes: RawNode[]
}
interface RawBadge {
  id: number
  slug: string
  name: string
  description: string
  icon: string
  theme: string
  rule_type: 'FIRST_REQUIREMENT_MET' | 'PHASE_COMPLIANT' | 'COURSE_COMPLIANT'
  rule_ref: string | null
}

const COURSE = courseData as unknown as { phases: RawPhase[]; badges: RawBadge[] }
const ALL_NODES = COURSE.phases.flatMap((phase) => phase.nodes)

// --- Avance guardado ---------------------------------------------------------
interface Progress {
  /** Codigos de los temas marcados como cumplidos. Lo no listado no cumple. */
  metCodes: string[]
  badges: Record<string, string>
  /** Niveles ya anunciados, para no repetir la animacion de desbloqueo. */
  announced: string[]
  started_at: string | null
}

const empty = (): Progress => ({
  metCodes: [],
  badges: {},
  announced: [],
  started_at: null,
})

/** Sin localStorage (incognito, politicas) se sigue trabajando en memoria. */
let memory: Progress | null = null
let storageWorks = true

function load(): Progress {
  if (memory) return memory
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    memory = raw ? { ...empty(), ...(JSON.parse(raw) as Progress) } : empty()
  } catch {
    storageWorks = false
    memory = empty()
  }
  return memory
}

function save(progress: Progress): void {
  memory = progress
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
  } catch {
    storageWorks = false
  }
}

export function storageAvailable(): boolean {
  load()
  return storageWorks
}

// --- Avance compartido --------------------------------------------------------
/** Parte del avance que es comun a todas las personas que abren el link. */
export interface SharedProgress {
  metCodes: string[]
  badges: Record<string, string>
  started_at: string | null
}

/**
 * Destino remoto de cada cambio. Se envian operaciones sueltas (no el avance
 * entero) para que dos personas marcando a la vez no se pisen.
 */
export interface RemoteSink {
  setCode(code: string, meets: boolean): void
  awardBadge(slug: string, awardedAt: string): void
  setStartedAt(startedAt: string): void
  reset(): void
}

let remote: RemoteSink | null = null

export function connectRemote(sink: RemoteSink): void {
  remote = sink
}

/**
 * Sustituye el avance local por el compartido. Los niveles ya anunciados se
 * conservan: son de cada pantalla, no del equipo.
 */
export function hydrate(shared: SharedProgress): void {
  const local = load()
  save({
    ...local,
    metCodes: [...shared.metCodes],
    badges: { ...shared.badges },
    started_at: shared.started_at,
  })
}

const now = () => new Date().toISOString()
const percent = (part: number, total: number) =>
  total <= 0 ? 0 : Math.max(0, Math.min(100, Math.round((part * 100) / total)))

/** Punto todavia no accesible. Se traduce a un 403, igual que en la API. */
export class LockedError extends Error {}

// --- Calculo del estado ------------------------------------------------------
interface ComputedPhase {
  phase: RawPhase
  unlocked: boolean
  total: number
  met: number
  compliantNodes: number
  percent: number
  compliant: boolean
  nodes: NodeState[]
}
interface ComputedState {
  phases: ComputedPhase[]
  statuses: Record<number, NodeState>
  summary: ProgressSummary
  courseCompliant: boolean
}

function nodeStatus(unlocked: boolean, total: number, met: number): NodeStatus {
  if (!unlocked) return 'LOCKED'
  if (total > 0 && met < total) return 'HAS_GAPS'
  return 'COMPLIANT'
}

function computeState(progress: Progress): ComputedState {
  const met = new Set(progress.metCodes)
  const phases: ComputedPhase[] = []
  const statuses: Record<number, NodeState> = {}
  let previous: ComputedPhase | null = null

  for (const phase of COURSE.phases) {
    // El primer nivel siempre esta abierto; los demas dependen del
    // cumplimiento del anterior.
    const unlocked = previous === null || previous.compliant
    const nodes = [...phase.nodes].sort((a, b) => a.order_index - b.order_index)
    const states: NodeState[] = []

    for (const node of nodes) {
      const metCount = node.requirements.filter((r) => met.has(r.code)).length
      const total = node.requirements.length
      const state: NodeState = {
        id: node.id,
        phase_id: phase.id,
        slug: node.slug,
        title: node.title,
        description: node.description,
        icon: node.icon,
        order_index: node.order_index,
        total_requirements: total,
        met: metCount,
        failed: total - metCount,
        status: nodeStatus(unlocked, total, metCount),
        locked_reason: unlocked ? null : LOCKED_BY_PHASE,
      }
      states.push(state)
      statuses[node.id] = state
    }

    const total = states.reduce((sum, s) => sum + s.total_requirements, 0)
    const metTotal = states.reduce((sum, s) => sum + s.met, 0)
    const computed: ComputedPhase = {
      phase,
      unlocked,
      total,
      met: metTotal,
      compliantNodes: states.filter((s) => s.status === 'COMPLIANT').length,
      percent: percent(metTotal, total),
      compliant: percent(metTotal, total) >= phase.unlock_threshold,
      nodes: states,
    }
    phases.push(computed)
    previous = computed
  }

  const nextNode = phases
    .filter((p) => p.unlocked)
    .flatMap((p) => p.nodes)
    .find((n) => n.status !== 'COMPLIANT')

  let currentPhase: ComputedPhase | null = null
  for (const phase of phases) {
    if (!phase.unlocked) break
    currentPhase = phase
    if (phase.compliantNodes < phase.nodes.length) break
  }

  const total = phases.reduce((sum, p) => sum + p.total, 0)
  const metTotal = phases.reduce((sum, p) => sum + p.met, 0)
  const courseCompliant = phases.length > 0 && phases.every((p) => p.compliant)

  return {
    phases,
    statuses,
    courseCompliant,
    summary: {
      general_progress: percent(metTotal, total),
      met_requirements: metTotal,
      failed_requirements: total - metTotal,
      total_requirements: total,
      compliant_nodes: phases.reduce((sum, p) => sum + p.compliantNodes, 0),
      total_nodes: phases.reduce((sum, p) => sum + p.nodes.length, 0),
      badges_earned: Object.keys(progress.badges).length,
      badges_total: COURSE.badges.length,
      current_phase_id: currentPhase?.phase.id ?? null,
      current_phase_name: currentPhase?.phase.name ?? null,
      next_node_id: nextNode?.id ?? null,
      next_node_title: nextNode?.title ?? null,
      unlocked_phases: phases.filter((p) => p.unlocked).length,
      total_phases: phases.length,
      started_at: progress.started_at,
      course_compliant: courseCompliant,
    },
  }
}

// --- Insignias ---------------------------------------------------------------
function badgeSchema(badge: RawBadge, awardedAt: string | null): Badge {
  return {
    id: badge.id,
    slug: badge.slug,
    name: badge.name,
    description: badge.description,
    icon: badge.icon,
    theme: badge.theme,
    earned: awardedAt !== null,
    awarded_at: awardedAt,
  }
}

function evaluateBadges(progress: Progress, state: ComputedState): Badge[] {
  const nuevas: Badge[] = []
  for (const badge of COURSE.badges) {
    if (progress.badges[badge.slug]) continue
    let satisfied = false
    if (badge.rule_type === 'FIRST_REQUIREMENT_MET') {
      satisfied = state.phases.some((p) => p.met > 0)
    } else if (badge.rule_type === 'PHASE_COMPLIANT') {
      satisfied = state.phases.some(
        (p) => p.phase.slug === badge.rule_ref && p.compliant,
      )
    } else if (badge.rule_type === 'COURSE_COMPLIANT') {
      satisfied = state.courseCompliant
    }
    if (satisfied) {
      const stamp = now()
      progress.badges[badge.slug] = stamp
      remote?.awardBadge(badge.slug, stamp)
      nuevas.push(badgeSchema(badge, stamp))
    }
  }
  return nuevas
}

// --- Serializacion -----------------------------------------------------------
function phaseDetail(computed: ComputedPhase): PhaseDetail {
  const { phase } = computed
  return {
    id: phase.id,
    slug: phase.slug,
    name: phase.name,
    description: phase.description,
    order_index: phase.order_index,
    unlock_threshold: phase.unlock_threshold,
    theme: phase.theme,
    icon: phase.icon,
    state: {
      phase_id: phase.id,
      unlocked: computed.unlocked,
      percent: computed.percent,
      met: computed.met,
      failed: computed.total - computed.met,
      total_requirements: computed.total,
      compliant_nodes: computed.compliantNodes,
      total_nodes: computed.nodes.length,
      compliant: computed.compliant,
      unlock_threshold: phase.unlock_threshold,
      locked_reason: computed.unlocked ? null : LOCKED_BY_PHASE,
    },
    nodes: computed.nodes,
  }
}

function buildStateChange(progress: Progress, nodeId: number): StateChange {
  const state = computeState(progress)

  // Nivel recien abierto: se anuncia una sola vez.
  let unlockedPhase: ComputedPhase | null = null
  for (const phase of state.phases) {
    if (!phase.unlocked) continue
    if (progress.announced.includes(phase.phase.slug)) continue
    progress.announced.push(phase.phase.slug)
    if (phase.phase.order_index > 0 && unlockedPhase === null) unlockedPhase = phase
  }
  // Si un nivel deja de cumplir el umbral, se vuelve a anunciar cuando se recupere.
  progress.announced = progress.announced.filter((slug) =>
    state.phases.some((p) => p.phase.slug === slug && p.unlocked),
  )

  const nuevas = evaluateBadges(progress, state)
  const recalculated = computeState(progress)
  const node = recalculated.statuses[nodeId]
  const phase = recalculated.phases.find((p) => p.phase.id === node.phase_id)
  const previousName =
    unlockedPhase === null
      ? null
      : (recalculated.phases.find(
          (p) => p.phase.order_index === unlockedPhase!.phase.order_index - 1,
        )?.phase.name ?? null)

  save(progress)

  return {
    node_status: node.status,
    node_met: node.met,
    node_failed: node.failed,
    node_total: node.total_requirements,
    phase_progress: phase?.percent ?? 0,
    general_progress: recalculated.summary.general_progress,
    new_phase_unlocked: unlockedPhase !== null,
    unlocked_phase_id: unlockedPhase?.phase.id ?? null,
    unlocked_phase_name: unlockedPhase?.phase.name ?? null,
    previous_phase_name: previousName,
    new_badges: nuevas,
    course_compliant: recalculated.courseCompliant,
    next_node_id: recalculated.summary.next_node_id,
  }
}

function findNode(nodeId: number): RawNode {
  const node = ALL_NODES.find((n) => n.id === nodeId)
  if (!node) throw new Error('Este punto no existe en el recorrido.')
  return node
}

function ensureOpen(progress: Progress, nodeId: number): RawNode {
  const node = findNode(nodeId)
  const state = computeState(progress).statuses[nodeId]
  if (state.status === 'LOCKED') {
    throw new LockedError(
      state.locked_reason ?? 'Este punto todavia esta bloqueado.',
    )
  }
  return node
}

// --- API publica (misma forma que los servicios HTTP) ------------------------
export function getCourse(): CourseResponse {
  const state = computeState(load())
  return { phases: state.phases.map(phaseDetail), summary: state.summary }
}

export function getProgress(): ProgressResponse {
  const state = computeState(load())
  return {
    summary: state.summary,
    phases: state.phases.map((p) => phaseDetail(p).state),
    nodes: state.phases.flatMap((p) => p.nodes),
  }
}

export function getBadges(): BadgeCollection {
  const progress = load()
  const badges = COURSE.badges.map((badge) =>
    badgeSchema(badge, progress.badges[badge.slug] ?? null),
  )
  return {
    badges,
    earned: badges.filter((b) => b.earned).length,
    total: badges.length,
  }
}

export function getNodeDetail(nodeId: number): NodeDetail {
  const progress = load()
  const node = ensureOpen(progress, nodeId)
  const phase = COURSE.phases.find((p) => p.id === node.phase_id)!
  const state = computeState(progress).statuses[nodeId]
  const met = new Set(progress.metCodes)

  const requirements: Requirement[] = node.requirements.map((item) => ({
    code: item.code,
    title: item.title,
    detail: item.detail,
    meets: met.has(item.code),
  }))

  return {
    node: state,
    phase_id: phase.id,
    phase_name: phase.name,
    phase_theme: phase.theme,
    content: {
      objective: node.objective,
      body: node.body,
      vpo_block: node.vpo_block,
      requirements,
    },
  }
}

export interface RequirementUpdateResult {
  code: string
  meets: boolean
  state: StateChange
}

/** `true` marca el tema como cumplido; `false` lo vuelve al valor por defecto. */
export function setRequirement(
  nodeId: number,
  code: string,
  meets: boolean,
): RequirementUpdateResult {
  const progress = load()
  const node = ensureOpen(progress, nodeId)

  if (!node.requirements.some((r) => r.code === code)) {
    throw new Error('Ese tema no pertenece a este punto.')
  }

  const index = progress.metCodes.indexOf(code)
  if (meets) {
    if (index === -1) progress.metCodes.push(code)
    if (!progress.started_at) {
      progress.started_at = now()
      remote?.setStartedAt(progress.started_at)
    }
  } else if (index !== -1) {
    progress.metCodes.splice(index, 1)
  }
  remote?.setCode(code, meets)

  return { code, meets, state: buildStateChange(progress, nodeId) }
}

export function reset(): ProgressResponse {
  save(empty())
  remote?.reset()
  return getProgress()
}
