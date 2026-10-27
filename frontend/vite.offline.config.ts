import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import path from 'node:path'
import fs from 'node:fs'

/**
 * Compilacion de la version descargable.
 *
 * Produce UN SOLO archivo HTML autocontenido (`dist-offline/RutaUtilities.html`)
 * con el CSS, el JavaScript, el contenido del curso y las tipografias dentro.
 * No necesita servidor, ni base de datos, ni conexion a internet: se sube a
 * SharePoint, la persona lo descarga y lo abre.
 *
 * Los servicios HTTP se sustituyen por sus equivalentes locales mediante alias,
 * de modo que los componentes son exactamente los mismos en ambas versiones.
 *
 * Con `--mode pages` el mismo archivo sale como `dist-pages/index.html`, que es
 * lo que publica GitHub Pages (ver `.github/workflows/deploy-pages.yml`).
 */
const src = (...parts: string[]) => path.resolve(__dirname, 'src', ...parts)

export default defineConfig(({ mode }) => {
  const pages = mode === 'pages'
  const outDir = pages ? 'dist-pages' : 'dist-offline'
  const nombre = pages ? 'index.html' : 'RutaUtilities.html'

  return {
    plugins: [
      react(),
      viteSingleFile(),
      {
        name: 'entregable-sharepoint',
        closeBundle() {
          const dir = path.resolve(__dirname, outDir)
          const origen = path.join(dir, 'index.offline.html')
          if (!fs.existsSync(origen)) return

          // El bundle es IIFE, asi que el script no necesita ser de tipo modulo:
          // como script clasico evita restricciones al abrir el archivo desde el
          // disco (file://). A cambio deja de ser diferido, asi que hay que
          // moverlo al final del body para que #root ya exista al ejecutarse.
          const scripts: string[] = []
          let html = fs
            .readFileSync(origen, 'utf8')
            .replace(/<script type="module"([ >])/g, '<script$1')
            .replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, (bloque) => {
              scripts.push(bloque)
              return ''
            })
          // Reemplazo con funcion: el bundle contiene secuencias como "$&" que
          // una cadena de reemplazo interpretaria como patrones y corromperia.
          html = html.replace('</body>', () => `${scripts.join('\n')}\n  </body>`)
          const destino = path.join(dir, nombre)
          fs.writeFileSync(destino, html, 'utf8')
          fs.unlinkSync(origen)
          const kb = (fs.statSync(destino).size / 1024).toFixed(0)
          console.log(`\n  Entregable: ${outDir}/${nombre} (${kb} KB)\n`)
        },
      },
    ],
    resolve: {
      // El orden importa: las rutas concretas van antes que el comodin '@'.
      alias: [
        { find: '@/services/apiClient', replacement: src('offline/apiClient.ts') },
        { find: '@/services/courseApi', replacement: src('offline/courseApi.ts') },
        { find: '@/services/progressApi', replacement: src('offline/progressApi.ts') },
        { find: '@/services/badgeApi', replacement: src('offline/badgeApi.ts') },
        { find: '@', replacement: src() },
      ],
    },
    build: {
      outDir,
      emptyOutDir: true,
      // Sin trocear: todo tiene que caber en un unico archivo.
      assetsInlineLimit: 100 * 1024 * 1024,
      chunkSizeWarningLimit: 4096,
      rollupOptions: {
        input: path.resolve(__dirname, 'index.offline.html'),
        // Un solo archivo, sin modulos: todo queda dentro de una funcion.
        output: { format: 'iife', inlineDynamicImports: true },
      },
    },
  }
})
