import { Reveal } from './ui'
import { manifesto } from '../data/site'

export default function Manifesto() {
  return (
    <section className="bg-ink-900 py-20 text-white md:py-32">
      <div className="shell">
        <div className="grid gap-12 lg:grid-cols-12 lg:gap-16">
          <div className="lg:col-span-7">
            <Reveal>
              <span className="eyebrow text-brand">{manifesto.eyebrow}</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-white">{manifesto.title}</h2>
            </Reveal>
          </div>

          <div className="space-y-6 lg:col-span-5 lg:pt-4">
            {manifesto.body.map((paragraph, i) => (
              <Reveal key={i} delay={140 + i * 80}>
                <p className="text-base leading-relaxed text-line md:text-[1.0625rem]">
                  {paragraph}
                </p>
              </Reveal>
            ))}
          </div>
        </div>

        <div className="mt-16 grid grid-cols-2 gap-px overflow-hidden rounded-2xl bg-white/12 md:mt-20 lg:grid-cols-4">
          {manifesto.metrics.map((metric, i) => (
            <Reveal key={metric.label} delay={i * 90}>
              <div className="h-full bg-ink-900 px-6 py-8 md:px-8 md:py-10">
                <p className="text-4xl font-extrabold tracking-tight text-brand md:text-5xl">
                  {metric.value}
                </p>
                <p className="mt-3 text-sm leading-snug text-muted">{metric.label}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
