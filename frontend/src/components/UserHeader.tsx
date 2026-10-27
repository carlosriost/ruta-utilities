import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { Award, BarChart3, Info, Map as MapIcon, Menu, X } from 'lucide-react'

const NAV_ITEMS = [
  { to: '/mapa', label: 'Mapa', icon: MapIcon },
  { to: '/progreso', label: 'Mi progreso', icon: BarChart3 },
  { to: '/insignias', label: 'Insignias', icon: Award },
  { to: '/acerca', label: 'Acerca de la Ruta', icon: Info },
]

/** Logotipo placeholder: sustituir por la marca oficial cuando este disponible. */
function BrandMark() {
  return (
    <span className="flex items-center gap-2.5">
      <span
        aria-hidden
        className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-gold to-brand-goldsoft shadow-soft"
      >
        <span className="text-lg font-extrabold text-brand-ink">RU</span>
      </span>
      <span className="leading-none">
        <span className="block font-display text-lg font-extrabold text-brand-ink">
          Ruta Utilities
        </span>
        <span className="block text-[11px] font-bold uppercase tracking-wider text-brand-slate">
          Seguridad VPO
        </span>
      </span>
    </span>
  )
}

/** Cabecera de la aplicacion. No hay sesion ni datos personales. */
export function UserHeader() {
  const [menuOpen, setMenuOpen] = useState(false)

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2 rounded-pill px-3.5 py-2 text-sm font-bold transition ${
      isActive
        ? 'bg-brand-blue text-white shadow-soft'
        : 'text-brand-slate hover:bg-black/5 hover:text-brand-ink'
    }`

  return (
    <header className="sticky top-0 z-40 border-b border-black/5 bg-white/85 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center gap-4 px-4 py-3">
        <Link to="/mapa" aria-label="Ir al mapa">
          <BrandMark />
        </Link>

        <nav aria-label="Navegacion principal" className="ml-auto hidden lg:block">
          <ul className="flex items-center gap-1">
            {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
              <li key={to}>
                <NavLink to={to} className={linkClass}>
                  <Icon aria-hidden className="h-4 w-4" />
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        <div className="ml-auto flex items-center gap-3">
          <button
            type="button"
            onClick={() => setMenuOpen((open) => !open)}
            className="rounded-pill p-2.5 text-brand-ink transition hover:bg-black/5 lg:hidden"
            aria-label={menuOpen ? 'Cerrar menu' : 'Abrir menu'}
            aria-expanded={menuOpen}
          >
            {menuOpen ? (
              <X aria-hidden className="h-6 w-6" />
            ) : (
              <Menu aria-hidden className="h-6 w-6" />
            )}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {menuOpen && (
          <motion.nav
            aria-label="Navegacion movil"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden border-t border-black/5 bg-white lg:hidden"
          >
            <ul className="space-y-1 p-3">
              {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
                <li key={to}>
                  <NavLink
                    to={to}
                    onClick={() => setMenuOpen(false)}
                    className={linkClass}
                  >
                    <Icon aria-hidden className="h-4 w-4" />
                    {label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  )
}
