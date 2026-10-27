import { useMemo } from 'react'
import { motion } from 'framer-motion'
import { Flag, Trophy } from 'lucide-react'
import { useIsMobile } from '@/hooks/useMediaQuery'
import { zoneTokens } from '@/utils/theme'
import type { PhaseDetail } from '@/types/api'
import {
  DESKTOP_CONFIG,
  MOBILE_CONFIG,
  buildMapLayout,
} from './mapLayout'
import { PhaseZone } from './PhaseZone'
import { CourseNodeMarker } from './CourseNodeMarker'

interface GameMapProps {
  phases: PhaseDetail[]
  nextNodeId: number | null
  courseCompliant: boolean
  onSelectNode: (nodeId: number) => void
}

/**
 * El mapa: un unico SVG con camino serpenteante, zonas ilustradas y nodos
 * conectados. No es una lista de tarjetas: es un recorrido.
 */
export function GameMap({
  phases,
  nextNodeId,
  courseCompliant,
  onSelectNode,
}: GameMapProps) {
  const compact = useIsMobile()
  const config = compact ? MOBILE_CONFIG : DESKTOP_CONFIG

  const layout = useMemo(() => buildMapLayout(phases, config), [phases, config])
  const lastPoint = layout.points[layout.points.length - 1]
  const firstPoint = layout.points[0]
  const goalY = lastPoint ? lastPoint.y + (compact ? 78 : 96) : 0
  const totalHeight = layout.height + (compact ? 40 : 60)

  return (
    <div className="relative w-full">
      <svg
        viewBox={`0 0 ${layout.width} ${totalHeight}`}
        width="100%"
        height="auto"
        role="group"
        aria-label="Mapa del recorrido Ruta Utilities"
        className="block h-auto w-full max-w-full"
        preserveAspectRatio="xMidYMin meet"
      >
        <defs>
          <linearGradient id="goalGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#F5B301" />
            <stop offset="100%" stopColor="#E0A501" />
          </linearGradient>
        </defs>

        {/* Zonas de fondo */}
        {layout.zones.map((zone, index) => (
          <PhaseZone
            key={zone.phase.id}
            zone={zone}
            config={config}
            compact={compact}
            previousThreshold={
              layout.zones[index - 1]?.phase.unlock_threshold ?? null
            }
          />
        ))}

        {/* Camino: los tramos recorridos van solidos, los pendientes punteados */}
        <g>
          {layout.segments.map((segment, index) => {
            const theme = layout.zones[segment.zoneIndex]?.phase
            const tokens = zoneTokens(theme?.theme)
            const unlocked = theme?.state.unlocked
            return (
              <g key={`segment-${index}`} aria-hidden>
                <path
                  d={segment.d}
                  fill="none"
                  stroke="#FFFFFF"
                  strokeWidth={compact ? 16 : 20}
                  strokeLinecap="round"
                  opacity={0.85}
                />
                {segment.travelled ? (
                  // Tramo recorrido: se dibuja animando su longitud.
                  <motion.path
                    d={segment.d}
                    fill="none"
                    stroke={tokens.main}
                    strokeWidth={compact ? 8 : 10}
                    strokeLinecap="round"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.6, delay: Math.min(index * 0.02, 0.5) }}
                  />
                ) : (
                  // Tramo pendiente: punteado estatico (pathLength usa el mismo
                  // stroke-dasharray, por eso no se animan estos tramos).
                  <path
                    d={segment.d}
                    fill="none"
                    stroke={unlocked ? '#CFDCEA' : '#DFE6EF'}
                    strokeWidth={compact ? 8 : 10}
                    strokeLinecap="round"
                    strokeDasharray="2 16"
                  />
                )}
              </g>
            )
          })}
        </g>

        {/* Marca de INICIO */}
        {firstPoint && (
          <g aria-hidden>
            <rect
              x={firstPoint.x - (compact ? 40 : 46)}
              y={firstPoint.y - (compact ? 84 : 96)}
              width={compact ? 80 : 92}
              height={compact ? 26 : 30}
              rx={15}
              fill="#16233A"
            />
            <text
              x={firstPoint.x}
              y={firstPoint.y - (compact ? 65 : 75)}
              textAnchor="middle"
              fontSize={compact ? 13 : 15}
              fontWeight={800}
              letterSpacing={2}
              fill="#FFFFFF"
              style={{ fontFamily: 'Nunito, system-ui, sans-serif' }}
            >
              INICIO
            </text>
          </g>
        )}

        {/* Nodos */}
        {layout.zones.map((zone) =>
          zone.points.map((point, index) => (
            <CourseNodeMarker
              key={point.node.id}
              point={point}
              tokens={zoneTokens(zone.phase.theme)}
              radius={config.nodeRadius}
              labelSize={config.labelSize}
              isNext={point.node.id === nextNodeId}
              index={index}
              onSelect={onSelectNode}
            />
          )),
        )}

        {/* META */}
        {lastPoint && (
          <g aria-label="Meta del recorrido">
            <path
              d={`M ${lastPoint.x} ${lastPoint.y + (compact ? 34 : 44)} V ${goalY - (compact ? 26 : 32)}`}
              stroke={courseCompliant ? '#F5B301' : '#CFDCEA'}
              strokeWidth={compact ? 8 : 10}
              strokeLinecap="round"
              strokeDasharray={courseCompliant ? undefined : '2 16'}
              fill="none"
            />
            <ellipse
              cx={layout.width / 2}
              cy={goalY + (compact ? 26 : 32)}
              rx={compact ? 42 : 54}
              ry={compact ? 12 : 15}
              fill="#16233A"
              opacity={0.1}
            />
            <circle
              cx={layout.width / 2}
              cy={goalY}
              r={compact ? 34 : 42}
              fill={courseCompliant ? 'url(#goalGradient)' : '#E7EDF5'}
              stroke="#FFFFFF"
              strokeWidth={5}
            />
            {courseCompliant ? (
              <Trophy
                x={layout.width / 2 - (compact ? 17 : 21)}
                y={goalY - (compact ? 17 : 21)}
                width={compact ? 34 : 42}
                height={compact ? 34 : 42}
                color="#16233A"
                strokeWidth={2.2}
                aria-hidden
              />
            ) : (
              <Flag
                x={layout.width / 2 - (compact ? 16 : 20)}
                y={goalY - (compact ? 16 : 20)}
                width={compact ? 32 : 40}
                height={compact ? 32 : 40}
                color="#A6B3C6"
                strokeWidth={2.2}
                aria-hidden
              />
            )}
            <text
              x={layout.width / 2}
              y={goalY + (compact ? 58 : 70)}
              textAnchor="middle"
              fontSize={compact ? 16 : 19}
              fontWeight={800}
              letterSpacing={2}
              fill={courseCompliant ? '#16233A' : '#8794A8'}
              style={{ fontFamily: '"Baloo 2", Nunito, system-ui, sans-serif' }}
            >
              META
            </text>
          </g>
        )}
      </svg>
    </div>
  )
}
