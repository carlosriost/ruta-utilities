/**
 * Sustituto del cliente HTTP para la version descargable.
 *
 * No hay red: solo se conserva el tipo de error, para que los componentes
 * distingan un punto bloqueado igual que en la version servida por API.
 */

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }

  get isUnauthorized(): boolean {
    return this.status === 401
  }

  get isLocked(): boolean {
    return this.status === 403
  }
}

/** Sin sesion que guardar: existe solo para mantener la misma interfaz. */
export const tokenStorage = {
  get: (): string | null => null,
  set: (): void => {},
  clear: (): void => {},
}
