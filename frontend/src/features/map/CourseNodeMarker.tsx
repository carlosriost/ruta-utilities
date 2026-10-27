import { motion } from 'framer-motion'
import { iconFor } from '@/utils/icons'
import { LOCKED_TOKENS, type ZoneTokens } from '@/utils/theme'
import { wrapText } from '@/utils/format'
import type { NodePoint } from './mapLayout'

interface CourseNodeMarkerProps {
  point: NodePoint
  tokens: ZoneTokens
  radius: number
  labelSize: number
  /** Es el siguiente punto sugerido del recorrido. */
  isNext: boolean
  index: number
  onSelect: (nodeId: number) => void
}

const VERDE = '#22A06B'
const ROJO = '#E5544B'

/**
 * Un punto del mapa dibujado dentro del SVG.
 *
 * Cada tema empieza en "no cumple", asi que un punto siempre tiene un estado
 * real desde el primer momento: verde con chulito si todos sus temas cumplen,
 * rojo con equis (y el contador de brechas) en caso contrario. No existe un
 * tercer estado de "sin revisar".
 */
export function CourseNodeMarker({
  point,
  tokens,
  radius,
  labelSize,
  isNext,
  index,
  onSelect,
}: CourseNodeMarkerProps) {
  const { node, x, y } = point
  const locked = node.status === 'LOCKED'
  const compliant = node.status === 'COMPLIANT'

  const palette = locked ? LOCKED_TOKENS : tokens
  const fill = locked ? palette.main : compliant ? VERDE : ROJO
  const Icon = iconFor(locked ? 'lock' : node.icon)
  const size = radius
  const iconSize = Math.round(size * 0.86)

  const estado = locked
    ? 'bloqueado'
    : compliant
      ? `los ${node.total_requirements} temas cumplen`
      : `${node.met} de ${node.total_requirements} temas cumplen`

  const lines = wrapText(node.title, radius > 36 ? 20 : 17, 2)

  const activar = () => {
    if (locked) return
    onSelect(node.id)
  }

  return (
    <motion.g
      role="button"
      tabIndex={locked ? -1 : 0}
      aria-label={`${node.title}. ${estado}.${
        locked ? ` ${node.locked_reason ?? ''}` : ''
      }`}
      aria-disabled={locked || undefined}
      className={locked ? 'cursor-not-allowed' : 'cursor-pointer'}
      onClick={activar}
      onKeyDown={(event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault()
          activar()
        }
      }}
      initial={{ opacity: 0, scale: 0.6 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        delay: Math.min(index * 0.035, 0.7),
        type: 'spring',
        stiffness: 220,
        damping: 18,
      }}
      whileHover={locked ? undefined : { scale: 1.09 }}
      whileTap={locked ? undefined : { scale: 0.95 }}
      style={{ transformOrigin: `${x}px ${y}px` }}
    >
      <title>
        {node.title} - {estado}
      </title>

      {/* Halo pulsante para el siguiente punto sugerido */}
      {isNext && !locked && (
        <circle
          cx={x}
          cy={y}
          r={size + 8}
          fill="none"
          stroke={palette.main}
          strokeWidth={4}
          opacity={0.55}
          className="animate-pulseRing"
          style={{ transformOrigin: `${x}px ${y}px` }}
        />
      )}

      {/* Sombra */}
      <ellipse
        cx={x}
        cy={y + size + 7}
        rx={size * 0.72}
        ry={size * 0.2}
        fill="#16233A"
        opacity={0.11}
      />

      <circle cx={x} cy={y} r={size} fill={fill} stroke="#FFFFFF" strokeWidth={5} />

      {/* Brillo superior, para el acabado ilustrado */}
      <ellipse
        cx={x - size * 0.24}
        cy={y - size * 0.42}
        rx={size * 0.34}
        ry={size * 0.2}
        fill="#FFFFFF"
        opacity={0.28}
        transform={`rotate(-25 ${x} ${y})`}
      />

      <Icon
        x={x - iconSize / 2}
        y={y - iconSize / 2}
        width={iconSize}
        height={iconSize}
        color="#FFFFFF"
        strokeWidth={2.2}
        aria-hidden
      />

      {/* Medalla: chulito si todo cumple, equis si hay brechas */}
      {!locked && (
        <g aria-hidden>
          <circle cx={x + size * 0.72} cy={y - size * 0.72} r={size * 0.36} fill="#FFFFFF" />
          <circle
            cx={x + size * 0.72}
            cy={y - size * 0.72}
            r={size * 0.29}
            fill={compliant ? VERDE : ROJO}
          />
          {compliant ? (
            <path
              d={`M ${x + size * 0.72 - size * 0.14} ${y - size * 0.72} l ${size * 0.1} ${size * 0.11} l ${size * 0.18} -${size * 0.2}`}
              stroke="#FFFFFF"
              strokeWidth={size * 0.09}
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
            />
          ) : (
            <g
              stroke="#FFFFFF"
              strokeWidth={size * 0.09}
              strokeLinecap="round"
              transform={`translate(${x + size * 0.72} ${y - size * 0.72})`}
            >
              <line x1={-size * 0.12} y1={-size * 0.12} x2={size * 0.12} y2={size * 0.12} />
              <line x1={size * 0.12} y1={-size * 0.12} x2={-size * 0.12} y2={size * 0.12} />
            </g>
          )}
        </g>
      )}

      {/* Etiqueta */}
      <g aria-hidden>
        <text
          x={x}
          y={y + size + 26}
          textAnchor="middle"
          fontSize={labelSize}
          fontWeight={800}
          fill={locked ? '#8794A8' : '#16233A'}
          style={{ paintOrder: 'stroke', fontFamily: 'Nunito, system-ui, sans-serif' }}
          stroke="#FFFCF3"
          strokeWidth={4}
        >
          {lines.map((line, i) => (
            <tspan key={line + i} x={x} dy={i === 0 ? 0 : labelSize + 2}>
              {line}
            </tspan>
          ))}
        </text>

        {!locked && (
          <text
            x={x}
            y={y + size + 26 + lines.length * (labelSize + 2)}
            textAnchor="middle"
            fontSize={labelSize - 2}
            fontWeight={700}
            fill={compliant ? VERDE : ROJO}
            style={{
              paintOrder: 'stroke',
              fontFamily: 'Nunito, system-ui, sans-serif',
            }}
            stroke="#FFFCF3"
            strokeWidth={4}
          >
            {node.met} de {node.total_requirements} cumplen
          </text>
        )}
      </g>
    </motion.g>
  )
}
