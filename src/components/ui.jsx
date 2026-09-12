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
