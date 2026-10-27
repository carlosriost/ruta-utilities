import type { ProgressResponse } from '@/types/api'
import * as engine from './engine'

export const progressApi = {
  getMine: async (_signal?: AbortSignal): Promise<ProgressResponse> =>
    engine.getProgress(),

  /** Reinicia el avance guardado en este navegador. */
  resetProgress: async (): Promise<ProgressResponse> => engine.reset(),
}
