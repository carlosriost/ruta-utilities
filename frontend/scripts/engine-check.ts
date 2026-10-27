/**
 * Verificacion del motor de la version descargable.
 *
 * La version servida por API tiene sus reglas cubiertas por pytest. El archivo
 * descargable lleva su propia copia de esas reglas, asi que necesita su propia
 * verificacion: este script recorre los cinco niveles sin navegador y
 * comprueba que el resultado sea el mismo.
 *
 * Un tema es binario: cumple o no cumple, con "no cumple" como valor por
 * defecto. Por eso, salvo que se diga lo contrario, marcar un tema en estas
 * pruebas significa activarlo a "cumple"; dejarlo intacto ya lo deja en "no
 * cumple" sin que haga falta ninguna llamada.
 *
 *     npm run check:offline
 */

import * as engine from '../src/offline/engine'

let fallos = 0

function ok(etiqueta: string, condicion: boolean, extra: unknown = '') {
  if (!condicion) fallos += 1
  console.log(`  [${condicion ? 'OK ' : 'FALLO'}] ${etiqueta}`, extra === '' ? '' : extra)
}

/** Todos los temas de un nivel, como pares (punto, codigo). */
function temasDelNivel(indice: number): Array<[number, string]> {
  const fase = engine.getCourse().phases[indice]
  return fase.nodes.flatMap((node) =>
    engine
      .getNodeDetail(node.id)
      .content.requirements.map((r) => [node.id, r.code] as [number, string]),
  )
}

/** Marca como cumplidos todos los temas de un nivel. */
function cumplirNivel(indice: number) {
  let ultimo = null as ReturnType<typeof engine.setRequirement>['state'] | null
  for (const [nodeId, code] of temasDelNivel(indice)) {
    ultimo = engine.setRequirement(nodeId, code, true).state
  }
  return ultimo
}

console.log('1. Estado inicial: todo en "no cumple"')
engine.reset()
const inicial = engine.getCourse()
ok('5 niveles', inicial.phases.length === 5, inicial.phases.length)
ok('60 puntos', inicial.summary.total_nodes === 60, inicial.summary.total_nodes)
ok('185 temas', inicial.summary.total_requirements === 185, inicial.summary.total_requirements)
ok('nada cumple', inicial.summary.met_requirements === 0)
ok('todo cuenta como brecha', inicial.summary.failed_requirements === 185)
ok('cumplimiento 0%', inicial.summary.general_progress === 0)
ok('solo el primer nivel abierto', inicial.summary.unlocked_phases === 1)
ok(
  'umbrales 100/90/80/70/70',
  JSON.stringify(inicial.phases.map((p) => p.unlock_threshold)) ===
    JSON.stringify([100, 90, 80, 70, 70]),
  inicial.phases.map((p) => p.unlock_threshold).join('/'),
)
ok(
  'todos los puntos del nivel abierto ya tienen brechas visibles',
  inicial.phases[0].nodes.every((n) => n.status === 'HAS_GAPS'),
)
ok(
  'los temas ya aparecen como no-cumple sin tocar nada',
  engine.getNodeDetail(inicial.phases[0].nodes[0].id).content.requirements.every(
    (r) => r.meets === false,
  ),
)

console.log('2. Punto de nivel bloqueado')
let bloqueado: unknown = null
try {
  engine.getNodeDetail(inicial.phases[1].nodes[0].id)
} catch (error) {
  bloqueado = error
}
ok('abrirlo falla', bloqueado instanceof engine.LockedError)

console.log('3. Marcar y desmarcar un tema')
const punto = inicial.phases[0].nodes[0]
const detalle = engine.getNodeDetail(punto.id)
ok('trae sus temas', detalle.content.requirements.length === 12, detalle.content.requirements.length)
ok('codigo trazable', detalle.content.requirements[0].code === 'R.1.1.2.1')

const primerCodigo = detalle.content.requirements[0].code
const marcado = engine.setRequirement(punto.id, primerCodigo, true)
ok('queda cumplido', marcado.meets === true)
ok('el punto sigue con brechas (faltan los demas)', marcado.state.node_status === 'HAS_GAPS')
ok('suma un tema cumplido', marcado.state.node_met === 1)

const desmarcado = engine.setRequirement(punto.id, primerCodigo, false)
ok('se puede volver a "no cumple"', desmarcado.meets === false)
ok('deja de sumar al cumplimiento', desmarcado.state.node_met === 0)
ok(
  'y la marca desaparece del todo (no queda un tercer estado)',
  engine.getNodeDetail(punto.id).content.requirements[0].meets === false,
)

console.log('4. Punto que cumple todos sus temas')
// Se reinicia: en el paso 3 ya se marco y desmarco un tema, lo que habria
// concedido de una vez la insignia de "primer tema cumplido".
engine.reset()
let ultimoEstado = null as ReturnType<typeof engine.setRequirement>['state'] | null
let insigniaConcedida = false
for (const r of engine.getNodeDetail(punto.id).content.requirements) {
  const resultado = engine.setRequirement(punto.id, r.code, true)
  ultimoEstado = resultado.state
  if (resultado.state.new_badges.some((b) => b.slug === 'primer-paso')) {
    insigniaConcedida = true
  }
}
ok('estado COMPLIANT', ultimoEstado!.node_status === 'COMPLIANT')
ok('sin brechas', ultimoEstado!.node_failed === 0)
// La insignia se concede en la PRIMERA marca de "cumple" del recorrido, no
// necesariamente en la ultima (que es la que devuelve el loop).
ok('insignia de primer tema cumplido', insigniaConcedida)

console.log('5. El nivel 0 exige el 100%')
engine.reset()
const temas0 = temasDelNivel(0)
// Se cumplen todos menos el ultimo (que se deja en su "no cumple" por defecto).
for (const [nodeId, code] of temas0.slice(0, -1)) {
  engine.setRequirement(nodeId, code, true)
}
const [ultimoNodo, ultimoCodigo] = temas0[temas0.length - 1]

let curso = engine.getCourse()
ok('cumplimiento 98%', curso.phases[0].state.percent === 98, curso.phases[0].state.percent)
ok('no alcanza el umbral', curso.phases[0].state.compliant === false)
ok('el nivel 1 sigue cerrado', curso.phases[1].state.unlocked === false)

const cierre = engine.setRequirement(ultimoNodo, ultimoCodigo, true).state
ok('al 100% se abre el nivel 1', cierre.new_phase_unlocked === true)
ok('nombre del nivel', cierre.unlocked_phase_name === 'Control del riesgo', cierre.unlocked_phase_name)
ok('nivel previo', cierre.previous_phase_name === 'Cimientos de seguridad')
ok('insignia del nivel', engine.getBadges().badges.some((b) => b.slug === 'cimientos-vpo' && b.earned))

console.log('6. El nivel 1 se abre con el 90%')
const temas1 = temasDelNivel(1)
const total1 = temas1.length
let cumplidos = 0
let pendiente: [number, string] | null = null
for (const [nodeId, code] of temas1) {
  if (Math.round(((cumplidos + 1) * 100) / total1) <= 89) {
    engine.setRequirement(nodeId, code, true)
    cumplidos += 1
  } else {
    pendiente = [nodeId, code] // se deja en "no cumple"
  }
}
curso = engine.getCourse()
ok('se queda en 89%', curso.phases[1].state.percent === 89, curso.phases[1].state.percent)
ok('el nivel 2 sigue cerrado', curso.phases[2].state.unlocked === false)

ok('hay un tema pendiente para la prueba', pendiente !== null)
const cruce = engine.setRequirement(pendiente![0], pendiente![1], true).state
ok('al cruzar el 90% se abre el nivel 2', cruce.new_phase_unlocked === true)
ok('cumplimiento >= 90', cruce.phase_progress >= 90, cruce.phase_progress)

console.log('7. Recorrido completo')
engine.reset()
for (let nivel = 0; nivel < 5; nivel += 1) cumplirNivel(nivel)
const final = engine.getCourse()
ok('cumplimiento 100%', final.summary.general_progress === 100)
ok('185 temas cumplidos', final.summary.met_requirements === 185)
ok('60 puntos sin brechas', final.summary.compliant_nodes === 60)
ok('todos los niveles cumplen', final.summary.course_compliant === true)
const insignias = engine.getBadges()
ok('6 insignias', insignias.earned === 6 && insignias.total === 6, `${insignias.earned}/${insignias.total}`)

console.log('8. Brechas explicitas (no solo "sin tocar")')
engine.reset()
// Se activan y se vuelven a desactivar: deben quedar identicas al estado
// inicial, para confirmar que no aparece un tercer estado intermedio.
for (const [nodeId, code] of temasDelNivel(0)) {
  engine.setRequirement(nodeId, code, true)
  engine.setRequirement(nodeId, code, false)
}
const conBrechas = engine.getCourse()
ok('cumplimiento 0%', conBrechas.phases[0].state.percent === 0)
ok('el nivel 1 no se abre', conBrechas.phases[1].state.unlocked === false)
ok(
  'las brechas del nivel se cuentan igual que al inicio',
  conBrechas.phases[0].state.failed === conBrechas.phases[0].state.total_requirements,
)

console.log('9. Reinicio')
engine.reset()
const reiniciado = engine.getCourse()
ok('nada cumple', reiniciado.summary.met_requirements === 0)
ok('insignias en cero', engine.getBadges().earned === 0)
ok('el catalogo sigue intacto', reiniciado.summary.total_requirements === 185)

console.log(
  fallos === 0
    ? '\nMOTOR OFFLINE: TODAS LAS COMPROBACIONES PASARON'
    : `\nMOTOR OFFLINE: ${fallos} COMPROBACIONES FALLARON`,
)
process.exit(fallos === 0 ? 0 : 1)
