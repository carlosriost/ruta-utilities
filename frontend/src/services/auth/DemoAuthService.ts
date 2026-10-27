import { ApiError, tokenStorage } from '../apiClient'
import { authApi } from '../authApi'
import type { AuthService } from './AuthService'
import type { User } from '@/types/api'

/**
 * Autenticacion de demostracion.
 *
 * No pide correo ni contrasena: llama a `POST /api/auth/demo-login`, que busca
 * al unico usuario en PostgreSQL y devuelve un token de sesion.
 */
export class DemoAuthService implements AuthService {
  readonly providerName = 'Demo'

  async signIn(): Promise<User> {
    const response = await authApi.demoLogin()
    tokenStorage.set(response.access_token)
    return response.user
  }

  async restoreSession(): Promise<User | null> {
    if (!tokenStorage.get()) return null
    try {
      return await authApi.getMe()
    } catch (error) {
      if (error instanceof ApiError && error.isUnauthorized) {
        tokenStorage.clear()
        return null
      }
      throw error
    }
  }

  async signOut(): Promise<void> {
    tokenStorage.clear()
  }
}
