import type { NodeState, PhaseDetail } from '@/types/api'

/**
 * Calculo del trazado del mapa.
 *
 * El mapa es un unico SVG con viewBox fijo: asi escala perfectamente en
 * cualquier pantalla, no genera scroll horizontal y los nodos, el camino y las
 * decoraciones mantienen siempre la misma proporcion.
 *
 * Los nodos se colocan en zigzag (serpentina) y se unen con curvas suaves
 * calculadas con Catmull-Rom convertido a bezier cubica.
 */

export interface MapConfig {
  width: number
  headerHeight: number
  nodeGap: number
  zonePaddingBottom: number
  zoneGap: number
  columns: number[]
  nodeRadius: number
  labelSize: number
  titleSize: number
}

export const DESKTOP_CONFIG: MapConfig = {
  width: 1000,
  headerHeight: 150,
  nodeGap: 156,
  zonePaddingBottom: 96,
  zoneGap: 26,
  columns: [270, 500, 730, 500],
  nodeRadius: 40,
  labelSize: 17,
  titleSize: 34,
}

export const MOBILE_CONFIG: MapConfig = {
  width: 480,
  headerHeight: 138,
  nodeGap: 140,
  zonePaddingBottom: 74,
  zoneGap: 20,
  columns: [130, 240, 350, 240],
  nodeRadius: 32,
  labelSize: 15,
  titleSize: 27,
}

export interface Point {
  x: number
  y: number
}

export interface NodePoint extends Point {
  node: NodeState
  zoneIndex: number
}

export interface PathSegment {
  d: string
  zoneIndex: number
  /** El tramo ya fue recorrido (el nodo de origen esta completado). */
  travelled: boolean
}

export interface ZoneLayout {
  phase: PhaseDetail
  top: number
  height: number
  centerX: number
  points: NodePoint[]
}

export interface MapLayout {
  width: number
  height: number
  zones: ZoneLayout[]
  segments: PathSegment[]
  points: NodePoint[]
  config: MapConfig
}

/** Un tramo suave entre `points[i]` y `points[i+1]` usando sus vecinos. */
function segmentPath(points: Point[], index: number): string {
  const p1 = points[index]
  const p2 = points[index + 1]
  const p0 = points[index - 1] ?? p1
  const p3 = points[index + 2] ?? p2

  const cp1 = {
    x: p1.x + (p2.x - p0.x) / 6,
    y: p1.y + (p2.y - p0.y) / 6,
  }
  const cp2 = {
    x: p2.x - (p3.x - p1.x) / 6,
    y: p2.y - (p3.y - p1.y) / 6,
  }

  return `M ${round(p1.x)} ${round(p1.y)} C ${round(cp1.x)} ${round(cp1.y)}, ${round(
    cp2.x,
  )} ${round(cp2.y)}, ${round(p2.x)} ${round(p2.y)}`
}

const round = (value: number) => Math.round(value * 10) / 10

export function buildMapLayout(
  phases: PhaseDetail[],
  config: MapConfig,
): MapLayout {
  const zones: ZoneLayout[] = []
  const points: NodePoint[] = []
  let cursor = 0

  phases.forEach((phase, zoneIndex) => {
    const nodes = [...phase.nodes].sort((a, b) => a.order_index - b.order_index)
    const zoneTop = cursor
    const zonePoints: NodePoint[] = nodes.map((node, i) => ({
      // El zigzag alterna columnas y anade una leve variacion por zona
      // para que ninguna zona se vea identica a la anterior.
      x: config.columns[(i + zoneIndex) % config.columns.length],
      y: zoneTop + config.headerHeight + i * config.nodeGap,
      node,
      zoneIndex,
    }))

    const height =
      config.headerHeight +
      Math.max(nodes.length - 1, 0) * config.nodeGap +
      config.zonePaddingBottom

    zones.push({
      phase,
      top: zoneTop,
      height,
      centerX: config.width / 2,
      points: zonePoints,
    })
    points.push(...zonePoints)
    cursor += height + config.zoneGap
  })

  const segments: PathSegment[] = []
  for (let i = 0; i < points.length - 1; i += 1) {
    segments.push({
      d: segmentPath(points, i),
      zoneIndex: points[i].zoneIndex,
      travelled: points[i].node.status === 'COMPLIANT',
    })
  }

  return {
    width: config.width,
    height: Math.max(cursor, config.headerHeight),
    zones,
    segments,
    points,
    config,
  }
}
