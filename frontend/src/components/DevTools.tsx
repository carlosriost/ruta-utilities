import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Check, FlaskConical, RotateCcw, X } from 'lucide-react'
import { courseApi } from '@/services/courseApi'
import type { StateChange } from '@/types/api'
import { useCourse } from '@/hooks/useCourse'
import { Button } from './Button'

/**
 * Herramientas de desarrollo.
 *
 * Solo se montan cuando `import.meta.env.DEV` es verdadero, asi que nunca
 * llegan a produccion. Importante: TODAS marcan los temas por la via normal;
 * ninguna modifica el estado de React por su cuenta.
 */
export function DevTools() {
  const { course, applyStateChange, resetProgress, refresh } = useCourse()
  const [open, setOpen] = useState(false)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState<string | null>(null)

  const nextNodeId = course?.summary.next_node_id ?? null

  const run = async (label: string, action: () => Promise<void>) => {
    setBusy(true)
    setMessage(null)
    try {
      await action()
      setMessage(label)
    } catch (error) {
      setMessage((error as Error).message)
    } finally {
      setBusy(false)
    }
  }

  /** Marca todos los temas de un punto y devuelve el ultimo estado. */
  const marcarPunto = async (nodeId: number): Promise<StateChange> => {
    const detail = await courseApi.getNode(nodeId)
    let last: StateChange | null = null
    for (const requirement of detail.content.requirements) {
      const result = await courseApi.setRequirement(nodeId, requirement.code, true)
      last = result.state
    }
    if (!last) throw new Error('Ese punto no tiene temas')
    return last
  }

  const marcarPuntoActual = () =>
    run('Punto marcado como cumple', async () => {
      if (!nextNodeId) throw new Error('No hay puntos sin revisar')
      await applyStateChange(await marcarPunto(nextNodeId))
    })

  /** Marca el nivel abierto hasta que se abre el siguiente. */
  const cumplirNivelActual = () =>
    run('Nivel cumplido', async () => {
      const phase = course?.phases.find(
        (item) => item.state.unlocked && !item.state.compliant,
      )
      if (!phase) throw new Error('No hay un nivel pendiente')

      for (const node of phase.nodes) {
        const change = await marcarPunto(node.id)
        if (change.new_phase_unlocked) {
          await applyStateChange(change)
          return
        }
      }
      await refresh()
    })

  return (
    <>
      <AnimatePresence>
        {open && (
          <motion.aside
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-20 left-4 z-40 w-[min(19rem,calc(100vw-2rem))] rounded-card border-2 border-dashed border-brand-blue/30 bg-white p-4 shadow-lift"
            aria-label="Herramientas de desarrollo"
          >
            <div className="mb-3 flex items-center justify-between">
              <p className="text-xs font-extrabold uppercase tracking-wide text-brand-blue">
                Modo desarrollo
              </p>
              <button
                type="button"
                onClick={() => setOpen(false)}
                aria-label="Cerrar herramientas"
                className="rounded-full p-1 text-brand-slate hover:bg-black/5"
              >
                <X aria-hidden className="h-4 w-4" />
              </button>
            </div>

            <div className="space-y-2">
              <Button
                size="sm"
                variant="secondary"
                className="w-full"
                loading={busy}
                disabled={!nextNodeId}
                onClick={marcarPuntoActual}
                icon={<Check aria-hidden className="h-4 w-4" />}
              >
                Marcar punto actual
              </Button>
              <Button
                size="sm"
                variant="secondary"
                className="w-full"
                loading={busy}
                onClick={cumplirNivelActual}
                icon={<FlaskConical aria-hidden className="h-4 w-4" />}
              >
                Cumplir el nivel actual
              </Button>
              <Button
                size="sm"
                variant="danger"
                className="w-full"
                loading={busy}
                onClick={() => run('Avance reiniciado', resetProgress)}
                icon={<RotateCcw aria-hidden className="h-4 w-4" />}
              >
                Reiniciar avance
              </Button>
            </div>

            {message && (
              <p className="mt-3 text-xs font-bold text-brand-slate" role="status">
                {message}
              </p>
            )}
          </motion.aside>
        )}
      </AnimatePresence>

      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="fixed bottom-4 left-4 z-40 flex items-center gap-2 rounded-pill border-2 border-dashed border-brand-blue/40 bg-white px-4 py-2.5 text-xs font-extrabold uppercase tracking-wide text-brand-blue shadow-soft"
      >
        <FlaskConical aria-hidden className="h-4 w-4" />
        Dev
      </button>
    </>
  )
}
