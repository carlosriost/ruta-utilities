/**
 * Punto de entrada de la version descargable.
 *
 * Diferencias con la version servida por API:
 *  - no hay inicio de sesion ni datos personales,
 *  - el estado del recorrido lo calcula `offline/engine.ts`,
 *  - la navegacion vive en memoria.
 *
 * MemoryRouter es deliberado: al abrir el archivo desde el disco (file://) el
 * documento tiene origen nulo y el navegador rechaza history.pushState /
 * replaceState con un SecurityError, lo que romperia BrowserRouter y tambien
 * HashRouter. En memoria no se toca la URL y el archivo funciona igual desde
 * el escritorio, una carpeta de red o SharePoint.
 *
 * En GitHub Pages (`--mode pages` con configuracion de Firebase) el avance es
 * compartido: antes de pintar se espera la primera lectura de Firestore.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { MemoryRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppLayout } from '@/components/AppLayout'
import { CourseProvider } from '@/context/CourseContext'
import { MapPage } from '@/pages/MapPage'
import { ProgressPage } from '@/pages/ProgressPage'
import { BadgesPage } from '@/pages/BadgesPage'
import { AboutPage } from '@/pages/AboutPage'
import { StorageWarning } from './StorageWarning'
import { SharedSync } from './SharedSync'
import './offline.css'

const container = document.getElementById('root')
if (!container) throw new Error('No se encontro el elemento #root')

// Constante en tiempo de compilacion: en el archivo descargable esta rama (y
// Firebase con ella) desaparece del bundle.
const shared =
  import.meta.env.MODE === 'pages' && Boolean(import.meta.env.VITE_FIREBASE_PROJECT_ID)

async function start() {
  const store = shared ? await import('./sharedStore') : null
  if (store) await store.connect()

  createRoot(container!).render(
    <StrictMode>
      <MemoryRouter initialEntries={['/mapa']}>
        <CourseProvider>
          {store ? <SharedSync store={store} /> : <StorageWarning />}
          <Routes>
            <Route element={<AppLayout />}>
              <Route path="/mapa" element={<MapPage />} />
              <Route path="/progreso" element={<ProgressPage />} />
              <Route path="/insignias" element={<BadgesPage />} />
              <Route path="/acerca" element={<AboutPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/mapa" replace />} />
          </Routes>
        </CourseProvider>
      </MemoryRouter>
    </StrictMode>,
  )
}

void start()
