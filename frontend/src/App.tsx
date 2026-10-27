import { useEffect } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from '@/components/AppLayout'
import { CourseProvider } from '@/context/CourseContext'
import { useAuth } from '@/hooks/useAuth'
import { MapPage } from '@/pages/MapPage'
import { ProgressPage } from '@/pages/ProgressPage'
import { BadgesPage } from '@/pages/BadgesPage'
import { AboutPage } from '@/pages/AboutPage'
import { ErrorState, Spinner } from '@/components/Loaders'

/**
 * Version servida por la API.
 *
 * No hay pantalla de inicio de sesion: la aplicacion abre directamente en el
 * mapa y la sesion tecnica se resuelve sola. El recorrido es igual para todos
 * los operarios y en ningun momento se muestran datos personales.
 */
function CourseArea() {
  const { status, error, signIn } = useAuth()

  useEffect(() => {
    if (status === 'anonymous') void signIn()
  }, [status, signIn])

  if (status !== 'authenticated') {
    return (
      <div className="sky-bg flex min-h-screen items-center justify-center p-6">
        {error ? (
          <ErrorState message={error} onRetry={signIn} />
        ) : (
          <Spinner label="Preparando el recorrido" />
        )}
      </div>
    )
  }

  return (
    <CourseProvider>
      <AppLayout />
    </CourseProvider>
  )
}

export default function App() {
  return (
    <Routes>
      <Route element={<CourseArea />}>
        <Route path="/mapa" element={<MapPage />} />
        <Route path="/progreso" element={<ProgressPage />} />
        <Route path="/insignias" element={<BadgesPage />} />
        <Route path="/acerca" element={<AboutPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/mapa" replace />} />
    </Routes>
  )
}
