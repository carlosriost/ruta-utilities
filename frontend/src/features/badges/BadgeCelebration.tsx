import { useEffect } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { X } from 'lucide-react'
import { iconFor } from '@/utils/icons'
import { zoneTokens } from '@/utils/theme'
import type { Badge } from '@/types/api'

interface BadgeCelebrationProps {
  badges: Badge[]
  onDismiss: () => void
}

/** Aviso flotante cuando FastAPI concede una insignia nueva. */
export function BadgeCelebration({ badges, onDismiss }: BadgeCelebrationProps) {
  useEffect(() => {
    if (badges.length === 0) return
    const timer = window.setTimeout(onDismiss, 7000)
    return () => window.clearTimeout(timer)
  }, [badges, onDismiss])

  return (
    <div
      className="pointer-events-none fixed bottom-4 right-4 z-50 flex w-[min(22rem,calc(100vw-2rem))] flex-col gap-3"
      role="status"
      aria-live="polite"
    >
      <AnimatePresence>
        {badges.map((badge, index) => {
          const tokens = zoneTokens(badge.theme)
          const Icon = iconFor(badge.icon)
          return (
            <motion.div
              key={badge.id}
              initial={{ opacity: 0, x: 60, scale: 0.9 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 60 }}
              transition={{ delay: index * 0.12, type: 'spring', stiffness: 220, damping: 22 }}
              className="pointer-events-auto flex items-center gap-3 rounded-card bg-white p-4 shadow-lift"
            >
              <span
                aria-hidden
                className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl"
                style={{ backgroundColor: tokens.soft }}
              >
                <Icon className="h-6 w-6" style={{ color: tokens.main }} strokeWidth={2.3} />
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-[11px] font-extrabold uppercase tracking-[0.16em] text-brand-gold">
                  Nueva insignia
                </p>
                <p className="truncate font-extrabold text-brand-ink">{badge.name}</p>
                <p className="truncate text-xs text-brand-slate">{badge.description}</p>
              </div>
              <button
                type="button"
                onClick={onDismiss}
                aria-label="Cerrar aviso"
                className="rounded-full p-1.5 text-brand-slate transition hover:bg-black/5"
              >
                <X aria-hidden className="h-4 w-4" />
              </button>
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}
