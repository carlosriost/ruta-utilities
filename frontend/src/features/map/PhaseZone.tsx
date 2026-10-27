import { Lock } from 'lucide-react'
import { zoneTokens } from '@/utils/theme'
import {
  Bolt,
  Bush,
  Cloud,
  Drop,
  Pipe,
  Plant,
  Sign,
  Snow,
  Tank,
  Tree,
  Valve,
} from '@/components/illustrations/Decorations'
import type { MapConfig, ZoneLayout } from './mapLayout'

interface PhaseZoneProps {
  zone: ZoneLayout
  config: MapConfig
  compact: boolean
  /** Cumplimiento que exige el nivel anterior para abrir este. */
  previousThreshold: number | null
}

/** Decoraciones caracteristicas de cada zona (agua, frio, energia...). */
function ZoneScenery({
  theme,
  top,
  height,
  width,
  compact,
}: {
  theme: string
  top: number
  height: number
  width: number
  compact: boolean
}) {
  const scale = compact ? 0.62 : 1
  const left = compact ? 52 : 96
  const right = width - left
  const midY = top + height * 0.45
  const lowY = top + height * 0.78

  switch (theme) {
    case 'mint':
      return (
        <>
          <Plant x={right - 10} y={top + 130} scale={scale * 0.9} opacity={0.75} />
          <Tree x={left} y={midY} scale={scale} />
          <Bush x={left + 46 * scale} y={midY + 34 * scale} scale={scale * 0.8} />
          <Sign x={right} y={lowY} scale={scale} />
          <Tree x={right - 34 * scale} y={lowY - 120 * scale} scale={scale * 0.8} />
        </>
      )
    case 'sky':
      return (
        <>
          <Cloud x={left + 10} y={top + 118} scale={scale * 0.9} opacity={0.95} />
          <Tank x={right - 6} y={midY} scale={scale} />
          <Drop x={left + 12} y={midY + 20} scale={scale * 1.15} />
          <Pipe x={left + 26} y={lowY} scale={scale} />
          <Cloud x={right - 30} y={lowY + 40} scale={scale * 0.75} opacity={0.9} />
        </>
      )
    case 'amber':
      return (
        <>
          <Valve x={left + 6} y={top + 150} scale={scale} />
          <Tank x={right - 4} y={midY - 20} scale={scale * 0.9} />
          <Pipe x={right - 40} y={lowY - 40} scale={scale * 0.95} />
          <Sign x={left + 10} y={lowY} scale={scale * 0.9} />
        </>
      )
    case 'teal':
      return (
        <>
          <Cloud x={left + 8} y={top + 124} scale={scale * 0.8} opacity={0.9} />
          <Valve x={right - 8} y={midY} scale={scale * 0.95} />
          <Plant x={left + 10} y={lowY} scale={scale} opacity={0.8} />
          <Bolt x={right - 30} y={lowY - 110 * scale} scale={scale} />
        </>
      )
    default:
      return (
        <>
          <Bolt x={left + 6} y={top + 150} scale={scale * 1.2} />
          <Snow x={right - 20} y={top + 160} scale={scale * 1.1} />
          <Tank x={left + 4} y={midY + 30} scale={scale * 0.85} />
          <Tree x={right - 12} y={lowY} scale={scale * 0.9} />
        </>
      )
  }
}

export function PhaseZone({
  zone,
  config,
  compact,
  previousThreshold,
}: PhaseZoneProps) {
  const { phase, top, height } = zone
  const tokens = zoneTokens(phase.theme)
  const unlocked = phase.state.unlocked
  const width = config.width
  const pad = compact ? 8 : 18

  const headerY = top + (compact ? 44 : 52)
  const barWidth = compact ? 190 : 250
  const barX = width / 2 - barWidth / 2
  const barY = headerY + (compact ? 40 : 46)

  return (
    <g>
      {/* Fondo de la zona */}
      <rect
        x={pad}
        y={top}
        width={width - pad * 2}
        height={height}
        rx={compact ? 26 : 38}
        fill={unlocked ? tokens.soft : '#F2F5F9'}
        opacity={unlocked ? 0.75 : 0.85}
      />
      <rect
        x={pad}
        y={top}
        width={width - pad * 2}
        height={height}
        rx={compact ? 26 : 38}
        fill="none"
        stroke={unlocked ? tokens.main : '#DFE6EF'}
        strokeWidth={2}
        opacity={0.4}
      />

      {/* Suelo orgánico al fondo de la zona */}
      <path
        d={`M ${pad} ${top + height - 46} q ${width / 4} -54 ${width / 2} -6 q ${width / 4} 46 ${width / 2 - pad * 2} -12 L ${width - pad} ${top + height - 20} Q ${width / 2} ${top + height + 8} ${pad} ${top + height - 20} Z`}
        fill={unlocked ? tokens.main : '#DFE6EF'}
        opacity={0.16}
      />

      {/* La escenografia de la zona se atenua mientras esta bloqueada. */}
      <g opacity={unlocked ? 1 : 0.4}>
        <ZoneScenery
          theme={phase.theme}
          top={top}
          height={height}
          width={width}
          compact={compact}
        />
      </g>

      {/* Cabecera de la zona */}
      <g aria-hidden>
        <rect
          x={width / 2 - (compact ? 54 : 62)}
          y={top + (compact ? 14 : 18)}
          width={compact ? 108 : 124}
          height={compact ? 22 : 26}
          rx={13}
          fill={unlocked ? tokens.main : '#B7C0D0'}
        />
        <text
          x={width / 2}
          y={top + (compact ? 29 : 35)}
          textAnchor="middle"
          fontSize={compact ? 12 : 14}
          fontWeight={800}
          letterSpacing={1.4}
          fill="#FFFFFF"
          style={{ fontFamily: 'Nunito, system-ui, sans-serif' }}
        >
          NIVEL VPO {phase.order_index}
        </text>

        <text
          x={width / 2}
          y={headerY + (compact ? 16 : 20)}
          textAnchor="middle"
          fontSize={config.titleSize}
          fontWeight={800}
          fill={unlocked ? '#16233A' : '#8794A8'}
          style={{ fontFamily: '"Baloo 2", Nunito, system-ui, sans-serif' }}
        >
          {phase.name}
        </text>

        {unlocked ? (
          <>
            <rect
              x={barX}
              y={barY}
              width={barWidth}
              height={compact ? 12 : 14}
              rx={7}
              fill="#FFFFFF"
              opacity={0.85}
            />
            <rect
              x={barX}
              y={barY}
              width={Math.max((barWidth * phase.state.percent) / 100, 0)}
              height={compact ? 12 : 14}
              rx={7}
              fill={tokens.main}
            />
            {/* Marca del umbral de desbloqueo (regla del 90%) */}
            <rect
              x={barX + (barWidth * phase.unlock_threshold) / 100 - 1.5}
              y={barY - 3}
              width={3}
              height={compact ? 18 : 20}
              rx={1.5}
              fill="#16233A"
              opacity={0.35}
            />
            <text
              x={width / 2}
              y={barY + (compact ? 30 : 34)}
              textAnchor="middle"
              fontSize={compact ? 13 : 15}
              fontWeight={700}
              fill="#5A6B87"
              style={{ fontFamily: 'Nunito, system-ui, sans-serif' }}
            >
              {phase.state.met} de {phase.state.total_requirements} temas cumplen ·{' '}
              {phase.state.percent}%
            </text>
          </>
        ) : (
          <>
            <Lock
              x={width / 2 - 11}
              y={barY - 2}
              width={22}
              height={22}
              color="#8794A8"
              strokeWidth={2.4}
            />
            <text
              x={width / 2}
              y={barY + (compact ? 40 : 42)}
              textAnchor="middle"
              fontSize={compact ? 13 : 15}
              fontWeight={700}
              fill="#8794A8"
              style={{ fontFamily: 'Nunito, system-ui, sans-serif' }}
            >
              Alcanza {previousThreshold ?? phase.unlock_threshold}% en el nivel
              anterior
            </text>
          </>
        )}
      </g>
    </g>
  )
}
