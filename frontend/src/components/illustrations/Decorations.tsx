/**
 * Decoraciones ilustradas del mapa.
 *
 * Son elementos SVG (<g>) pensados para vivir DENTRO del viewBox de `GameMap`,
 * de modo que escalan con el mapa y nunca provocan scroll horizontal.
 * Estetica caricaturesca y limpia: nada de P&ID ni de SCADA.
 */

import type { ReactNode } from 'react'

interface DecoProps {
  x: number
  y: number
  scale?: number
  opacity?: number
}

function wrap({ x, y, scale = 1, opacity = 1 }: DecoProps, children: ReactNode) {
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity} aria-hidden>
      {children}
    </g>
  )
}

export function Cloud(props: DecoProps) {
  return wrap(
    props,
    <g>
      <ellipse cx="0" cy="0" rx="34" ry="20" fill="#FFFFFF" />
      <ellipse cx="-26" cy="6" rx="22" ry="15" fill="#FFFFFF" />
      <ellipse cx="28" cy="7" rx="24" ry="16" fill="#FFFFFF" />
      <ellipse cx="4" cy="-12" rx="20" ry="14" fill="#FFFFFF" />
      <ellipse cx="6" cy="10" rx="40" ry="10" fill="#EAF2FB" />
    </g>,
  )
}

export function Tree(props: DecoProps) {
  return wrap(
    props,
    <g>
      <rect x="-5" y="6" width="10" height="26" rx="4" fill="#B0763F" />
      <circle cx="0" cy="-6" r="24" fill="#3FBE86" />
      <circle cx="-16" cy="4" r="16" fill="#35A876" />
      <circle cx="16" cy="4" r="16" fill="#4CCB92" />
      <circle cx="-6" cy="-16" r="12" fill="#5AD79E" opacity="0.75" />
    </g>,
  )
}

export function Bush(props: DecoProps) {
  return wrap(
    props,
    <g>
      <ellipse cx="0" cy="0" rx="22" ry="14" fill="#41C48B" />
      <ellipse cx="-12" cy="2" rx="13" ry="10" fill="#37B27D" />
      <ellipse cx="13" cy="3" rx="12" ry="9" fill="#57D49C" />
    </g>,
  )
}

/** Tanque de almacenamiento estilizado. */
export function Tank(props: DecoProps) {
  return wrap(
    props,
    <g>
      <rect x="-26" y="-30" width="52" height="60" rx="16" fill="#DCEDFD" />
      <rect x="-26" y="-30" width="52" height="60" rx="16" fill="none" stroke="#2E8FEA" strokeWidth="4" />
      <rect x="-26" y="4" width="52" height="26" rx="13" fill="#8EC5F6" />
      <rect x="-14" y="-40" width="28" height="12" rx="6" fill="#2E8FEA" />
      <circle cx="0" cy="-10" r="7" fill="#fff" opacity="0.85" />
      <rect x="-32" y="30" width="64" height="8" rx="4" fill="#C9D6E6" />
    </g>,
  )
}

/** Tuberia curva con dos bridas. */
export function Pipe(props: DecoProps) {
  return wrap(
    props,
    <g>
      <path
        d="M-40 0h30a20 20 0 0 1 20 20v24"
        stroke="#C9D6E6"
        strokeWidth="16"
        fill="none"
        strokeLinecap="round"
      />
      <path
        d="M-40 0h30a20 20 0 0 1 20 20v24"
        stroke="#EEF3F9"
        strokeWidth="7"
        fill="none"
        strokeLinecap="round"
      />
      <rect x="-44" y="-11" width="9" height="22" rx="3" fill="#9FB2C8" />
      <rect x="1" y="40" width="18" height="9" rx="3" fill="#9FB2C8" />
    </g>,
  )
}

/** Valvula de volante, icono clasico y amable de Utilities. */
export function Valve(props: DecoProps) {
  return wrap(
    props,
    <g>
      <rect x="-24" y="-6" width="48" height="14" rx="7" fill="#C9D6E6" />
      <circle cx="0" cy="-4" r="15" fill="none" stroke="#F5B301" strokeWidth="6" />
      <rect x="-2.5" y="-22" width="5" height="16" rx="2.5" fill="#F5B301" />
      <circle cx="0" cy="-4" r="4" fill="#F5B301" />
    </g>,
  )
}

/** Gota de agua sonriente. */
export function Drop(props: DecoProps) {
  return wrap(
    props,
    <g>
      <path d="M0-22c9 11 16 18 16 27a16 16 0 1 1-32 0c0-9 7-16 16-27z" fill="#5BB0F5" />
      <ellipse cx="-5" cy="6" rx="4" ry="5" fill="#fff" opacity="0.55" />
    </g>,
  )
}

/** Rayo de energia. */
export function Bolt(props: DecoProps) {
  return wrap(
    props,
    <g>
      <path d="M6-26-14 4h12l-6 22 20-30H0z" fill="#F5B301" stroke="#E0A501" strokeWidth="2" />
    </g>,
  )
}

/** Copo de nieve para la zona de frio. */
export function Snow(props: DecoProps) {
  return wrap(
    props,
    <g stroke="#8FD3FF" strokeWidth="4" strokeLinecap="round">
      <path d="M0-16V16M-14-8L14 8M-14 8L14-8" />
    </g>,
  )
}

/** Senal de seguridad amable. */
export function Sign(props: DecoProps) {
  return wrap(
    props,
    <g>
      <rect x="-3" y="0" width="6" height="30" rx="3" fill="#B0763F" />
      <rect x="-26" y="-26" width="52" height="30" rx="8" fill="#FFD75E" stroke="#E0A501" strokeWidth="3" />
      <path d="M0-20l10 17H-10z" fill="#16233A" />
      <rect x="-1.6" y="-13" width="3.2" height="7" rx="1.6" fill="#FFD75E" />
      <circle cx="0" cy="-4.6" r="1.8" fill="#FFD75E" />
    </g>,
  )
}

/** Silueta de planta al fondo. */
export function Plant(props: DecoProps) {
  return wrap(
    props,
    <g>
      <rect x="-60" y="-20" width="120" height="52" rx="10" fill="#E4EDF7" />
      <rect x="-42" y="-46" width="26" height="30" rx="6" fill="#D5E3F2" />
      <rect x="12" y="-56" width="18" height="40" rx="9" fill="#D5E3F2" />
      <rect x="-52" y="-6" width="16" height="16" rx="4" fill="#FFFFFF" />
      <rect x="-26" y="-6" width="16" height="16" rx="4" fill="#FFFFFF" />
      <rect x="0" y="-6" width="16" height="16" rx="4" fill="#FFFFFF" />
      <rect x="26" y="-6" width="16" height="16" rx="4" fill="#FFFFFF" />
      <ellipse cx="21" cy="-62" rx="14" ry="9" fill="#FFFFFF" opacity="0.85" />
    </g>,
  )
}

/** Colina orgánica para dar profundidad a la zona. */
export function Hill({ x, y, width, color, opacity = 1 }: DecoProps & { width: number; color: string }) {
  return (
    <g aria-hidden opacity={opacity}>
      <path
        d={`M${x - width / 2} ${y} q ${width / 4} -70 ${width / 2} 0 z`}
        fill={color}
      />
    </g>
  )
}
