import { Loader2, WifiOff } from 'lucide-react'
import { Button } from './Button'

/** Spinner accesible para acciones puntuales. */
export function Spinner({ label = 'Cargando' }: { label?: string }) {
  return (
    <span className="inline-flex items-center gap-2 text-brand-slate" role="status">
      <Loader2 aria-hidden className="h-5 w-5 animate-spin" />
      <span className="text-sm font-semibold">{label}</span>
    </span>
  )
}

export function SkeletonBlock({ className = '' }: { className?: string }) {
  return <div aria-hidden className={`skeleton ${className}`} />
}

/** Esqueleto del mapa mientras FastAPI responde: nunca una pantalla vacia. */
export function MapSkeleton() {
  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-8" role="status" aria-live="polite">
      <span className="sr-only">Cargando tu recorrido</span>
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[0, 1, 2, 3].map((i) => (
          <SkeletonBlock key={i} className="h-24 rounded-card" />
        ))}
      </div>
      <SkeletonBlock className="mb-6 h-14 w-2/3 rounded-card" />
      <div className="space-y-10">
        {[0, 1, 2].map((zone) => (
          <div key={zone} className="space-y-5">
            <SkeletonBlock className="h-9 w-52 rounded-pill" />
            <div className="flex flex-wrap justify-center gap-8">
              {[0, 1, 2, 3].map((node) => (
                <SkeletonBlock key={node} className="h-20 w-20 rounded-full" />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

interface ErrorStateProps {
  message: string
  onRetry?: () => void
}

/** Estado de error amigable: nunca se muestra un stack trace de Python. */
export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="mx-auto max-w-lg px-4 py-16 text-center" role="alert">
      <div className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-zone-ambersoft">
        <WifiOff aria-hidden className="h-9 w-9 text-zone-amber" />
      </div>
      <h2 className="mb-2 text-2xl font-extrabold">Algo se interpuso en el camino</h2>
      <p className="mb-6 text-brand-slate">{message}</p>
      {onRetry && (
        <Button onClick={onRetry} variant="primary" size="lg">
          Reintentar
        </Button>
      )}
    </div>
  )
}
