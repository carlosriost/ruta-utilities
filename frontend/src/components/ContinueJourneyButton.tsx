import { motion } from 'framer-motion'
import { Play } from 'lucide-react'

interface ContinueJourneyButtonProps {
  nodeTitle: string | null
  disabled?: boolean
  onClick: () => void
}

/**
 * Boton destacado "Continuar revision".
 * El siguiente punto lo determina FastAPI (`summary.next_node_id`).
 */
export function ContinueJourneyButton({
  nodeTitle,
  disabled = false,
  onClick,
}: ContinueJourneyButtonProps) {
  return (
    <motion.button
      type="button"
      onClick={onClick}
      disabled={disabled}
      whileHover={disabled ? undefined : { scale: 1.02 }}
      whileTap={disabled ? undefined : { scale: 0.98 }}
      className="group flex w-full items-center gap-4 rounded-card bg-gradient-to-r from-brand-gold to-brand-goldsoft p-4 text-left shadow-lift transition disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto sm:pr-8"
    >
      <span
        aria-hidden
        className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-brand-ink/90 text-white"
      >
        <Play className="h-6 w-6 translate-x-[1px]" fill="currentColor" strokeWidth={0} />
      </span>
      <span className="min-w-0">
        <span className="block text-xs font-extrabold uppercase tracking-[0.16em] text-brand-ink/70">
          Continuar revision
        </span>
        <span className="block truncate text-lg font-extrabold text-brand-ink">
          {nodeTitle ?? 'Recorrido completado'}
        </span>
      </span>
    </motion.button>
  )
}
