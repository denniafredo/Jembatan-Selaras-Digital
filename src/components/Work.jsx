import { useMemo, useState } from 'react'
import { Reveal, ArrowIcon } from './ui'
import { projects } from '../data/site'

/**
 * Abstract interface mock used in place of a screenshot.
 * Swap this for a real <img loading="lazy" /> once project imagery is available.
 */
function ProjectVisual({ index }) {
  const palettes = [
    { bg: '#0E93D3', bar: 'rgba(255,255,255,0.9)', dim: 'rgba(255,255,255,0.35)' },
    { bg: '#2C3A44', bar: 'rgba(255,255,255,0.85)', dim: 'rgba(255,255,255,0.28)' },
    { bg: '#98B0BE', bar: 'rgba(255,255,255,0.95)', dim: 'rgba(255,255,255,0.45)' },
    { bg: '#6A7A87', bar: 'rgba(255,255,255,0.9)', dim: 'rgba(255,255,255,0.32)' },
  ]
  const p = palettes[index % palettes.length]
  const bars = [0.72, 0.45, 0.9, 0.58, 0.35, 0.8]

  return (
    <svg
      viewBox="0 0 480 300"
      className="h-full w-full transition-transform duration-700 ease-out group-hover:scale-[1.04]"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <rect width="480" height="300" fill={p.bg} />

      {/* window chrome */}
      <rect x="40" y="42" width="400" height="216" rx="14" fill="rgba(255,255,255,0.12)" />
      <rect x="40" y="42" width="400" height="30" rx="14" fill="rgba(255,255,255,0.16)" />
      <g fill={p.dim}>
        <circle cx="62" cy="57" r="4.5" />
        <circle cx="78" cy="57" r="4.5" />
        <circle cx="94" cy="57" r="4.5" />
      </g>

      {/* sidebar */}
      <rect x="56" y="88" width="74" height="154" rx="8" fill="rgba(255,255,255,0.14)" />
      <g fill={p.dim}>
        {[0, 1, 2, 3].map((i) => (
          <rect key={i} x="68" y={104 + i * 22} width="50" height="7" rx="3.5" />
        ))}
      </g>

      {/* content */}
      <rect x="146" y="88" width="130" height="11" rx="5.5" fill={p.bar} />
      <rect x="146" y="108" width="86" height="8" rx="4" fill={p.dim} />

      {/* chart */}
      <g>
        {bars.map((h, i) => (
          <rect
            key={i}
            x={146 + i * 44}
            y={242 - h * 100}
            width="26"
            height={h * 100}
            rx="5"
            fill={i % 2 === 0 ? p.bar : p.dim}
          />
        ))}
      </g>
      <line x1="146" y1="242" x2="424" y2="242" stroke={p.dim} strokeWidth="2" />
    </svg>
  )
}

export default function Work() {
  const categories = useMemo(
    () => ['All Work', ...new Set(projects.map((p) => p.category))],
    [],
  )
  const [active, setActive] = useState('All Work')

  const visible =
    active === 'All Work' ? projects : projects.filter((p) => p.category === active)

  return (
    <section id="work" className="scroll-mt-24 py-20 md:py-32">
      <div className="shell">
        <div className="flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl">
            <Reveal>
              <span className="eyebrow">Selected work</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-ink-900">
                Projects we can talk about.
              </h2>
            </Reveal>
          </div>

          <Reveal delay={160}>
            <div className="flex flex-wrap gap-2" role="tablist" aria-label="Filter projects">
              {categories.map((category) => (
                <button
                  key={category}
                  type="button"
                  role="tab"
                  aria-selected={active === category}
                  onClick={() => setActive(category)}
                  className={`rounded-full border px-4 py-2 text-[0.78rem] font-bold transition-all duration-200 ${
                    active === category
                      ? 'border-brand bg-brand text-white'
                      : 'border-line bg-white text-ink hover:border-brand hover:text-brand'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </Reveal>
        </div>

        <div className="mt-14 grid gap-6 md:mt-20 md:grid-cols-2 md:gap-8">
          {visible.map((project, i) => (
            <Reveal key={project.title} delay={(i % 2) * 90}>
              <article className="group h-full overflow-hidden rounded-3xl border border-line bg-white transition-shadow duration-300 hover:shadow-xl hover:shadow-ink-900/5">
                <div className="relative aspect-[16/10] overflow-hidden">
                  <ProjectVisual index={i} />
                  <span className="absolute left-5 top-5 rounded-full bg-white/95 px-3.5 py-1.5 text-[0.68rem] font-bold uppercase tracking-[0.14em] text-ink-900">
                    {project.category}
                  </span>
                </div>

                <div className="p-7 md:p-8">
                  <div className="flex items-start justify-between gap-5">
                    <h3 className="text-xl font-extrabold tracking-tight text-ink-900 md:text-2xl">
                      {project.title}
                    </h3>
                    <span className="mt-1 shrink-0 text-xs font-bold tracking-widest text-muted">
                      {project.year}
                    </span>
                  </div>

                  <p className="mt-3.5 text-[0.95rem] leading-relaxed text-ink">
                    {project.summary}
                  </p>

                  <p className="mt-5 inline-flex items-center gap-2 rounded-full bg-brand-soft px-4 py-2 text-[0.78rem] font-bold text-brand-dark">
                    <span className="h-1.5 w-1.5 rounded-full bg-brand" />
                    {project.result}
                  </p>

                  <div className="mt-6 flex items-center justify-between gap-4 border-t border-line pt-5">
                    <ul className="flex flex-wrap gap-x-3 gap-y-1.5">
                      {project.tags.map((tag) => (
                        <li key={tag} className="text-[0.72rem] font-semibold text-muted">
                          {tag}
                        </li>
                      ))}
                    </ul>
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-line text-ink transition-all duration-300 group-hover:border-brand group-hover:bg-brand group-hover:text-white">
                      <ArrowIcon className="h-3.5 w-3.5" />
                    </span>
                  </div>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
