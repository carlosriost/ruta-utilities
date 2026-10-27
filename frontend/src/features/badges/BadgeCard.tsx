import { motion } from 'framer-motion'
import { Lock } from 'lucide-react'
import { iconFor } from '@/utils/icons'
import { LOCKED_TOKENS, zoneTokens } from '@/utils/theme'
import { formatDate } from '@/utils/format'
import type { Badge } from '@/types/api'

interface BadgeCardProps {
  badge: Badge
  index?: number
}

/** Insignia del operario. Las reglas las evalua FastAPI, aqui solo se muestra. */
export function BadgeCard({ badge, index = 0 }: BadgeCardProps) {
  const tokens = badge.earned ? zoneTokens(badge.theme) : LOCKED_TOKENS
  const Icon = iconFor(badge.icon)

  return (
    <motion.article
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.06, 0.5) }}
      className={`card-soft relative overflow-hidden p-5 text-center ${
        badge.earned ? '' : 'opacity-80'
      }`}
    >
      {badge.earned && (
        <span
          aria-hidden
          className="absolute -right-8 top-4 rotate-45 px-9 py-1 text-[10px] font-extrabold uppercase tracking-widest text-white"
          style={{ backgroundColor: tokens.main }}
        >
          Obtenida
        </span>
      )}

      <span
        aria-hidden
        className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-3xl"
        style={{ backgroundColor: tokens.soft }}
      >
        {badge.earned ? (
          <Icon className="h-10 w-10" style={{ color: tokens.main }} strokeWidth={2.2} />
        ) : (
          <Lock className="h-8 w-8 text-state-locked" strokeWidth={2.4} />
        )}
      </span>

      <h3 className="text-lg font-extrabold text-brand-ink">{badge.name}</h3>
      <p className="mt-1 text-sm text-brand-slate">{badge.description}</p>

      <p className="mt-3 text-xs font-bold uppercase tracking-wide text-brand-slate">
        {badge.earned ? formatDate(badge.awarded_at) : 'Aun por conseguir'}
      </p>
    </motion.article>
  )
}
