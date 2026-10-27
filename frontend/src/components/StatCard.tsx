import type { LucideIcon } from 'lucide-react'
import { motion } from 'framer-motion'

interface StatCardProps {
  icon: LucideIcon
  label: string
  value: string
  hint?: string
  color: string
  soft: string
  index?: number
}

/** Tarjeta de dato del resumen. Los valores vienen siempre del backend. */
export function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  color,
  soft,
  index = 0,
}: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.07 }}
      className="card-soft flex items-center gap-4 p-4"
    >
      <span
        aria-hidden
        className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl"
        style={{ backgroundColor: soft }}
      >
        <Icon className="h-6 w-6" style={{ color }} strokeWidth={2.3} />
      </span>
      <div className="min-w-0">
        <p className="text-xs font-extrabold uppercase tracking-wide text-brand-slate">
          {label}
        </p>
        <p className="truncate text-xl font-extrabold text-brand-ink">{value}</p>
        {hint && <p className="truncate text-xs text-brand-slate">{hint}</p>}
      </div>
    </motion.div>
  )
}
