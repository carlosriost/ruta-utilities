import {
  Check,
  ClipboardList,
  Compass,
  Database,
  Gauge,
  Lock,
  Server,
  Sparkles,
  Trophy,
} from 'lucide-react'
import { MascotGuide } from '@/components/MascotGuide'
import { useCourse } from '@/hooks/useCourse'
import { zoneTokens } from '@/utils/theme'
import { iconFor } from '@/utils/icons'

const HOW_IT_WORKS = [
  {
    icon: ClipboardList,
    title: 'Una lista, no un examen',
    text: 'Cada punto del mapa agrupa los requisitos VPO de un bloque. Marcas cada tema como cumple o no cumple.',
  },
  {
    icon: Check,
    title: 'Sin cuestionarios',
    text: 'No hay preguntas ni puntajes: la ruta registra el estado de los requisitos, no evalua a las personas.',
  },
  {
    icon: Gauge,
    title: 'Cumplimiento del nivel',
    text: 'El porcentaje de un nivel son sus temas cumplidos sobre el total de temas del nivel.',
  },
  {
    icon: Lock,
    title: 'Umbral por nivel',
    text: 'El nivel 0 exige 100%; el 1, 90%; el 2, 80%; y el 3 y el 4, 70%. Al alcanzarlo se abre el siguiente.',
  },
  {
    icon: Compass,
    title: 'Se recorre libre',
    text: 'Dentro de un nivel abierto puedes entrar a cualquier punto y marcar sus temas en el orden que quieras.',
  },
  {
    icon: Sparkles,
    title: 'Insignias',
    text: 'Se conceden solas cuando un nivel alcanza su umbral de cumplimiento.',
  },
  {
    icon: Trophy,
    title: 'La meta',
    text: 'Que los cinco niveles alcancen su umbral. Eso te convierte en Maestro Utilities.',
  },
]

export function AboutPage() {
  const { course } = useCourse()

  return (
    <div className="space-y-8">
      <header>
        <h1 className="font-display text-3xl font-extrabold text-brand-ink">
          Acerca de la Ruta
        </h1>
        <p className="mt-1 max-w-2xl font-semibold text-brand-slate">
          Ruta Utilities es una lista de verificacion interactiva de los
          requisitos VPO del pilar Safety: un mapa con los cinco niveles de
          madurez donde se marca, tema por tema, que cumple y que no.
        </p>
      </header>

      <MascotGuide
        message="Soy Gotix, tu guia. Te acompano durante todo el recorrido."
        mood="happy"
      />

      <section aria-label="Como funciona" className="space-y-4">
        <h2 className="font-display text-2xl font-extrabold text-brand-ink">
          Como funciona
        </h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {HOW_IT_WORKS.map(({ icon: Icon, title, text }) => (
            <article key={title} className="card-soft p-5">
              <span
                aria-hidden
                className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl bg-brand-cream"
              >
                <Icon className="h-5 w-5 text-brand-gold" strokeWidth={2.4} />
              </span>
              <h3 className="font-extrabold text-brand-ink">{title}</h3>
              <p className="mt-1 text-sm text-brand-slate">{text}</p>
            </article>
          ))}
        </div>
      </section>

      {course && (
        <section aria-label="Niveles del recorrido" className="space-y-4">
          <h2 className="font-display text-2xl font-extrabold text-brand-ink">
            Los cinco niveles
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {course.phases.map((phase) => {
              const tokens = zoneTokens(phase.theme)
              const Icon = iconFor(phase.icon)
              return (
                <article key={phase.id} className="card-soft flex gap-4 p-5">
                  <span
                    aria-hidden
                    className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl"
                    style={{ backgroundColor: tokens.soft }}
                  >
                    <Icon className="h-6 w-6" style={{ color: tokens.main }} strokeWidth={2.3} />
                  </span>
                  <div>
                    <p
                      className="text-xs font-extrabold uppercase tracking-[0.16em]"
                      style={{ color: tokens.deep }}
                    >
                      Nivel VPO {phase.order_index}
                    </p>
                    <h3 className="font-display text-xl font-extrabold text-brand-ink">
                      {phase.name}
                    </h3>
                    <p className="mt-1 text-sm text-brand-slate">{phase.description}</p>
                    <p className="mt-2 text-xs font-bold text-brand-slate">
                      {phase.state.total_requirements} temas · umbral{' '}
                      {phase.unlock_threshold}%
                    </p>
                  </div>
                </article>
              )
            })}
          </div>
        </section>
      )}

      <section aria-label="Arquitectura" className="card-soft p-6">
        <h2 className="font-display text-2xl font-extrabold text-brand-ink">
          Como esta construida
        </h2>
        <p className="mt-2 max-w-3xl text-sm font-semibold text-brand-slate">
          Esta es una version funcional. Las reglas (cumplimiento, umbrales y
          desbloqueos) se calculan siempre fuera de la interfaz, y el avance
          queda guardado: si cierras y vuelves a entrar, sigue donde estaba.
        </p>

        <div className="mt-5 grid gap-4 sm:grid-cols-3">
          {[
            { icon: Compass, title: 'React + TypeScript', text: 'Representa el estado que envia la API.' },
            { icon: Server, title: 'FastAPI', text: 'Calcula progreso, desbloqueos e insignias.' },
            { icon: Database, title: 'PostgreSQL', text: 'Fuente de verdad de contenido y avance.' },
          ].map(({ icon: Icon, title, text }) => (
            <div key={title} className="rounded-2xl bg-brand-cream p-4">
              <Icon aria-hidden className="mb-2 h-5 w-5 text-brand-blue" />
              <p className="font-extrabold text-brand-ink">{title}</p>
              <p className="text-sm text-brand-slate">{text}</p>
            </div>
          ))}
        </div>

        <p className="mt-5 rounded-2xl border-2 border-dashed border-brand-blue/25 p-4 text-sm font-semibold text-brand-slate">
          El acceso corporativo con Microsoft Entra ID se integrará sustituyendo
          el servicio de autenticación, sin reconstruir la aplicación. La
          mascota y el logotipo son placeholders neutrales pendientes de
          reemplazo por la marca oficial.
        </p>
      </section>
    </div>
  )
}
