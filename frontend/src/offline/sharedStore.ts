/**
 * Avance compartido de la version de GitHub Pages.
 *
 * Todas las personas que abren el link leen y escriben el mismo documento de
 * Firestore (`ruta-utilities/progreso`). Cada marca se envia como una
 * operacion suelta (arrayUnion / arrayRemove) para que dos personas marcando
 * a la vez no se borren el trabajo, y `onSnapshot` trae al momento lo que
 * marcan los demas.
 *
 * Solo se carga cuando la compilacion es `--mode pages` y existe la
 * configuracion de Firebase (`.env.pages` o variables del workflow). El archivo
 * descargable de SharePoint nunca incluye este modulo.
 */

import { initializeApp } from 'firebase/app'
import {
  arrayRemove,
  arrayUnion,
  doc,
  initializeFirestore,
  onSnapshot,
  persistentLocalCache,
  setDoc,
} from 'firebase/firestore'
import * as engine from './engine'

export type SharedStatus = 'connecting' | 'online' | 'error'

type Listener = (status: SharedStatus) => void

let status: SharedStatus = 'connecting'
const listeners = new Set<Listener>()

function setStatus(next: SharedStatus) {
  status = next
  listeners.forEach((listener) => listener(next))
}

export function getStatus(): SharedStatus {
  return status
}

/** Avisa de cada cambio de estado y de cada actualizacion recibida. */
export function subscribe(listener: Listener): () => void {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

function toShared(data: Record<string, unknown> | undefined): engine.SharedProgress {
  return {
    metCodes: Array.isArray(data?.metCodes) ? (data.metCodes as string[]) : [],
    badges:
      data?.badges && typeof data.badges === 'object'
        ? (data.badges as Record<string, string>)
        : {},
    started_at: typeof data?.started_at === 'string' ? data.started_at : null,
  }
}

/**
 * Conecta el motor con Firestore. Resuelve con la primera lectura (o al
 * agotar la espera), para no pintar un mapa vacio y luego saltar de golpe.
 */
export function connect(): Promise<void> {
  const app = initializeApp({
    apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
    authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
    projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
    appId: import.meta.env.VITE_FIREBASE_APP_ID,
  })
  // La cache local deja seguir marcando sin red y envia todo al volver.
  const db = initializeFirestore(app, { localCache: persistentLocalCache() })
  const ref = doc(db, 'ruta-utilities', 'progreso')

  const write = (data: Record<string, unknown>) => {
    setDoc(ref, data, { merge: true }).catch(() => setStatus('error'))
  }

  engine.connectRemote({
    setCode: (code, meets) =>
      write({ metCodes: meets ? arrayUnion(code) : arrayRemove(code) }),
    awardBadge: (slug, awardedAt) => write({ badges: { [slug]: awardedAt } }),
    setStartedAt: (startedAt) => write({ started_at: startedAt }),
    reset: () => {
      // Sin merge: el documento queda exactamente vacio.
      setDoc(ref, { metCodes: [], badges: {}, started_at: null }).catch(() =>
        setStatus('error'),
      )
    },
  })

  return new Promise((resolve) => {
    const timeout = window.setTimeout(resolve, 8000)
    onSnapshot(
      ref,
      (snapshot) => {
        engine.hydrate(toShared(snapshot.data()))
        setStatus('online')
        window.clearTimeout(timeout)
        resolve()
      },
      () => {
        setStatus('error')
        window.clearTimeout(timeout)
        resolve()
      },
    )
  })
}
