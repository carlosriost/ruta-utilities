import { apiClient } from './apiClient'
import type { BadgeCollection } from '@/types/api'

export const badgeApi = {
  getMine: (signal?: AbortSignal) =>
    apiClient.get<BadgeCollection>('/badges/me', signal),
}
