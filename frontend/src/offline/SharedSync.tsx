import { useEffect, useState } from 'react'
import { CloudOff } from 'lucide-react'
import { useCourse } from '@/hooks/useCourse'
import type { SharedStatus } from './sharedStore'

type Store = typeof import('./sharedStore')

/**
 * Mantiene el mapa al dia con el avance compartido (version GitHub Pages).
 *
 * Cada vez que alguien marca un tema, Firestore avisa, el motor ya tiene el
 * dato nuevo y aqui solo se vuelve a leer el recorrido. Si no hay conexion se
 * avisa: lo marcado se guarda y se envia en cuanto vuelva la red.
 */
export function SharedSync({ store }: { store: Store }) {
  const { refresh } = useCourse()
  const [status, setStatus] = useState<SharedStatus>(store.getStatus())

  useEffect(
    () =>
      store.subscribe((next) => {
        setStatus(next)
        void refresh()
      }),
    [store, refresh],
  )

  if (status !== 'error') return null

  return (
    <div
      role="alert"
      className="flex items-start gap-3 bg-zone-ambersoft px-4 py-3 text-sm font-bold text-[#B96908]"
    >
      <CloudOff aria-hidden className="mt-0.5 h-5 w-5 shrink-0" />
      <p>
        No pudimos conectar con el avance compartido. Lo que marques se guarda
        en este navegador y se enviara cuando vuelva la conexion.
      </p>
    </div>
  )
}
