import { useState } from 'react'
import { AlertTriangle, CheckCircle2, Lock, RotateCcw, XCircle } from 'lucide-react'
import { Button } from '@/components/Button'
import { Modal } from '@/components/Modal'
import { ProgressBar } from '@/components/ProgressBar'
import { ErrorState, MapSkeleton } from '@/components/Loaders'
import { useCourse } from '@/hooks/useCourse'
import { iconFor } from '@/utils/icons'
import { zoneTokens } from '@/utils/theme'
import type { NodeState } from '@/types/api'

const STATUS_META = {
  COMPLIANT: { label: 'Cumple', icon: CheckCircle2, className: 'text-state-success' },
  HAS_GAPS: { label: 'Con brechas', icon: XCircle, className: 'text-state-danger' },
  LOCKED: { label: 'Bloqueado', icon: Lock, className: 'text-state-locked' },
} as const

function NodeRow({ node }: { node: NodeState }) {
  const meta = STATUS_META[node.status]
  const StatusIcon = meta.icon
  const NodeIcon = iconFor(node.icon)

  return (
    <li className="flex items-center gap-3 border-t border-black/5 py-3 first:border-t-0">
      <span
        aria-hidden
        className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${
          node.status === 'LOCKED' ? 'bg-state-lockedsoft' : 'bg-brand-cream'
        }`}
      >
        <NodeIcon
          size={18}
          className={
            node.status === 'LOCKED' ? 'text-state-locked' : 'text-brand-ink'
          }
        />
      </span>

      <div className="min-w-0 flex-1">
        <p className="truncate font-bold text-brand-ink">{node.title}</p>
        <p className="text-xs font-semibold text-brand-slate">
          {node.met} de {node.total_requirements} temas cumplen
          {node.failed > 0 && ` · ${node.failed} no cumplen`}
        </p>
      </div>

      <span className={`flex items-center gap-1.5 text-sm font-bold ${meta.className}`}>
        <StatusIcon aria-hidden className="h-4 w-4" />
        <span className="hidden sm:inline">{meta.label}</span>
      </span>
    </li>
  )
}

// En GitHub Pages el avance es uno solo para todo el equipo.
const SHARED = import.meta.env.MODE === 'pages'

export function ProgressPage() {
  const { course, loading, error, refresh, resetProgress } = useCourse()
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [resetting, setResetting] = useState(false)
  const [resetError, setResetError] = useState<string | null>(null)

  const handleReset = async () => {
    setResetting(true)
    setResetError(null)
    try {
      await resetProgress()
      setConfirmOpen(false)
    } catch (err) {
      setResetError((err as Error).message ?? 'No pudimos reiniciar el progreso.')
    } finally {
      setResetting(false)
    }
  }

  if (loading) return <MapSkeleton />
  if (error) return <ErrorState message={error} onRetry={refresh} />
  if (!course) return null

  const { summary, phases } = course

  return (
    <div className="space-y-7">
      <header>
        <h1 className="font-display text-3xl font-extrabold text-brand-ink">
          Mi progreso
        </h1>
        <p className="mt-1 font-semibold text-brand-slate">
          Estado de los requisitos VPO por nivel de madurez.
        </p>
      </header>

      <section className="card-soft p-6">
        <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="text-xs font-extrabold uppercase tracking-wide text-brand-slate">
              Cumplimiento general
            </p>
            <p className="font-display text-5xl font-extrabold text-brand-ink">
              {summary.general_progress}%
            </p>
          </div>
          <p className="text-sm font-bold text-brand-slate">
            {summary.met_requirements} de {summary.total_requirements} temas cumplen
          </p>
        </div>
        <ProgressBar value={summary.general_progress} color="#F5B301" size="lg" />
      </section>

      <section className="space-y-5">
        {phases.map((phase) => {
          const tokens = zoneTokens(phase.theme)
          return (
            <article key={phase.id} className="card-soft overflow-hidden">
              <header
                className="flex flex-wrap items-center gap-4 p-5"
                style={{ backgroundColor: tokens.soft }}
              >
                <div className="min-w-0 flex-1">
                  <p
                    className="text-xs font-extrabold uppercase tracking-[0.16em]"
                    style={{ color: tokens.deep }}
                  >
                    Nivel VPO {phase.order_index}
                    {!phase.state.unlocked && ' · bloqueado'}
                  </p>
                  <h2 className="font-display text-2xl font-extrabold text-brand-ink">
                    {phase.name}
                  </h2>
                  <p className="mt-0.5 text-sm font-semibold text-brand-slate">
                    {phase.state.met} de {phase.state.total_requirements} temas
                    cumplen · {phase.state.percent}%
                    {' · '}abre el siguiente con {phase.unlock_threshold}%
                  </p>
                </div>
                <div className="w-full sm:w-56">
                  <ProgressBar
                    value={phase.state.percent}
                    color={phase.state.unlocked ? tokens.main : '#B7C0D0'}
                    threshold={phase.unlock_threshold}
                    label={
                      phase.state.compliant ? 'Umbral alcanzado' : 'Cumplimiento'
                    }
                    showValue
                    size="md"
                  />
                </div>
              </header>

              <ul className="px-5 pb-4">
                {phase.nodes.map((node) => (
                  <NodeRow key={node.id} node={node} />
                ))}
              </ul>
            </article>
          )
        })}
      </section>

      {/* Reinicio del recorrido */}
      <section className="card-soft border-2 border-dashed border-state-danger/25 p-6">
        <h2 className="flex items-center gap-2 font-display text-xl font-extrabold text-brand-ink">
          <RotateCcw aria-hidden className="h-5 w-5 text-state-danger" />
          Reiniciar el recorrido
        </h2>
        <p className="mt-1 max-w-2xl text-sm font-semibold text-brand-slate">
          Borra tu avance y vuelve a empezar desde el primer punto. El contenido
          del curso no se toca.
        </p>
        <Button
          variant="danger"
          className="mt-4"
          onClick={() => setConfirmOpen(true)}
          icon={<RotateCcw aria-hidden className="h-4 w-4" />}
        >
          Reiniciar mi progreso
        </Button>
      </section>

      <Modal
        open={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        labelledBy="reset-title"
        size="md"
      >
        <div className="p-6 text-center sm:p-8">
          <span
            aria-hidden
            className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-state-danger/10"
          >
            <AlertTriangle className="h-8 w-8 text-state-danger" />
          </span>
          <h2 id="reset-title" className="font-display text-2xl font-extrabold text-brand-ink">
            Reiniciar el recorrido
          </h2>
          <p className="mx-auto mt-2 max-w-sm font-semibold text-brand-slate">
            Se borrara todo tu avance: puntos completados, respuestas e
            insignias. Esta accion no se puede deshacer.
          </p>
          {SHARED && (
            <p className="mx-auto mt-2 max-w-sm text-sm font-bold text-state-danger">
              El avance es compartido: se borrara para todas las personas que
              usan este link.
            </p>
          )}
          {resetError && (
            <p role="alert" className="mt-3 text-sm font-bold text-state-danger">
              {resetError}
            </p>
          )}
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button variant="secondary" onClick={() => setConfirmOpen(false)}>
              Cancelar
            </Button>
            <Button variant="danger" loading={resetting} onClick={handleReset}>
              Si, reiniciar
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
