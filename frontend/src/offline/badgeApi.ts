import type { BadgeCollection } from '@/types/api'
import * as engine from './engine'

export const badgeApi = {
  getMine: async (_signal?: AbortSignal): Promise<BadgeCollection> =>
    engine.getBadges(),
}
