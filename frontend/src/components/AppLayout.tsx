import { Outlet } from 'react-router-dom'
import { UserHeader } from './UserHeader'
import { DevTools } from './DevTools'
import { UnlockModal } from '@/features/progress/UnlockModal'
import { BadgeCelebration } from '@/features/badges/BadgeCelebration'
import { useCourse } from '@/hooks/useCourse'

/**
 * Marco comun de la aplicacion: cabecera, contenido y las celebraciones
 * globales (nuevo nivel, insignias). No hay sesion ni datos personales.
 */
export function AppLayout() {
  const { unlockEvent, dismissUnlock, celebratedBadges, dismissBadges } = useCourse()

  return (
    <div className="sky-bg min-h-screen">
      <a
        href="#contenido"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-pill focus:bg-brand-blue focus:px-5 focus:py-2.5 focus:font-bold focus:text-white"
      >
        Saltar al contenido
      </a>

      <UserHeader />

      <main id="contenido" className="mx-auto w-full max-w-6xl px-4 pb-20 pt-6">
        <Outlet />
      </main>

      <UnlockModal event={unlockEvent} onClose={dismissUnlock} />
      <BadgeCelebration badges={celebratedBadges} onDismiss={dismissBadges} />

      {import.meta.env.DEV && <DevTools />}
    </div>
  )
}
