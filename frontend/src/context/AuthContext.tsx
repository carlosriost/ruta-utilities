import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { DemoAuthService } from '@/services/auth/DemoAuthService'
import type { AuthService } from '@/services/auth/AuthService'
import { ApiError } from '@/services/apiClient'
import type { User } from '@/types/api'

/**
 * Para migrar a Microsoft Entra ID basta con cambiar esta linea por
 * `new MicrosoftEntraAuthService()`. El resto de la aplicacion no se entera.
 */
const authService: AuthService = new DemoAuthService()

interface AuthContextValue {
  user: User | null
  status: 'loading' | 'authenticated' | 'anonymous'
  error: string | null
  providerName: string
  signIn: () => Promise<void>
  signOut: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [status, setStatus] = useState<AuthContextValue['status']>('loading')
  const [error, setError] = useState<string | null>(null)

  // Al cargar la app intentamos recuperar la sesion contra el backend.
  useEffect(() => {
    let active = true
    authService
      .restoreSession()
      .then((restored) => {
        if (!active) return
        setUser(restored)
        setStatus(restored ? 'authenticated' : 'anonymous')
      })
      .catch((err: unknown) => {
        if (!active) return
        setError(err instanceof ApiError ? err.message : null)
        setStatus('anonymous')
      })
    return () => {
      active = false
    }
  }, [])

  const signIn = useCallback(async () => {
    setError(null)
    try {
      const signedIn = await authService.signIn()
      setUser(signedIn)
      setStatus('authenticated')
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : 'No pudimos iniciar la sesion de demostracion.',
      )
      throw err
    }
  }, [])

  const signOut = useCallback(async () => {
    await authService.signOut()
    setUser(null)
    setStatus('anonymous')
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      status,
      error,
      providerName: authService.providerName,
      signIn,
      signOut,
    }),
    [user, status, error, signIn, signOut],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
