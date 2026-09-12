import { useEffect, useState } from 'react'
import { Reveal, Marquee } from './ui'
import { testimonials, clients } from '../data/site'

function QuoteIcon() {
  return (
    <svg viewBox="0 0 48 36" className="h-8 w-10 text-brand" fill="currentColor" aria-hidden="true">
      <path d="M0 36V20.5C0 9.2 6.6 1.6 18.2 0l1.8 5.6C13.4 7.6 9.8 11.6 9.6 17.4H18V36H0Zm28 0V20.5C28 9.2 34.6 1.6 46.2 0L48 5.6c-6.6 2-10.2 6-10.4 11.8H46V36H28Z" />
    </svg>
  )
}

function Chevron({ direction = 'left' }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-4 w-4"
      aria-hidden="true"
    >
      <path d={direction === 'left' ? 'M15 18 9 12l6-6' : 'M9 18l6-6-6-6'} />
    </svg>
  )
}

export default function Testimonials() {
  const [index, setIndex] = useState(0)
  const [paused, setPaused] = useState(false)
  const total = testimonials.length

  const go = (next) => setIndex((next + total) % total)

  useEffect(() => {
    if (paused) return
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduced) return

    const timer = setInterval(() => setIndex((i) => (i + 1) % total), 7000)
    return () => clearInterval(timer)
  }, [paused, total])

  return (
    <section
      id="clients"
      className="scroll-mt-24 border-y border-line bg-paper-2 py-20 md:py-32"
    >
      <div className="shell">
        <div className="grid gap-12 lg:grid-cols-12 lg:gap-16">
          <div className="lg:col-span-4">
            <Reveal>
              <span className="eyebrow">Clients</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-ink-900">
                What it is like to work with us.
              </h2>
            </Reveal>
            <Reveal delay={160}>
              <div className="mt-8 flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => go(index - 1)}
                  aria-label="Previous testimonial"
                  className="flex h-11 w-11 items-center justify-center rounded-full border border-line bg-white text-ink-900 transition-colors hover:border-brand hover:bg-brand hover:text-white"
                >
                  <Chevron direction="left" />
                </button>
                <button
                  type="button"
                  onClick={() => go(index + 1)}
                  aria-label="Next testimonial"
                  className="flex h-11 w-11 items-center justify-center rounded-full border border-line bg-white text-ink-900 transition-colors hover:border-brand hover:bg-brand hover:text-white"
                >
                  <Chevron direction="right" />
                </button>
                <span className="ml-2 text-sm font-bold tabular-nums text-muted">
                  {String(index + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}
                </span>
              </div>
            </Reveal>
          </div>

          {/* min-w-0 keeps the slider from sizing the grid track to its max-content width */}
          <Reveal delay={120} className="min-w-0 lg:col-span-8">
            <div
              className="w-full overflow-hidden rounded-3xl border border-line bg-white"
              onMouseEnter={() => setPaused(true)}
              onMouseLeave={() => setPaused(false)}
            >
              <div
                className="flex transition-transform duration-700 ease-[cubic-bezier(0.22,1,0.36,1)]"
                style={{ transform: `translate3d(-${index * 100}%, 0, 0)` }}
                aria-live="polite"
              >
                {testimonials.map((item) => (
                  <figure
                    key={item.name}
                    className="w-full shrink-0 p-8 md:p-12 lg:p-14"
                    aria-hidden={testimonials[index].name !== item.name}
                  >
                    <QuoteIcon />
                    <blockquote className="mt-7 text-lg font-semibold leading-snug tracking-tight text-ink-900 md:text-2xl md:leading-[1.35]">
                      {item.quote}
                    </blockquote>
                    <figcaption className="mt-8 flex items-center gap-4 border-t border-line pt-6">
                      <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-brand-soft text-sm font-extrabold text-brand-dark">
                        {item.name
                          .split(' ')
                          .map((n) => n[0])
                          .join('')
                          .slice(0, 2)}
                      </span>
                      <span>
                        <span className="block text-sm font-extrabold text-ink-900">
                          {item.name}
                        </span>
                        <span className="block text-sm text-muted">{item.role}</span>
                      </span>
                    </figcaption>
                  </figure>
                ))}
              </div>
            </div>
          </Reveal>
        </div>
      </div>

      {/* Client roster ticker */}
      <div className="mt-16 border-y border-line bg-white py-6 md:mt-24">
        <Marquee duration={44}>
          {clients.map((client) => (
            <span key={client} className="flex items-center gap-10 px-10">
              <span className="whitespace-nowrap text-lg font-extrabold tracking-tight text-muted md:text-xl">
                {client}
              </span>
            </span>
          ))}
        </Marquee>
      </div>
    </section>
  )
}
