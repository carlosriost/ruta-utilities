import type { User } from '@/types/api'

/**
 * Contrato de autenticacion del frontend.
 *
 * Hoy lo implementa `DemoAuthService`. Cuando llegue Microsoft Entra ID se
 * anade `MicrosoftEntraAuthService` cumpliendo esta misma interfaz y se cambia
 * una sola linea en `AuthProvider`: ningun componente ni pantalla se modifica.
 *
 *   AuthService (interfaz)
 *     |- DemoAuthService              (esta version)
 *     |- MicrosoftEntraAuthService    (futuro: MSAL + token corporativo)
 */
export interface AuthService {
  /** Nombre del proveedor, util para mostrarlo en la interfaz. */
  readonly providerName: string

  /** Inicia sesion y devuelve el usuario ya resuelto por el backend. */
  signIn(): Promise<User>

  /** Recupera la sesion existente al recargar la pagina, si la hay. */
  restoreSession(): Promise<User | null>

  /** Cierra la sesion local. */
  signOut(): Promise<void>
}
