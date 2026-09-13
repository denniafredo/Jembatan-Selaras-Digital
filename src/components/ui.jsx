import { useEffect, useRef, useState } from 'react'

/**
 * Fades content in once as it scrolls into view.
 * Uses a single IntersectionObserver per element and unobserves after firing,
 * so nothing is left listening on scroll.
 */
export function Reveal({ children, delay = 0, as: Tag = 'div', className = '' }) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    if (!('IntersectionObserver' in window)) {
      el.classList.add('is-visible')
      return
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          observer.unobserve(entry.target)
        }
      },
      { threshold: 0.12, rootMargin: '0px 0px -8% 0px' },
    )

    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  return (
    <Tag
      ref={ref}
      className={`reveal ${className}`}
      style={delay ? { '--reveal-delay': `${delay}ms` } : undefined}
    >
      {children}
    </Tag>
  )
}

/** Infinite horizontal ticker. Children are duplicated once for a seamless loop. */
export function Marquee({ children, duration = 32, pauseOnHover = true, className = '' }) {
  return (
    <div
      className={`overflow-hidden ${pauseOnHover ? 'marquee-paused' : ''} ${className}`}
      aria-hidden="true"
    >
      <div className="marquee-track" style={{ '--marquee-duration': `${duration}s` }}>
        <div className="flex shrink-0 items-center">{children}</div>
        <div className="flex shrink-0 items-center">{children}</div>
      </div>
    </div>
  )
}

export function Eyebrow({ children, className = '' }) {
  return <span className={`eyebrow ${className}`}>{children}</span>
}

export function ArrowIcon({ className = 'h-4 w-4' }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M7 17 17 7" />
      <path d="M8 7h9v9" />
    </svg>
  )
}

/**
 * Contact icons. Drawn on the same 24px grid and stroked with currentColor so
 * they inherit whatever text colour the row is using.
 */
function Stroke({ className, children }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      {children}
    </svg>
  )
}

export function MailIcon({ className = 'h-5 w-5' }) {
  return (
    <Stroke className={className}>
      <rect x="2.5" y="4.5" width="19" height="15" rx="2.5" />
      <path d="m3.5 7 7.3 5.3a2 2 0 0 0 2.4 0L20.5 7" />
    </Stroke>
  )
}

export function PhoneIcon({ className = 'h-5 w-5' }) {
  return (
    <Stroke className={className}>
      <path d="M6.6 3h-.8A2.8 2.8 0 0 0 3 5.8c0 8.4 6.8 15.2 15.2 15.2a2.8 2.8 0 0 0 2.8-2.8v-.8a1.4 1.4 0 0 0-1-1.35l-3.4-1a1.4 1.4 0 0 0-1.5.5l-.8 1a11.7 11.7 0 0 1-5.65-5.65l1-.8a1.4 1.4 0 0 0 .5-1.5l-1-3.4A1.4 1.4 0 0 0 6.6 3Z" />
    </Stroke>
  )
}

export function WhatsAppIcon({ className = 'h-5 w-5' }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden="true">
      <path d="M12.04 2C6.6 2 2.2 6.4 2.2 11.84c0 1.74.46 3.44 1.32 4.93L2.1 22l5.36-1.4a9.8 9.8 0 0 0 4.58 1.14h.01c5.43 0 9.84-4.4 9.84-9.84C21.89 6.4 17.47 2 12.04 2Zm0 17.98h-.01a8.2 8.2 0 0 1-4.15-1.13l-.3-.18-3.08.8.83-3-.2-.31a8.13 8.13 0 0 1-1.25-4.32c0-4.5 3.67-8.17 8.17-8.17a8.17 8.17 0 0 1 .01 16.31Zm4.47-6.1c-.24-.13-1.45-.72-1.68-.8-.22-.08-.39-.12-.55.12-.16.25-.62.8-.77.97-.14.16-.28.18-.52.06-.25-.12-1.04-.38-1.97-1.22-.73-.65-1.22-1.45-1.37-1.7-.14-.24-.01-.37.11-.5.11-.1.25-.28.37-.42.12-.15.16-.25.24-.41.08-.17.04-.31-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47c-.16 0-.43.06-.65.3-.22.25-.85.84-.85 2.04s.88 2.37 1 2.53c.12.17 1.72 2.63 4.17 3.69.58.25 1.04.4 1.39.51.58.19 1.12.16 1.54.1.47-.07 1.45-.59 1.66-1.17.2-.57.2-1.06.14-1.16-.06-.1-.22-.16-.46-.28Z" />
    </svg>
  )
}

export function PinIcon({ className = 'h-5 w-5' }) {
  return (
    <Stroke className={className}>
      <path d="M12 21.5s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z" />
      <circle cx="12" cy="10.4" r="2.6" />
    </Stroke>
  )
}

export function CheckIcon({ className = 'h-4 w-4' }) {
  return (
    <Stroke className={className}>
      <path d="m4.5 12.5 5 5 10-11" />
    </Stroke>
  )
}

/** Primary pill button used for the main calls to action. */
export function Button({ href, children, variant = 'solid', className = '', ...rest }) {
  const base =
    'group inline-flex items-center justify-center gap-2.5 rounded-full px-7 py-3.5 text-sm font-bold tracking-tight transition-all duration-300'

  const styles = {
    solid: 'bg-brand text-white hover:bg-brand-dark hover:shadow-lg hover:shadow-brand/25',
    outline: 'border border-line bg-transparent text-ink-900 hover:border-brand hover:text-brand',
    ghost: 'bg-white text-ink-900 hover:bg-brand hover:text-white',
  }

  const content = (
    <>
      {children}
      <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
    </>
  )

  if (href) {
    return (
      <a href={href} className={`${base} ${styles[variant]} ${className}`} {...rest}>
        {content}
      </a>
    )
  }

  return (
    <button type="button" className={`${base} ${styles[variant]} ${className}`} {...rest}>
      {content}
    </button>
  )
}

/** Counts up to `value` the first time the element is on screen. */
export function CountUp({ value, suffix = '', duration = 1400 }) {
  const ref = useRef(null)
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduced || !('IntersectionObserver' in window)) {
      setDisplay(value)
      return
    }

    let frame = 0
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return
        observer.unobserve(entry.target)

        const start = performance.now()
        const tick = (now) => {
          const progress = Math.min((now - start) / duration, 1)
          // ease-out-cubic
          const eased = 1 - Math.pow(1 - progress, 3)
          setDisplay(Math.round(value * eased))
          if (progress < 1) frame = requestAnimationFrame(tick)
        }
        frame = requestAnimationFrame(tick)
      },
      { threshold: 0.4 },
    )

    observer.observe(el)
    return () => {
      observer.disconnect()
      cancelAnimationFrame(frame)
    }
  }, [value, duration])

  return (
    <span ref={ref}>
      {display}
      {suffix}
    </span>
  )
}
