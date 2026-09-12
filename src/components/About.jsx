import { Reveal, CountUp } from './ui'
import { LogoMark } from './Logo'
import { about, stats } from '../data/site'

export default function About() {
  return (
    <section id="about" className="scroll-mt-24 border-y border-line bg-paper-2 py-20 md:py-32">
      <div className="shell">
        <div className="grid gap-12 lg:grid-cols-12 lg:gap-20">
          {/* Visual side */}
          <Reveal className="lg:col-span-5">
            <div className="relative overflow-hidden rounded-3xl border border-line bg-white p-10 md:p-14">
              <div
                aria-hidden="true"
                className="pointer-events-none absolute -right-16 -top-16 h-56 w-56 rounded-full bg-brand/8 blur-2xl"
              />
              <LogoMark className="relative h-24 w-24 md:h-28 md:w-28" />

              <p className="relative mt-10 text-xl font-bold leading-snug tracking-tight text-ink-900 md:text-2xl">
                “Jembatan” means bridge. “Selaras” means in harmony. That is the whole brief.
              </p>

              <dl className="relative mt-10 space-y-5 border-t border-line pt-8">
                {about.principles.map((principle) => (
                  <div key={principle.title}>
                    <dt className="text-sm font-extrabold tracking-tight text-brand">
                      {principle.title}
                    </dt>
                    <dd className="mt-1.5 text-sm leading-relaxed text-ink">{principle.text}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </Reveal>

          {/* Copy side */}
          <div className="lg:col-span-7">
            <Reveal>
              <span className="eyebrow">{about.eyebrow}</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-ink-900">{about.title}</h2>
            </Reveal>

            <div className="mt-8 max-w-2xl space-y-6">
              {about.body.map((paragraph, i) => (
                <Reveal key={i} delay={140 + i * 80}>
                  <p className="text-base leading-relaxed text-ink md:text-[1.0625rem]">
                    {paragraph}
                  </p>
                </Reveal>
              ))}
            </div>

            <div className="mt-12 grid grid-cols-2 gap-8 border-t border-line pt-10 md:gap-10">
              {stats.map((stat, i) => (
                <Reveal key={stat.label} delay={i * 80}>
                  <p className="text-4xl font-extrabold tracking-tight text-ink-900 md:text-5xl">
                    <CountUp value={stat.value} suffix={stat.suffix} />
                  </p>
                  <p className="mt-2 text-sm leading-snug text-ink">{stat.label}</p>
                </Reveal>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
