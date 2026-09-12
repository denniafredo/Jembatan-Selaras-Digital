import { useEffect, useState } from 'react'
import { Logo } from './Logo'
import { nav } from '../data/site'

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // Lock the page while the mobile drawer is open.
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''
    return () => {
      document.body.style.overflow = ''
    }
  }, [open])

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && setOpen(false)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  return (
    <>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-full focus:bg-brand focus:px-5 focus:py-2 focus:text-sm focus:font-bold focus:text-white"
      >
        Skip to content
      </a>

      <header
        className={`fixed inset-x-0 top-0 z-50 transition-all duration-300 ${
          scrolled || open
            ? 'border-b border-line/70 bg-paper/85 backdrop-blur-xl'
            : 'border-b border-transparent bg-transparent'
        }`}
      >
        <div className="shell flex h-[72px] items-center justify-between md:h-20">
          <a href="#top" aria-label="Jembatan Selaras Digital — home">
            <Logo compact />
          </a>

          <nav className="hidden items-center gap-1 lg:flex" aria-label="Main">
            {nav.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="relative rounded-full px-4 py-2 text-sm font-semibold text-ink transition-colors duration-200 hover:text-brand"
              >
                {item.label}
              </a>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <a
              href="#contact"
              className="hidden rounded-full bg-brand px-6 py-3 text-sm font-bold text-white transition-all duration-300 hover:bg-brand-dark hover:shadow-lg hover:shadow-brand/25 sm:inline-flex"
            >
              Start a project
            </a>

            <button
              type="button"
              onClick={() => setOpen((v) => !v)}
              aria-expanded={open}
              aria-controls="mobile-menu"
              aria-label={open ? 'Close menu' : 'Open menu'}
              className="flex h-11 w-11 items-center justify-center rounded-full border border-line text-ink-900 transition-colors hover:border-brand hover:text-brand lg:hidden"
            >
              <span className="relative block h-3.5 w-5">
                <span
                  className={`absolute left-0 block h-[2px] w-full rounded bg-current transition-all duration-300 ${
                    open ? 'top-1.5 rotate-45' : 'top-0'
                  }`}
                />
                <span
                  className={`absolute left-0 top-1.5 block h-[2px] w-full rounded bg-current transition-all duration-200 ${
                    open ? 'opacity-0' : 'opacity-100'
                  }`}
                />
                <span
                  className={`absolute left-0 block h-[2px] w-full rounded bg-current transition-all duration-300 ${
                    open ? 'top-1.5 -rotate-45' : 'top-3'
                  }`}
                />
              </span>
            </button>
          </div>
        </div>

        {/* Mobile drawer */}
        <div
          id="mobile-menu"
          className={`overflow-hidden border-t border-line/70 bg-paper transition-[max-height] duration-400 ease-out lg:hidden ${
            open ? 'max-h-[26rem]' : 'max-h-0'
          }`}
        >
          <nav className="shell flex flex-col py-4" aria-label="Mobile">
            {nav.map((item, i) => (
              <a
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="flex items-baseline gap-4 border-b border-line/60 py-4 text-2xl font-bold tracking-tight text-ink-900 last:border-0 hover:text-brand"
              >
                <span className="text-[0.65rem] font-bold tracking-widest text-muted">
                  0{i + 1}
                </span>
                {item.label}
              </a>
            ))}
            <a
              href="#contact"
              onClick={() => setOpen(false)}
              className="mt-5 rounded-full bg-brand px-6 py-4 text-center text-sm font-bold text-white sm:hidden"
            >
              Start a project
            </a>
          </nav>
        </div>
      </header>
    </>
  )
}
