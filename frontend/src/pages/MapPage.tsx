import { useState } from 'react'
import { Award, CheckCircle2, Layers, Target, XCircle } from 'lucide-react'
import { GameMap } from '@/features/map/GameMap'
import { NodeModal } from '@/features/course/NodeModal'
import { StatCard } from '@/components/StatCard'
import { ContinueJourneyButton } from '@/components/ContinueJourneyButton'
import { ProgressBar } from '@/components/ProgressBar'
import { MascotGuide } from '@/components/MascotGuide'
import { ErrorState, MapSkeleton } from '@/components/Loaders'
import { useCourse } from '@/hooks/useCourse'
import type { StateChange } from '@/types/api'

/** Mensaje de la mascota segun el cumplimiento general. */
function mascotMessage(progress: number, cumple: boolean) {
  if (cumple) return 'Todos los niveles alcanzan su umbral de cumplimiento!'
  if (progress === 0) return 'Bienvenido! Todos los temas empiezan en "No cumple": activa los que sí cumplen.'
  if (progress < 40) return 'Vas bien. Sigue marcando los temas que sí cumplen.'
  if (progress < 80) return 'Buen avance. Cada vez quedan menos brechas.'
  return 'Estas muy cerca del umbral. Revisa las ultimas brechas.'
}

export function MapPage() {
  const { course, loading, error, refresh, applyStateChange } = useCourse()
  const [activeNodeId, setActiveNodeId] = useState<number | null>(null)

  if (loading) return <MapSkeleton />
  if (error) return <ErrorState message={error} onRetry={refresh} />
  if (!course) return null

  const { summary, phases } = course

  const handleMarked = async (change: StateChange) => {
    // El backend (o el motor local) ya recalculo: aqui solo se refresca.
    await applyStateChange(change)
    // Si el nivel siguiente acaba de abrirse, se cierra el punto para que la
    // celebracion quede a la vista.
    if (change.new_phase_unlocked) setActiveNodeId(null)
  }

  return (
    <div className="space-y-8">
      {/* Saludo */}
      <section className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="font-display text-3xl font-extrabold text-brand-ink sm:text-4xl">
            Ruta Utilities <span aria-hidden>👷</span>
          </h1>
          <p className="mt-1 text-lg font-semibold text-brand-slate">
            Recorrido de seguridad VPO para el area
          </p>
        </div>

        <ContinueJourneyButton
          nodeTitle={summary.next_node_title}
          disabled={summary.next_node_id === null}
          onClick={() => summary.next_node_id && setActiveNodeId(summary.next_node_id)}
        />
      </section>

      {/* Resumen general */}
      <section aria-label="Resumen de tu progreso" className="space-y-4">
        <div className="card-soft p-5">
          <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-xs font-extrabold uppercase tracking-wide text-brand-slate">
                Cumplimiento general
              </p>
              <p className="font-display text-4xl font-extrabold text-brand-ink">
                {summary.general_progress}%
              </p>
            </div>
            <p className="text-sm font-bold text-brand-slate">
              {summary.met_requirements} de {summary.total_requirements} temas
              cumplen
            </p>
          </div>
          <ProgressBar value={summary.general_progress} color="#F5B301" size="lg" />
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            index={0}
            icon={Layers}
            label="Nivel actual"
            value={summary.current_phase_name ?? 'Sin iniciar'}
            hint={`${summary.unlocked_phases} de ${summary.total_phases} niveles abiertos`}
            color="#2E8FEA"
            soft="#DCEDFD"
          />
          <StatCard
            index={1}
            icon={CheckCircle2}
            label="Temas que cumplen"
            value={`${summary.met_requirements} / ${summary.total_requirements}`}
            hint="Requisitos VPO cumplidos"
            color="#2FBF87"
            soft="#D6F6E7"
          />
          <StatCard
            index={2}
            icon={XCircle}
            label="Brechas"
            value={`${summary.failed_requirements}`}
            hint="Temas marcados como no cumple"
            color="#E5544B"
            soft="#FDE4E2"
          />
          <StatCard
            index={3}
            icon={Award}
            label="Insignias"
            value={`${summary.badges_earned} / ${summary.badges_total}`}
            hint="Logros obtenidos"
            color="#7C5CE0"
            soft="#E8E1FC"
          />
        </div>
      </section>

      <MascotGuide
        message={mascotMessage(summary.general_progress, summary.course_compliant)}
        mood={summary.course_compliant ? 'cheer' : 'happy'}
      />

      {/* Mapa */}
      <section aria-label="Mapa del recorrido" className="card-soft overflow-hidden p-2 sm:p-4">
        <div className="mb-2 flex flex-wrap items-center justify-between gap-2 px-3 pt-2">
          <h2 className="font-display text-2xl font-extrabold text-brand-ink">
            Tu recorrido
          </h2>
          <p className="flex items-center gap-1.5 text-sm font-bold text-brand-slate">
            <Target aria-hidden className="h-4 w-4" />
            Toca un punto para revisar sus temas
          </p>
        </div>

        <GameMap
          phases={phases}
          nextNodeId={summary.next_node_id}
          courseCompliant={summary.course_compliant}
          onSelectNode={setActiveNodeId}
        />
      </section>

      <NodeModal
        nodeId={activeNodeId}
        onClose={() => setActiveNodeId(null)}
        onMarked={handleMarked}
      />
    </div>
  )
}
