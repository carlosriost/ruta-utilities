/**
 * Cliente HTTP unico de la aplicacion.
 *
 * Ningun componente hace `fetch()` por su cuenta: todos pasan por aqui, que se
 * encarga del token de sesion, de los errores y de los mensajes amigables.
 */

const BASE_URL = (
  import.meta.env.VITE_API_URL ?? 'http://localhost:8001/api'
).replace(/\/$/, '')

const TOKEN_STORAGE_KEY = 'ruta-utilities.token'

/** Error de API con mensaje ya legible para el usuario. */
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

/**
 * El token demo se guarda en localStorage porque es SOLO sesion de interfaz.
 * El progreso, las respuestas y las insignias viven exclusivamente en
 * PostgreSQL: localStorage nunca es la fuente de verdad.
 */
export const tokenStorage = {
  get(): string | null {
    try {
      return window.localStorage.getItem(TOKEN_STORAGE_KEY)
    } catch {
      return null
    }
  },
  set(token: string): void {
    try {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, token)
    } catch {
      /* modo privado: la sesion durara solo lo que dure la pestana */
    }
  },
  clear(): void {
    try {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY)
    } catch {
      /* ignorado a proposito */
    }
  },
}

const FRIENDLY_NETWORK_ERROR = `No pudimos conectar con el servidor. Verifica que FastAPI este ejecutandose en ${new URL(BASE_URL, window.location.origin).origin}.`

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  body?: unknown
  signal?: AbortSignal
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, signal } = options
  const headers: Record<string, string> = { Accept: 'application/json' }

  const token = tokenStorage.get()
  if (token) headers.Authorization = `Bearer ${token}`
  if (body !== undefined) headers['Content-Type'] = 'application/json'

  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      signal,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch (error) {
    if ((error as Error).name === 'AbortError') throw error
    throw new ApiError(FRIENDLY_NETWORK_ERROR, 0)
  }

  if (response.status === 204) return undefined as T

  const raw = await response.text()
  const data = raw ? safeParse(raw) : null

  if (!response.ok) {
    throw new ApiError(extractMessage(data, response.status), response.status)
  }

  return data as T
}

function safeParse(raw: string): unknown {
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

/** Traduce la respuesta de FastAPI a un mensaje que se pueda mostrar. */
function extractMessage(data: unknown, status: number): string {
  const detail = (data as { detail?: unknown } | null)?.detail

  if (typeof detail === 'string') return detail

  // Errores de validacion de Pydantic (422): llegan como lista.
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0] as { msg?: string }
    if (first?.msg) return first.msg
  }

  switch (status) {
    case 401:
      return 'Tu sesion expiro. Vuelve a ingresar.'
    case 403:
      return 'Este punto del recorrido todavia esta bloqueado.'
    case 404:
      return 'No encontramos lo que buscabas.'
    case 409:
      return 'No pudimos guardar la marca de ese tema.'
    case 500:
      return 'Ocurrio un problema en el servidor. Intentalo de nuevo en un momento.'
    default:
      return 'Algo no salio como esperabamos. Intentalo nuevamente.'
  }
}

export const apiClient = {
  get: <T>(path: string, signal?: AbortSignal) => request<T>(path, { signal }),
  post: <T>(path: string, body?: unknown, signal?: AbortSignal) =>
    request<T>(path, { method: 'POST', body, signal }),
  put: <T>(path: string, body?: unknown, signal?: AbortSignal) =>
    request<T>(path, { method: 'PUT', body, signal }),
}
