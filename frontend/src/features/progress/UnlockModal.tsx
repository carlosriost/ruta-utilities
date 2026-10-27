import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'
import { Modal } from '@/components/Modal'
import { Button } from '@/components/Button'
import { MascotGuide } from '@/components/MascotGuide'
import type { UnlockEvent } from '@/context/CourseContext'

interface UnlockModalProps {
  event: UnlockEvent | null
  onClose: () => void
}

/** Celebracion cuando FastAPI desbloquea una nueva zona del mapa. */
export function UnlockModal({ event, onClose }: UnlockModalProps) {
  return (
    <Modal
      open={event !== null}
      onClose={onClose}
      labelledBy="unlock-title"
      size="md"
      hideClose
    >
      {event && (
        <div className="relative overflow-hidden px-7 py-9 text-center sm:px-10">
          {/* Rayos de fondo */}
          <motion.div
            aria-hidden
            className="pointer-events-none absolute inset-0 -z-10"
            initial={{ opacity: 0, scale: 0.8, rotate: -20 }}
            animate={{ opacity: 1, scale: 1, rotate: 0 }}
            transition={{ duration: 0.6 }}
            style={{
              background:
                'conic-gradient(from 0deg, #FFF3CC 0deg 12deg, transparent 12deg 30deg, #FFF3CC 30deg 42deg, transparent 42deg 60deg, #FFF3CC 60deg 72deg, transparent 72deg 90deg, #FFF3CC 90deg 102deg, transparent 102deg 120deg, #FFF3CC 120deg 132deg, transparent 132deg 150deg, #FFF3CC 150deg 162deg, transparent 162deg 180deg, #FFF3CC 180deg 192deg, transparent 192deg 210deg, #FFF3CC 210deg 222deg, transparent 222deg 240deg, #FFF3CC 240deg 252deg, transparent 252deg 270deg, #FFF3CC 270deg 282deg, transparent 282deg 300deg, #FFF3CC 300deg 312deg, transparent 312deg 330deg, #FFF3CC 330deg 342deg, transparent 342deg 360deg)',
            }}
          />

          <motion.span
            className="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-brand-gold to-brand-goldsoft shadow-lift"
            initial={{ scale: 0, rotate: -45 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ type: 'spring', stiffness: 220, damping: 14, delay: 0.1 }}
          >
            <Sparkles aria-hidden className="h-10 w-10 text-brand-ink" strokeWidth={2.3} />
          </motion.span>

          <p className="text-xs font-extrabold uppercase tracking-[0.22em] text-brand-gold">
            {event.courseCompliant ? 'Recorrido completado' : 'Nueva zona desbloqueada'}
          </p>
          <h2 id="unlock-title" className="mt-2 text-3xl font-extrabold text-brand-ink">
            Felicitaciones!
          </h2>

          <p className="mx-auto mt-3 max-w-sm text-brand-slate">
            {event.previousPhaseName ? (
              <>
                Has superado <strong className="text-brand-ink">{event.previousPhaseName}</strong>.{' '}
              </>
            ) : null}
            Ahora puedes explorar{' '}
            <strong className="text-brand-ink">{event.phaseName}</strong>.
          </p>

          <MascotGuide
            mood="cheer"
            size={78}
            message="Nueva zona desbloqueada! Sigue asi."
            className="mt-6 justify-center"
          />

          <Button size="lg" variant="gold" className="mt-7 w-full sm:w-auto" onClick={onClose}>
            EXPLORAR NUEVA ZONA
          </Button>
        </div>
      )}
    </Modal>
  )
}
