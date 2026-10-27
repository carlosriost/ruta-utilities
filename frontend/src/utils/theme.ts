import type { ZoneTheme } from '@/types/api'

/**
 * Tokens de color por zona del mapa.
 *
 * Los valores hex se usan dentro del SVG del mapa (donde no llegan las clases
 * de Tailwind). Estan alineados con `tailwind.config.js` e `index.css`.
 */
export interface ZoneTokens {
  main: string
  soft: string
  deep: string
  /** Clases utilitarias equivalentes, para las tarjetas de la interfaz. */
  chipClass: string
  textClass: string
  bgClass: string
  ringClass: string
  gradientClass: string
}

const ZONES: Record<ZoneTheme, ZoneTokens> = {
  mint: {
    main: '#2FBF87',
    soft: '#D6F6E7',
    deep: '#1B8B60',
    chipClass: 'bg-zone-mintsoft text-[#1B8B60]',
    textClass: 'text-zone-mint',
    bgClass: 'bg-zone-mint',
    ringClass: 'ring-zone-mint',
    gradientClass: 'from-zone-mint to-[#5FD8A6]',
  },
  sky: {
    main: '#2E8FEA',
    soft: '#DCEDFD',
    deep: '#1B63A8',
    chipClass: 'bg-zone-skysoft text-[#1B63A8]',
    textClass: 'text-zone-sky',
    bgClass: 'bg-zone-sky',
    ringClass: 'ring-zone-sky',
    gradientClass: 'from-zone-sky to-[#6FB6F5]',
  },
  amber: {
    main: '#F09520',
    soft: '#FEEBD2',
    deep: '#B96908',
    chipClass: 'bg-zone-ambersoft text-[#B96908]',
    textClass: 'text-zone-amber',
    bgClass: 'bg-zone-amber',
    ringClass: 'ring-zone-amber',
    gradientClass: 'from-zone-amber to-[#F7BC63]',
  },
  grape: {
    main: '#7C5CE0',
    soft: '#E8E1FC',
    deep: '#553BA8',
    chipClass: 'bg-zone-grapesoft text-[#553BA8]',
    textClass: 'text-zone-grape',
    bgClass: 'bg-zone-grape',
    ringClass: 'ring-zone-grape',
    gradientClass: 'from-zone-grape to-[#A78BFA]',
  },
  teal: {
    main: '#0FA3A3',
    soft: '#D3F1F1',
    deep: '#0A7070',
    chipClass: 'bg-zone-tealsoft text-[#0A7070]',
    textClass: 'text-zone-teal',
    bgClass: 'bg-zone-teal',
    ringClass: 'ring-zone-teal',
    gradientClass: 'from-zone-teal to-[#5BC9C9]',
  },
}

export const LOCKED_TOKENS: ZoneTokens = {
  main: '#B7C0D0',
  soft: '#EDF1F6',
  deep: '#8794A8',
  chipClass: 'bg-state-lockedsoft text-state-locked',
  textClass: 'text-state-locked',
  bgClass: 'bg-state-locked',
  ringClass: 'ring-state-locked',
  gradientClass: 'from-state-locked to-[#CBD3DF]',
}

export function zoneTokens(theme: string | undefined): ZoneTokens {
  return ZONES[(theme as ZoneTheme) ?? 'sky'] ?? ZONES.sky
}
