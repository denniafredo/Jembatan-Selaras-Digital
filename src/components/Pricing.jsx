import { Reveal, ArrowIcon, CheckIcon } from './ui'
import { pricing } from '../data/site'

export default function Pricing() {
  return (
    <section id="pricing" className="scroll-mt-24 bg-paper-2 py-20 md:py-32">
      <div className="shell">
        <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl">
            <Reveal>
              <span className="eyebrow">{pricing.eyebrow}</span>
            </Reveal>
            <Reveal delay={80}>
              <h2 className="mt-6 text-title font-extrabold text-ink-900">{pricing.title}</h2>
            </Reveal>
          </div>
          <Reveal delay={160}>
            <p className="max-w-sm text-sm leading-relaxed text-ink md:text-right">
              {pricing.body}
            </p>
          </Reveal>
        </div>

        {/* Plans */}
        <div className="mt-14 grid gap-px overflow-hidden rounded-3xl border border-line bg-line md:mt-20 lg:grid-cols-3">
          {pricing.plans.map((plan, i) => (
            <Reveal key={plan.name} delay={i * 90} className="h-full">
              <article
                className={`flex h-full flex-col p-8 md:p-10 ${
                  plan.featured ? 'bg-ink-900 text-white' : 'bg-white'
                }`}
              >
                <div className="flex items-center justify-between gap-4">
                  <h3
                    className={`text-xl font-extrabold tracking-tight ${
                      plan.featured ? 'text-white' : 'text-ink-900'
                    }`}
                  >
                    {plan.name}
                  </h3>
                  {plan.featured && (
                    <span className="rounded-full bg-brand px-3 py-1 text-[0.62rem] font-bold uppercase tracking-[0.16em] text-white">
                      Most chosen
                    </span>
                  )}
                </div>

                <p
                  className={`mt-6 text-[2rem] font-extrabold leading-none tracking-tight ${
                    plan.featured ? 'text-white' : 'text-ink-900'
                  }`}
                >
                  {plan.price}
                </p>
                <p
                  className={`mt-2.5 text-[0.72rem] font-bold uppercase tracking-[0.16em] ${
                    plan.featured ? 'text-brand' : 'text-muted'
                  }`}
                >
                  {plan.timeline}
                </p>

                <p
                  className={`mt-6 text-[0.95rem] leading-relaxed ${
                    plan.featured ? 'text-white/70' : 'text-ink'
                  }`}
                >
                  {plan.summary}
                </p>

                <ul
                  className={`mt-8 mb-10 space-y-3.5 border-t pt-8 ${
                    plan.featured ? 'border-white/15' : 'border-line'
                  }`}
                >
                  {plan.includes.map((item) => (
                    <li key={item} className="flex gap-3">
                      <CheckIcon className="mt-0.5 h-4 w-4 shrink-0 text-brand" />
                      <span
                        className={`text-[0.88rem] leading-relaxed ${
                          plan.featured ? 'text-white/80' : 'text-ink'
                        }`}
                      >
                        {item}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* mt-auto keeps every call to action on the same baseline,
                    however uneven the feature lists are. */}
                <a
                  href="#contact"
                  className={`group mt-auto inline-flex items-center justify-center gap-2.5 rounded-full px-6 py-3.5 text-sm font-bold transition-all duration-300 ${
                    plan.featured
                      ? 'bg-brand text-white hover:bg-brand-dark'
                      : 'border border-line text-ink-900 hover:border-brand hover:bg-brand hover:text-white'
                  }`}
                >
                  {plan.cta}
                  <ArrowIcon className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                </a>
              </article>
            </Reveal>
          ))}
        </div>

        {/* Retainer and one-off work that sits outside a build */}
        <div className="mt-px grid gap-px overflow-hidden rounded-3xl border border-line bg-line md:mt-6 md:grid-cols-2">
          {pricing.addons.map((addon, i) => (
            <Reveal key={addon.name} delay={i * 80}>
              <div className="flex h-full flex-col gap-4 bg-white p-8 sm:flex-row sm:items-center sm:justify-between md:p-10">
                <div className="max-w-sm">
                  <h3 className="text-lg font-extrabold tracking-tight text-ink-900">
                    {addon.name}
                  </h3>
                  <p className="mt-2 text-[0.88rem] leading-relaxed text-ink">{addon.text}</p>
                </div>
                <p className="shrink-0 text-right">
                  <span className="text-xl font-extrabold tracking-tight text-ink-900">
                    {addon.price}
                  </span>
                  <span className="ml-1.5 text-[0.72rem] font-bold uppercase tracking-[0.14em] text-muted">
                    {addon.unit}
                  </span>
                </p>
              </div>
            </Reveal>
          ))}
        </div>

        {/* The small print that otherwise arrives as four emails */}
        <Reveal delay={120}>
          <ul className="mt-10 grid gap-x-10 gap-y-3 md:grid-cols-2">
            {pricing.terms.map((term) => (
              <li key={term} className="flex gap-3 text-[0.82rem] leading-relaxed text-ink">
                <span className="mt-[0.55rem] h-1 w-1 shrink-0 rounded-full bg-muted" />
                {term}
              </li>
            ))}
          </ul>
        </Reveal>
      </div>
    </section>
  )
}
