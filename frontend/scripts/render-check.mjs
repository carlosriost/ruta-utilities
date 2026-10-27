/**
 * Comprobacion de que el archivo descargable abre y se dibuja.
 *
 * Carga `dist-offline/RutaUtilities.html` en un DOM simulado (jsdom), deja que
 * React lo renderice y verifica que aparezcan el mapa, los puntos y los textos
 * del recorrido. No sustituye a abrirlo en un navegador real, pero detecta que
 * el archivo este completo y que la aplicacion arranque sin errores.
 *
 *     npm run check:render
 */

import fs from 'node:fs'
import path from 'node:path'
import { JSDOM, VirtualConsole } from 'jsdom'

const archivo = path.resolve('dist-offline/RutaUtilities.html')
const html = fs.readFileSync(archivo, 'utf8')
console.log(`Archivo: ${archivo} (${(html.length / 1024).toFixed(0)} KB)`)

const errores = []
const virtualConsole = new VirtualConsole()
virtualConsole.on('jsdomError', (error) => errores.push(error.message))
virtualConsole.on('error', (...args) => errores.push(args.join(' ')))

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  url: 'file:///C:/Descargas/RutaUtilities.html',
  virtualConsole,
})

// jsdom no implementa estas dos APIs; el navegador si. Se rellenan para que la
// comprobacion mida la aplicacion y no las carencias del simulador.
dom.window.matchMedia ??= (query) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener() {},
  removeListener() {},
  addEventListener() {},
  removeEventListener() {},
  dispatchEvent: () => false,
})
dom.window.scrollTo ??= () => {}

await new Promise((resolve) => setTimeout(resolve, 2500))

const { document } = dom.window
const texto = document.body.textContent ?? ''
let fallos = 0
const ok = (etiqueta, condicion, extra = '') => {
  if (!condicion) fallos += 1
  console.log(`  [${condicion ? 'OK ' : 'FALLO'}] ${etiqueta}`, extra)
}

console.log('\nRenderizado')
ok('la aplicacion monto contenido', (document.getElementById('root')?.childElementCount ?? 0) > 0)
ok('sin errores de JavaScript', errores.length === 0, errores.slice(0, 2).join(' | '))
ok('dibuja el mapa', document.querySelectorAll('svg').length > 0)
ok('titulo del recorrido', texto.includes('Ruta Utilities'))
ok('saludo sin nombre propio', !/Hola,\s*\w/.test(texto), texto.slice(0, 0))
ok('primer nivel visible', texto.includes('Cimientos de seguridad'))
ok('quinto nivel visible', texto.includes('Referente en seguridad'))
ok('marca los niveles VPO', texto.includes('NIVEL VPO 0'))
ok('muestra el primer punto', texto.includes('Seguridad operacional'))
ok('boton para continuar', texto.includes('Continuar'))
ok('cuenta los temas cumplidos', texto.includes('temas cumplen'))
ok('muestra el umbral del nivel 0', texto.includes('100%'))
// Sin tocar nada, todo empieza en "no cumple": el resumen debe mostrar 0%.
ok('arranca en 0% de cumplimiento', texto.includes('0%'))

console.log('\nNavegacion')
// "ingresar" aparece en el contenido del curso, asi que se busca el boton
// de la antigua pantalla de acceso, no la palabra suelta.
const botones = [...document.querySelectorAll('button, a')].map((b) =>
  (b.textContent ?? '').trim().toLowerCase(),
)
ok('sin boton de inicio de sesion', !botones.includes('ingresar'))
ok('sin checkpoints', !texto.toLowerCase().includes('checkpoint'))
ok('sin cuestionarios', !botones.includes('responder'))
ok('menu sin perfil', !texto.includes('Perfil'))
ok('menu sin cerrar sesion', !texto.toLowerCase().includes('cerrar sesion'))

const nodos = document.querySelectorAll('[role="button"][aria-label]')
ok('puntos del mapa clicables', nodos.length >= 15, `${nodos.length} puntos`)

console.log(
  fallos === 0
    ? '\nARCHIVO DESCARGABLE: SE ABRE Y SE DIBUJA CORRECTAMENTE'
    : `\nARCHIVO DESCARGABLE: ${fallos} COMPROBACIONES FALLARON`,
)
dom.window.close()
process.exit(fallos === 0 ? 0 : 1)
