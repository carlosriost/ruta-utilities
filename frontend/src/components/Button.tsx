import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { Loader2 } from 'lucide-react'

type Variant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'gold'
type Size = 'sm' | 'md' | 'lg'

const VARIANTS: Record<Variant, string> = {
  primary:
    'bg-brand-blue text-white shadow-soft hover:bg-[#1a44ba] focus-visible:bg-[#1a44ba]',
  gold: 'bg-brand-gold text-brand-ink shadow-soft hover:bg-[#e0a501]',
  secondary:
    'bg-white text-brand-ink border-2 border-black/10 hover:border-brand-blue/40 hover:text-brand-blue',
  ghost: 'bg-transparent text-brand-slate hover:bg-black/5',
  danger: 'bg-state-danger text-white shadow-soft hover:bg-[#c9433b]',
}

const SIZES: Record<Size, string> = {
  sm: 'px-4 py-2 text-sm',
  md: 'px-5 py-2.5 text-[15px]',
  lg: 'px-7 py-3.5 text-base tracking-wide',
}

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  loading?: boolean
  icon?: ReactNode
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className = '',
  disabled,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`btn-base ${VARIANTS[variant]} ${SIZES[size]} ${className}`}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      {...rest}
    >
      {loading ? <Loader2 aria-hidden className="h-4 w-4 animate-spin" /> : icon}
      {children}
    </button>
  )
}
