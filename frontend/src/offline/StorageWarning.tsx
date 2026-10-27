import { AlertTriangle } from 'lucide-react'
import { storageAvailable } from './engine'

/**
 * Aviso cuando el navegador no deja guardar el avance.
 *
 * Ocurre en ventanas de incognito o con el almacenamiento bloqueado por
 * politica. El recorrido sigue funcionando, pero el avance se pierde al
 * cerrar la pestana, y es mejor decirlo antes de que la persona avance.
 */
export function StorageWarning() {
  if (storageAvailable()) return null

  return (
    <div
      role="alert"
      className="flex items-start gap-3 bg-zone-ambersoft px-4 py-3 text-sm font-bold text-[#B96908]"
    >
      <AlertTriangle aria-hidden className="mt-0.5 h-5 w-5 shrink-0" />
      <p>
        Este navegador no permite guardar tu avance (puede ser una ventana de
        incognito). Puedes hacer el recorrido, pero se perdera al cerrar la
        pestana. Abre el archivo en una ventana normal para conservarlo.
      </p>
    </div>
  )
}
