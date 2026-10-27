import { motion } from 'framer-motion'

/**
 * ============================================================================
 *  MASCOTA PLACEHOLDER  -  SUSTITUIR AQUI
 * ============================================================================
 * "Gotix" es un personaje NEUTRAL creado solo para esta demo. No representa
 * ni imita a ninguna mascota oficial de Bavaria.
 *
 * COMO REEMPLAZARLA:
 *   1. Sustituye unicamente el componente `MascotAvatar` de este archivo por
 *      la ilustracion oficial (SVG inline o <img src="/mascota.png" />).
 *   2. Mantén la firma de props (`mood`, `size`) para no tocar el resto.
 *   3. Los textos de los bocadillos se pasan desde fuera con `message`,
 *      asi que no hay copy quemado dentro de la mascota.
 * ============================================================================
 */

export type MascotMood = 'happy' | 'cheer' | 'hint' | 'thinking'

const MOOD_COLOR: Record<MascotMood, string> = {
  happy: '#2E8FEA',
  cheer: '#2FBF87',
  hint: '#F09520',
  thinking: '#7C5CE0',
}

function MascotAvatar({ mood, size }: { mood: MascotMood; size: number }) {
  const color = MOOD_COLOR[mood]
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 120 120"
      role="img"
      aria-label="Gotix, tu guia en la ruta"
      className="drop-shadow-[0_8px_16px_rgba(22,35,58,0.18)]"
    >
      {/* cuerpo: gota redondeada */}
      <path
        d="M60 14c16 18 30 32 30 50a30 30 0 1 1-60 0c0-18 14-32 30-50z"
        fill={color}
      />
      <path
        d="M60 14c16 18 30 32 30 50a30 30 0 0 1-14 25c6-8 8-17 8-25 0-16-11-29-24-45z"
        fill="#000"
        opacity="0.12"
      />
      {/* casco de seguridad */}
      <path
        d="M32 52a28 28 0 0 1 56 0z"
        fill="#F5B301"
      />
      <rect x="26" y="50" width="68" height="8" rx="4" fill="#FFD75E" />
      <path d="M56 26h8v26h-8z" fill="#FFD75E" opacity="0.9" />
      {/* cara */}
      <ellipse cx="49" cy="74" rx="5.5" ry="6.5" fill="#16233A" />
      <ellipse cx="71" cy="74" rx="5.5" ry="6.5" fill="#16233A" />
      <circle cx="50.8" cy="71.8" r="1.9" fill="#fff" />
      <circle cx="72.8" cy="71.8" r="1.9" fill="#fff" />
      {mood === 'thinking' ? (
        <path
          d="M50 92c4-3 16-3 20 0"
          stroke="#16233A"
          strokeWidth="3.5"
          strokeLinecap="round"
          fill="none"
        />
      ) : (
        <path
          d="M48 88c5 7 19 7 24 0"
          stroke="#16233A"
          strokeWidth="3.5"
          strokeLinecap="round"
          fill="none"
        />
      )}
      <ellipse cx="40" cy="86" rx="5" ry="3.4" fill="#fff" opacity="0.35" />
      <ellipse cx="80" cy="86" rx="5" ry="3.4" fill="#fff" opacity="0.35" />
    </svg>
  )
}

interface MascotGuideProps {
  message: string
  mood?: MascotMood
  size?: number
  /** Coloca el bocadillo a la izquierda del personaje. */
  reverse?: boolean
  className?: string
}

export function MascotGuide({
  message,
  mood = 'happy',
  size = 92,
  reverse = false,
  className = '',
}: MascotGuideProps) {
  return (
    <div
      className={`flex items-center gap-4 ${reverse ? 'flex-row-reverse' : ''} ${className}`}
    >
      <motion.div
        className="shrink-0"
        animate={{ y: [0, -7, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
      >
        <MascotAvatar mood={mood} size={size} />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: reverse ? 12 : -12 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.35 }}
        className="relative max-w-sm rounded-card bg-white px-5 py-3.5 shadow-soft"
      >
        {/* pico del bocadillo */}
        <span
          aria-hidden
          className={`absolute top-1/2 h-4 w-4 -translate-y-1/2 rotate-45 bg-white ${
            reverse ? '-right-2' : '-left-2'
          }`}
        />
        <p className="relative text-[15px] font-semibold leading-snug text-brand-ink">
          {message}
        </p>
      </motion.div>
    </div>
  )
}
