import { motion } from 'framer-motion'

interface ProgressBarProps {
  value: number
  /** Color de relleno (token hex de la zona). */
  color?: string
  label?: string
  /** Marca opcional del umbral de desbloqueo (regla del 90%). */
  threshold?: number
  size?: 'sm' | 'md' | 'lg'
  showValue?: boolean
}

const HEIGHTS = { sm: 'h-2', md: 'h-3', lg: 'h-5' }

export function ProgressBar({
  value,
  color = '#1F4FD8',
  label,
  threshold,
  size = 'md',
  showValue = false,
}: ProgressBarProps) {
  const safeValue = Math.max(0, Math.min(100, Math.round(value)))

  return (
    <div className="w-full">
      {(label || showValue) && (
        <div className="mb-1.5 flex items-baseline justify-between gap-3">
          {label && (
            <span className="text-sm font-semibold text-brand-slate">{label}</span>
          )}
          {showValue && (
            <span className="text-sm font-extrabold tabular-nums text-brand-ink">
              {safeValue}%
            </span>
          )}
        </div>
      )}

      <div
        role="progressbar"
        aria-valuenow={safeValue}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label ?? 'Progreso'}
        className={`relative w-full overflow-hidden rounded-pill bg-state-lockedsoft shadow-inner_soft ${HEIGHTS[size]}`}
      >
        <motion.div
          className="h-full rounded-pill"
          style={{ backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${safeValue}%` }}
          transition={{ type: 'spring', stiffness: 120, damping: 20 }}
        />
        {threshold !== undefined && threshold > 0 && threshold < 100 && (
          <span
            aria-hidden
            title={`Umbral de desbloqueo: ${threshold}%`}
            className="absolute top-0 h-full w-[3px] rounded-full bg-brand-ink/30"
            style={{ left: `calc(${threshold}% - 1.5px)` }}
          />
        )}
      </div>
    </div>
  )
}
