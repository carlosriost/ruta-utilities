import { useEffect, useState } from 'react'
import { badgeApi } from '@/services/badgeApi'
import { ApiError } from '@/services/apiClient'
import { BadgeCard } from '@/features/badges/BadgeCard'
import { ErrorState, SkeletonBlock } from '@/components/Loaders'
import { ProgressBar } from '@/components/ProgressBar'
import { MascotGuide } from '@/components/MascotGuide'
import { useCourse } from '@/hooks/useCourse'
import type { BadgeCollection } from '@/types/api'

export function BadgesPage() {
  const { course } = useCourse()
  const [collection, setCollection] = useState<BadgeCollection | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = () => {
    setLoading(true)
    setError(null)
    badgeApi
      .getMine()
      .then(setCollection)
      .catch((err: unknown) =>
        setError(
          err instanceof ApiError
            ? err.message
            : 'No pudimos cargar tus insignias.',
        ),
      )
      .finally(() => setLoading(false))
  }

  // Se recarga cuando cambia el progreso para reflejar logros recien obtenidos.
  useEffect(load, [course?.summary.met_requirements])

  if (error) return <ErrorState message={error} onRetry={load} />

  const percent = collection
    ? Math.round((collection.earned * 100) / Math.max(collection.total, 1))
    : 0

  return (
    <div className="space-y-7">
      <header>
        <h1 className="font-display text-3xl font-extrabold text-brand-ink">
          Insignias
        </h1>
        <p className="mt-1 font-semibold text-brand-slate">
          Logros que otorga el backend al cumplir las reglas del recorrido.
        </p>
      </header>

      <section className="card-soft p-6">
        {loading && !collection ? (
          <SkeletonBlock className="h-16 w-full" />
        ) : (
          <>
            <div className="mb-3 flex flex-wrap items-end justify-between gap-3">
              <p className="font-display text-3xl font-extrabold text-brand-ink">
                {collection?.earned ?? 0}{' '}
                <span className="text-lg font-bold text-brand-slate">
                  de {collection?.total ?? 0} insignias
                </span>
              </p>
              <p className="text-sm font-bold text-brand-slate">{percent}% de la coleccion</p>
            </div>
            <ProgressBar value={percent} color="#7C5CE0" size="lg" />
          </>
        )}
      </section>

      <MascotGuide
        mood={percent === 100 ? 'cheer' : 'hint'}
        message={
          percent === 100
            ? 'Coleccion completa. Eres Maestro Utilities!'
            : 'Completa zonas enteras para desbloquear mas insignias.'
        }
      />

      <section
        aria-label="Coleccion de insignias"
        className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
      >
        {loading && !collection
          ? [0, 1, 2, 3, 4].map((i) => (
              <SkeletonBlock key={i} className="h-64 rounded-card" />
            ))
          : collection?.badges.map((badge, index) => (
              <BadgeCard key={badge.id} badge={badge} index={index} />
            ))}
      </section>
    </div>
  )
}
