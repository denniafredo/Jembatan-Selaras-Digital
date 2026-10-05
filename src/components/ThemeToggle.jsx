import { useEffect, useState } from 'react'
import { MoonIcon, SunIcon } from './ui'

const STORAGE_KEY = 'jsd-theme'

function savedTheme() {
  try {
    const theme = localStorage.getItem(STORAGE_KEY)
    return theme === 'light' || theme === 'dark' ? theme : null
  } catch {
    return null
  }
}

/**
 * Light / dark switch. The inline script in index.html applies the saved choice (or the OS
 * preference) to <html data-theme> before first paint; this button flips it and remembers
 * the choice. Until the visitor picks one, the site keeps following the OS setting.
 */
export default function ThemeToggle({ className = '' }) {
  const [theme, setTheme] = useState(() =>
    document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light',
  )

  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const onChange = (e) => {
      if (savedTheme()) return
      const next = e.matches ? 'dark' : 'light'
      document.documentElement.dataset.theme = next
      setTheme(next)
    }
    media.addEventListener('change', onChange)
    return () => media.removeEventListener('change', onChange)
  }, [])

  const toggle = () => {
    const next = theme === 'dark' ? 'light' : 'dark'
    try {
      localStorage.setItem(STORAGE_KEY, next)
    } catch {
      // Private mode: the switch still works for this visit.
    }
    const apply = () => {
      document.documentElement.dataset.theme = next
      setTheme(next)
    }
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (document.startViewTransition && !reduced) document.startViewTransition(apply)
    else apply()
  }

  const dark = theme === 'dark'
  const label = dark ? 'Switch to light theme' : 'Switch to dark theme'

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={label}
      title={label}
      className={`relative flex h-11 w-11 items-center justify-center rounded-full border border-line text-ink-900 transition-colors hover:border-brand hover:text-brand ${className}`}
    >
      <SunIcon
        className={`absolute h-5 w-5 transition duration-300 motion-reduce:transition-none ${
          dark ? 'rotate-0 scale-100 opacity-100' : '-rotate-90 scale-50 opacity-0'
        }`}
      />
      <MoonIcon
        className={`absolute h-5 w-5 transition duration-300 motion-reduce:transition-none ${
          dark ? 'rotate-90 scale-50 opacity-0' : 'rotate-0 scale-100 opacity-100'
        }`}
      />
    </button>
  )
}
