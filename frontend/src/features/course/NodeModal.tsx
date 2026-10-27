import { useCallback, useEffect, useState } from 'react'
import { Check, Lock, Target, X } from 'lucide-react'
import { Modal } from '@/components/Modal'
import { Button } from '@/components/Button'
import { ErrorState, SkeletonBlock } from '@/components/Loaders'
import { courseApi } from '@/services/courseApi'
import { ApiError } from '@/services/apiClient'
import { useCourse } from '@/hooks/useCourse'
import { iconFor } from '@/utils/icons'
import { zoneTokens } from '@/utils/theme'
import { toParagraphs } from '@/utils/format'
import type { NodeDetail, Requirement, StateChange } from '@/types/api'

// En GitHub Pages el avance es compartido y puede cambiar desde otro equipo.
const SHARED = import.meta.env.MODE === 'pages'

interface NodeModalProps {
  nodeId: number | null
  onClose: () => void
  /** Se invoca con el estado recalculado cada vez que se marca un tema. */
  onMarked: (change: StateChange) => void | Promise<void>
}

/**
 * Un punto del mapa: su contexto y la lista de temas.
 *
 * Cada tema es un interruptor: empieza en "No cumple" (el valor por defecto)
 * y se activa a "Cumple" cuando la planta lo tiene resuelto. No hay un tercer
 * estado de "sin marcar": todo tema cuenta desde el principio, para que el
 * mapa muestre siempre la situacion real, no lo que falta por revisar.
 */
export function NodeModal({ nodeId, onClose, onMarked }: NodeModalProps) {
  const [detail, setDetail] = useState<NodeDetail | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState<string | null>(null)

  const load = useCallback(async () => {
    if (nodeId === null) return
    setLoading(true)
    setError(null)
    try {
      setDetail(await courseApi.getNode(nodeId))
    } catch (err) {
      setError(
        err instanceof ApiError ? err.message : 'No pudimos abrir este punto.',
      )
    } finally {
      setLoading(false)
    }
  }, [nodeId])

  useEffect(() => {
    if (nodeId === null) {
      setDetail(null)
      setError(null)
      return
    }
    void load()
  }, [nodeId, load])

  // Si otra persona marca temas de este mismo punto, el mapa se actualiza y
  // aqui se vuelve a leer el detalle sin mostrar la carga.
  const { course } = useCourse()
  useEffect(() => {
    if (!SHARED || nodeId === null) return
    courseApi.getNode(nodeId).then(setDetail).catch(() => {})
  }, [course, nodeId])

  const tokens = zoneTokens(detail?.phase_theme)
  const Icon = iconFor(detail?.node.icon)

  const marcar = async (code: string, meets: boolean) => {
    if (nodeId === null) return
    setSaving(code)
    setError(null)
    try {
      const result = await courseApi.setRequirement(nodeId, code, meets)
      // El backend (o el motor local) manda: se aplica lo que devuelve.
      setDetail((current) => {
        if (current === null) return current
        const requirements = current.content.requirements.map((item) =>
          item.code === code ? { ...item, meets: result.meets } : item,
        )
        return {
          ...current,
          node: {
            ...current.node,
            met: result.state.node_met,
            failed: result.state.node_failed,
            status: result.state.node_status,
          },
          content: { ...current.content, requirements },
        }
      })
      await onMarked(result.state)
    } catch (err) {
      setError(
        err instanceof ApiError ? err.message : 'No pudimos guardar la marca.',
      )
    } finally {
      setSaving(null)
    }
  }

  const requirements = detail?.content.requirements ?? []
  const cumplidos = requirements.filter((r) => r.meets).length
  const noCumplidos = requirements.length - cumplidos

  return (
    <Modal open={nodeId !== null} onClose={onClose} labelledBy="node-title" size="lg">
      <div className="max-h-[88vh] overflow-y-auto">
        {/* Cabecera */}
        <header
          className="px-6 pb-6 pt-7 sm:px-8"
          style={{ backgroundColor: detail ? tokens.soft : '#F2F5F9' }}
        >
          {loading && !detail ? (
            <div className="space-y-3">
              <SkeletonBlock className="h-5 w-32" />
              <SkeletonBlock className="h-8 w-2/3" />
            </div>
          ) : detail ? (
            <div className="flex items-start gap-4 pr-10">
              <span
                aria-hidden
                className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl shadow-soft"
                style={{ backgroundColor: tokens.main }}
              >
                <Icon className="h-7 w-7 text-white" strokeWidth={2.3} />
              </span>
              <div className="min-w-0">
                <p
                  className="text-xs font-extrabold uppercase tracking-[0.16em]"
                  style={{ color: tokens.deep }}
                >
                  {detail.phase_name}
                </p>
                <h2
                  id="node-title"
                  className="mt-1 text-2xl font-extrabold leading-tight text-brand-ink"
                >
                  {detail.node.title}
                </h2>
                {detail.content.vpo_block && (
                  <p className="mt-1 text-sm font-bold text-brand-slate">
                    Bloque VPO: {detail.content.vpo_block}
                  </p>
                )}
              </div>
            </div>
          ) : null}
        </header>

        <div className="px-6 py-6 sm:px-8">
          {loading && !detail && (
            <div className="space-y-3" role="status" aria-live="polite">
              <span className="sr-only">Cargando punto</span>
              <SkeletonBlock className="h-4 w-full" />
              <SkeletonBlock className="h-4 w-11/12" />
              <SkeletonBlock className="mt-6 h-20 w-full rounded-2xl" />
              <SkeletonBlock className="h-20 w-full rounded-2xl" />
            </div>
          )}

          {error && !detail && (
            <div className="py-4">
              {error.toLowerCase().includes('nivel anterior') ? (
                <div className="text-center">
                  <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-state-lockedsoft">
                    <Lock aria-hidden className="h-7 w-7 text-state-locked" />
                  </div>
                  <h3 className="mb-1 text-xl font-extrabold">Punto bloqueado</h3>
                  <p className="text-brand-slate">{error}</p>
                </div>
              ) : (
                <ErrorState message={error} onRetry={load} />
              )}
            </div>
          )}

          {detail && (
            <div className="space-y-6">
              {detail.content.objective && (
                <div
                  className="flex items-start gap-3 rounded-2xl p-4"
                  style={{ backgroundColor: tokens.soft }}
                >
                  <Target
                    aria-hidden
                    className="mt-0.5 h-5 w-5 shrink-0"
                    style={{ color: tokens.deep }}
                  />
                  <p className="text-sm font-bold" style={{ color: tokens.deep }}>
                    {detail.content.objective}
                  </p>
                </div>
              )}

              {detail.content.body && (
                <div className="space-y-3 text-[15px] leading-relaxed text-brand-ink/85">
                  {toParagraphs(detail.content.body).map((paragraph, index) => (
                    <p key={index} className="whitespace-pre-line">
                      {paragraph}
                    </p>
                  ))}
                </div>
              )}

              <section aria-label="Temas del punto" className="space-y-3">
                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <h3 className="font-display text-lg font-extrabold text-brand-ink">
                    {requirements.length === 1
                      ? '1 tema'
                      : `${requirements.length} temas`}
                  </h3>
                  <p className="text-sm font-bold text-brand-slate">
                    Todos empiezan en "No cumple": activa los que sí cumplen
                  </p>
                </div>

                <ul className="space-y-3">
                  {requirements.map((requirement) => (
                    <RequirementRow
                      key={requirement.code}
                      requirement={requirement}
                      tokens={tokens}
                      saving={saving === requirement.code}
                      onToggle={() => marcar(requirement.code, !requirement.meets)}
                    />
                  ))}
                </ul>
              </section>

              {error && (
                <p role="alert" className="text-sm font-semibold text-state-danger">
                  {error}
                </p>
              )}

              {/* Resumen del punto */}
              <div className="flex flex-wrap items-center gap-4 border-t border-black/5 pt-5">
                <p className="mr-auto text-sm font-bold text-brand-slate">
                  <span className="text-state-success">{cumplidos} cumplen</span>
                  {' · '}
                  <span className="text-state-danger">{noCumplidos} no cumplen</span>
                </p>
                <Button onClick={onClose} size="lg" variant="gold">
                  Listo
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </Modal>
  )
}

function RequirementRow({
  requirement,
  tokens,
  saving,
  onToggle,
}: {
  requirement: Requirement
  tokens: ReturnType<typeof zoneTokens>
  saving: boolean
  onToggle: () => void
}) {
  const { meets } = requirement

  return (
    <li
      className={`rounded-2xl border-2 p-4 transition ${
        meets
          ? 'border-state-success/40 bg-state-success/5'
          : 'border-state-danger/30 bg-state-danger/5'
      }`}
    >
      <div className="flex flex-wrap items-start gap-x-2 gap-y-1">
        <code
          className="rounded-md px-1.5 py-0.5 font-mono text-xs font-bold"
          style={{ backgroundColor: tokens.soft, color: tokens.deep }}
        >
          {requirement.code}
        </code>
        <p className="min-w-0 flex-1 font-bold text-brand-ink">{requirement.title}</p>
      </div>

      <p className="mt-1.5 text-sm leading-relaxed text-brand-ink/75">
        {requirement.detail}
      </p>

      <button
        type="button"
        role="switch"
        aria-checked={meets}
        aria-label={`${requirement.code}: ${meets ? 'cumple' : 'no cumple'}. Cambiar.`}
        disabled={saving}
        onClick={onToggle}
        className={`mt-3 flex w-full items-center gap-3 rounded-2xl border-2 px-4 py-3 text-left font-extrabold transition disabled:opacity-60 sm:w-auto ${
          meets
            ? 'border-state-success bg-state-success text-white shadow-soft'
            : 'border-state-danger bg-state-danger text-white shadow-soft'
        }`}
      >
        <span
          aria-hidden
          className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-white/25"
        >
          {meets ? (
            <Check className="h-4 w-4" strokeWidth={3} />
          ) : (
            <X className="h-4 w-4" strokeWidth={3} />
          )}
        </span>
        {meets ? 'Cumple' : 'No cumple'}
        <span className="ml-auto text-xs font-bold opacity-80 sm:ml-2">
          Toca para cambiar
        </span>
      </button>
    </li>
  )
}
