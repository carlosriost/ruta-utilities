import { apiClient } from './apiClient'
import type {
  CourseResponse,
  NodeDetail,
  PhaseDetail,
  RequirementUpdate,
} from '@/types/api'

/** Todo lo relacionado con el mapa y el marcado de temas. */
export const courseApi = {
  getCourse: (signal?: AbortSignal) =>
    apiClient.get<CourseResponse>('/course', signal),

  getPhases: (signal?: AbortSignal) =>
    apiClient.get<PhaseDetail[]>('/phases', signal),

  getPhase: (phaseId: number, signal?: AbortSignal) =>
    apiClient.get<PhaseDetail>(`/phases/${phaseId}`, signal),

  getNode: (nodeId: number, signal?: AbortSignal) =>
    apiClient.get<NodeDetail>(`/nodes/${nodeId}`, signal),

  /** `true` marca el tema como cumplido; `false` lo vuelve al valor por defecto. */
  setRequirement: (nodeId: number, code: string, meets: boolean) =>
    apiClient.put<RequirementUpdate>(`/nodes/${nodeId}/requirements/${code}`, {
      meets,
    }),
}
