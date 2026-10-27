/**
 * Version offline de `services/courseApi`.
 *
 * Misma forma y misma firma que el cliente HTTP, pero resolviendo contra el
 * motor local. Vite lo sustituye mediante un alias al compilar el archivo
 * descargable, de modo que ningun componente necesita cambiar.
 */

import type { CourseResponse, NodeDetail, PhaseDetail, RequirementUpdate } from '@/types/api'
import { ApiError } from './apiClient'
import * as engine from './engine'

async function run<T>(action: () => T): Promise<T> {
  try {
    return action()
  } catch (error) {
    // Se reutilizan los codigos HTTP para que la interfaz reaccione igual que
    // con la API: 403 cuando el punto aun no esta accesible.
    const status = error instanceof engine.LockedError ? 403 : 409
    throw new ApiError((error as Error).message, status)
  }
}

export const courseApi = {
  getCourse: (_signal?: AbortSignal): Promise<CourseResponse> =>
    run(() => engine.getCourse()),

  getPhases: (_signal?: AbortSignal): Promise<PhaseDetail[]> =>
    run(() => engine.getCourse().phases),

  getPhase: (phaseId: number, _signal?: AbortSignal): Promise<PhaseDetail> =>
    run(() => {
      const phase = engine.getCourse().phases.find((p) => p.id === phaseId)
      if (!phase) throw new Error('Ese nivel no existe.')
      return phase
    }),

  getNode: (nodeId: number, _signal?: AbortSignal): Promise<NodeDetail> =>
    run(() => engine.getNodeDetail(nodeId)),

  setRequirement: (
    nodeId: number,
    code: string,
    meets: boolean,
  ): Promise<RequirementUpdate> => run(() => engine.setRequirement(nodeId, code, meets)),
}
