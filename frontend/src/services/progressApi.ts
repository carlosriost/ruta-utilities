import { apiClient } from './apiClient'
import type { ProgressResponse } from '@/types/api'

export const progressApi = {
  getMine: (signal?: AbortSignal) =>
    apiClient.get<ProgressResponse>('/progress/me', signal),

  /** Reinicia el progreso de la demo (el catalogo del curso se conserva). */
  resetProgress: () => apiClient.post<ProgressResponse>('/demo/reset'),
}
