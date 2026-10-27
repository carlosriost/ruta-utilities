/**
 * Tipos que reflejan los schemas del backend.
 *
 * El frontend NO define reglas: solo describe la forma del estado que recibe,
 * venga de FastAPI o del motor local de la version descargable.
 */

/** Un tema es binario: bloqueado, cumple todo o tiene brechas. No hay "sin marcar". */
export type NodeStatus = 'LOCKED' | 'COMPLIANT' | 'HAS_GAPS'

export type ZoneTheme = 'mint' | 'sky' | 'amber' | 'grape' | 'teal'

export interface User {
  id: number
  name: string
  area: string
  plant: string
  role: string
  email: string | null
  created_at: string
}

export interface DemoLoginResponse {
  access_token: string
  token_type: string
  auth_provider: string
  user: User
}

export interface NodeState {
  id: number
  phase_id: number
  slug: string
  title: string
  description: string
  icon: string
  order_index: number
  total_requirements: number
  met: number
  failed: number
  status: NodeStatus
  locked_reason: string | null
}

export interface PhaseState {
  phase_id: number
  unlocked: boolean
  /** Cumplimiento: temas cumplidos sobre el total del nivel. */
  percent: number
  met: number
  failed: number
  total_requirements: number
  /** Puntos donde todos los temas cumplen. */
  compliant_nodes: number
  total_nodes: number
  /** El nivel alcanza su umbral de cumplimiento. */
  compliant: boolean
  unlock_threshold: number
  locked_reason: string | null
}

export interface PhaseDetail {
  id: number
  slug: string
  name: string
  description: string
  order_index: number
  unlock_threshold: number
  theme: ZoneTheme
  icon: string
  state: PhaseState
  nodes: NodeState[]
}

export interface ProgressSummary {
  general_progress: number
  met_requirements: number
  failed_requirements: number
  total_requirements: number
  compliant_nodes: number
  total_nodes: number
  badges_earned: number
  badges_total: number
  current_phase_id: number | null
  current_phase_name: string | null
  next_node_id: number | null
  next_node_title: string | null
  unlocked_phases: number
  total_phases: number
  started_at: string | null
  course_compliant: boolean
}

export interface CourseResponse {
  phases: PhaseDetail[]
  summary: ProgressSummary
}

export interface ProgressResponse {
  summary: ProgressSummary
  phases: PhaseState[]
  nodes: NodeState[]
}

export interface Badge {
  id: number
  slug: string
  name: string
  description: string
  icon: string
  theme: string
  earned: boolean
  awarded_at: string | null
}

export interface BadgeCollection {
  badges: Badge[]
  earned: number
  total: number
}

export interface StateChange {
  node_status: NodeStatus
  node_met: number
  node_failed: number
  node_total: number
  phase_progress: number
  general_progress: number
  new_phase_unlocked: boolean
  unlocked_phase_id: number | null
  unlocked_phase_name: string | null
  previous_phase_name: string | null
  new_badges: Badge[]
  course_compliant: boolean
  next_node_id: number | null
}

/** Un tema: el requisito VPO con su marca actual. Sin marcar = no cumple. */
export interface Requirement {
  code: string
  title: string
  detail: string
  meets: boolean
}

export interface NodeContent {
  objective: string
  body: string
  /** Nombre oficial del bloque VPO, en ingles, para trazabilidad. */
  vpo_block: string | null
  requirements: Requirement[]
}

export interface NodeDetail {
  node: NodeState
  phase_id: number
  phase_name: string
  phase_theme: ZoneTheme
  content: NodeContent
}

export interface RequirementUpdate {
  code: string
  meets: boolean
  state: StateChange
}
