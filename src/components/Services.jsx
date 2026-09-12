import { Reveal, ArrowIcon } from './ui'
import { services } from '../data/site'

export default function Services() {
  return (
    <section id="services" className="scroll-mt-24 py-20 md:py-32">
      <div className="shell">
        <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl">
            <Reveal>
              <span className="eyebrow">Services</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-ink-900">
                What we do, and what you get out of it.
              </h2>
            </Reveal>
          </div>
          <Reveal delay={160}>
            <p className="max-w-sm text-sm leading-relaxed text-ink md:text-right">
              Four practices, one team. Most engagements combine two of them — design and build,
              or build and maintain.
            </p>
          </Reveal>
        </div>

        <div className="mt-14 grid gap-px overflow-hidden rounded-3xl border border-line bg-line md:mt-20 md:grid-cols-2">
          {services.map((service, i) => (
            <Reveal key={service.number} delay={(i % 2) * 90}>
              <article className="group relative h-full bg-white p-8 transition-colors duration-300 hover:bg-paper-2 md:p-10 lg:p-12">
                <div className="flex items-start justify-between gap-6">
                  <span className="text-[0.7rem] font-bold tracking-[0.24em] text-muted">
                    {service.number}
                  </span>
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-line text-ink transition-all duration-300 group-hover:border-brand group-hover:bg-brand group-hover:text-white">
                    <ArrowIcon className="h-4 w-4" />
                  </span>
                </div>

                <h3 className="mt-8 text-2xl font-extrabold tracking-tight text-ink-900 md:text-[1.75rem]">
                  {service.title}
                </h3>
                <p className="mt-4 max-w-md text-[0.95rem] leading-relaxed text-ink">
                  {service.description}
                </p>

                <ul className="mt-8 flex flex-wrap gap-2">
                  {service.points.map((point) => (
                    <li
                      key={point}
                      className="rounded-full bg-brand-soft px-3.5 py-1.5 text-[0.72rem] font-semibold text-brand-dark"
                    >
                      {point}
                    </li>
                  ))}
                </ul>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
