import { apiClient } from './apiClient'
import type { DemoLoginResponse, User } from '@/types/api'

export const authApi = {
  demoLogin: () => apiClient.post<DemoLoginResponse>('/auth/demo-login'),
  getMe: (signal?: AbortSignal) => apiClient.get<User>('/users/me', signal),
}
