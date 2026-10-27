/**
 * Design tokens de Ruta Utilities.
 *
 * Toda la paleta vive aqui y en `src/index.css`. Para adaptar el branding
 * corporativo mas adelante basta con cambiar estos valores: ningun componente
 * escribe colores en crudo.
 */
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // --- Marca -------------------------------------------------------
        brand: {
          gold: '#F5B301',
          goldsoft: '#FFD75E',
          blue: '#1F4FD8',
          bluesoft: '#5B8DEF',
          ink: '#16233A',
          slate: '#5A6B87',
          cream: '#FFFCF3',
          paper: '#FFFFFF',
        },
        // --- Zonas del mapa ---------------------------------------------
        zone: {
          mint: '#2FBF87',
          mintsoft: '#D6F6E7',
          sky: '#2E8FEA',
          skysoft: '#DCEDFD',
          amber: '#F09520',
          ambersoft: '#FEEBD2',
          grape: '#7C5CE0',
          grapesoft: '#E8E1FC',
          teal: '#0FA3A3',
          tealsoft: '#D3F1F1',
        },
        // --- Estados ------------------------------------------------------
        state: {
          locked: '#B7C0D0',
          lockedsoft: '#EDF1F6',
          success: '#22A06B',
          danger: '#E5544B',
        },
      },
      fontFamily: {
        sans: ['"Nunito"', '"Segoe UI"', 'system-ui', 'sans-serif'],
        display: ['"Baloo 2"', '"Nunito"', '"Segoe UI"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        card: '1.5rem',
        pill: '999px',
      },
      boxShadow: {
        soft: '0 10px 30px -12px rgba(22, 35, 58, 0.22)',
        lift: '0 18px 40px -16px rgba(22, 35, 58, 0.32)',
        node: '0 8px 18px -6px rgba(22, 35, 58, 0.35)',
        inner_soft: 'inset 0 2px 6px rgba(22, 35, 58, 0.08)',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        drift: {
          '0%': { transform: 'translateX(0px)' },
          '100%': { transform: 'translateX(24px)' },
        },
        pulseRing: {
          '0%': { transform: 'scale(0.9)', opacity: '0.7' },
          '70%': { transform: 'scale(1.35)', opacity: '0' },
          '100%': { transform: 'scale(1.35)', opacity: '0' },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        float: 'float 5s ease-in-out infinite',
        drift: 'drift 9s ease-in-out infinite alternate',
        pulseRing: 'pulseRing 2.2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        shimmer: 'shimmer 1.6s infinite',
      },
    },
  },
  plugins: [],
}
