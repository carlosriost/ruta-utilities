/** Utilidades de formato para la interfaz. */

export function firstName(fullName: string | undefined | null): string {
  if (!fullName) return ''
  return fullName.trim().split(/\s+/)[0]
}

export function initials(fullName: string | undefined | null): string {
  if (!fullName) return '?'
  const parts = fullName.trim().split(/\s+/).slice(0, 2)
  return parts.map((part) => part.charAt(0).toUpperCase()).join('')
}

export function formatDate(value: string | null | undefined): string {
  if (!value) return 'Sin registro'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'Sin registro'
  return date.toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

/** Divide un texto en lineas para poder pintarlo dentro de un SVG. */
export function wrapText(text: string, maxChars: number, maxLines = 2): string[] {
  const words = text.split(/\s+/)
  const lines: string[] = []
  let current = ''

  for (const word of words) {
    const candidate = current ? `${current} ${word}` : word
    if (candidate.length <= maxChars) {
      current = candidate
    } else {
      if (current) lines.push(current)
      current = word
      if (lines.length === maxLines - 1) break
    }
  }
  if (current) lines.push(current)

  if (lines.length > maxLines) lines.length = maxLines
  const consumed = lines.join(' ').split(/\s+/).length
  if (consumed < words.length && lines.length > 0) {
    const last = lines[lines.length - 1]
    lines[lines.length - 1] =
      last.length > maxChars - 1 ? `${last.slice(0, maxChars - 1)}...` : `${last}...`
  }
  return lines
}

/** Convierte los saltos de linea del contenido en parrafos. */
export function toParagraphs(body: string): string[] {
  return body
    .split(/\n{2,}/)
    .map((block) => block.trim())
    .filter(Boolean)
}
