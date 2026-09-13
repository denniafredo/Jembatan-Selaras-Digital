import { Reveal, Button, Marquee } from './ui'
import { LogoMark } from './Logo'
import { hero, marqueeWords, company } from '../data/site'

/**
 * Decorative bridge span — echoes the logo mark, drawn as SVG so it costs nothing to load.
 * The cable is three quadratic curves (side span, main sag, side span) and the suspender
 * drops are sampled off those same curves so everything lines up exactly.
 */
const DECK_Y = 292

const CABLE = [
  { p0: [0, 288], p1: [140, 252], p2: [256, 78] },
  { p0: [256, 78], p1: [456, 298], p2: [656, 78] },
  { p0: [656, 78], p1: [772, 252], p2: [900, 288] },
]

const quad = (a, b, c, t) => (1 - t) ** 2 * a + 2 * (1 - t) * t * b + t ** 2 * c

function Tower({ x }) {
  return (
    <g fill="#6A7A87">
      <rect x={x - 20} y="78" width="9" height={DECK_Y - 78} />
      <rect x={x + 11} y="78" width="9" height={DECK_Y - 78} />
      <rect x={x - 20} y="78" width="40" height="9" rx="2" />
      <rect x={x - 20} y="148" width="40" height="8" rx="2" />
      <rect x={x - 20} y="214" width="40" height="8" rx="2" />
    </g>
  )
}

function BridgeArt() {
  const suspenders = CABLE.flatMap((segment, s) =>
    Array.from({ length: s === 1 ? 18 : 8 }, (_, i) => {
      const t = (i + 0.5) / (s === 1 ? 18 : 8)
      const x = quad(segment.p0[0], segment.p1[0], segment.p2[0], t)
      const y = quad(segment.p0[1], segment.p1[1], segment.p2[1], t)
      return DECK_Y - y > 10 ? { key: `${s}-${i}`, x, y } : null
    }).filter(Boolean),
  )

  return (
    <svg
      viewBox="0 0 900 360"
      className="h-full w-full"
      preserveAspectRatio="xMidYMax slice"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="jsd-water" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#0E93D3" stopOpacity="0.18" />
          <stop offset="100%" stopColor="#0E93D3" stopOpacity="0" />
        </linearGradient>
      </defs>

      <rect x="0" y={DECK_Y} width="900" height={360 - DECK_Y} fill="url(#jsd-water)" />

      {/* Suspenders */}
      <g stroke="#CDD9E0" strokeWidth="1.5">
        {suspenders.map((drop) => (
          <line key={drop.key} x1={drop.x} y1={drop.y} x2={drop.x} y2={DECK_Y} />
        ))}
      </g>

      {/* Main cable */}
      <path
        d={CABLE.map(
          (c, i) =>
            `${i === 0 ? `M${c.p0[0]} ${c.p0[1]}` : ''} Q${c.p1[0]} ${c.p1[1]} ${c.p2[0]} ${c.p2[1]}`,
        ).join('')}
        stroke="#98B0BE"
        strokeWidth="3.5"
        fill="none"
        strokeLinecap="round"
      />

      {/* Deck */}
      <line x1="0" y1={DECK_Y} x2="900" y2={DECK_Y} stroke="#6A7A87" strokeWidth="3" />

      <Tower x={256} />
      <Tower x={656} />
    </svg>
  )
}

/** Paints `accent` in the brand colour inside `line`; renders the line as-is if absent. */
function accentuate(line, accent) {
  if (!accent || !line.includes(accent)) return line
  const [before, ...rest] = line.split(accent)
  return (
    <>
      {before}
      <span className="text-brand">{accent}</span>
      {rest.join(accent)}
    </>
  )
}

export default function Hero() {
  return (
    <section id="top" className="relative overflow-hidden pt-[104px] md:pt-32">
      {/* Soft brand glow behind the headline */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -top-40 left-1/2 h-[36rem] w-[52rem] -translate-x-1/2 rounded-full bg-brand/8 blur-3xl"
      />

      <div className="shell relative">
        <Reveal>
          <span className="eyebrow">{hero.eyebrow}</span>
        </Reveal>

        <h1 className="mt-6 max-w-6xl text-display font-extrabold text-ink-900">
          {hero.headline.map((line, i) => (
            <Reveal key={line} as="span" delay={i * 90} className="block">
              {i === hero.headline.length - 1 ? accentuate(line, hero.headlineAccent) : line}
            </Reveal>
          ))}
        </h1>

        <div className="mt-10 flex flex-col gap-10 border-t border-line pt-8 md:flex-row md:items-end md:justify-between">
          <Reveal delay={120} className="max-w-xl">
            <p className="text-base leading-relaxed text-ink md:text-lg">{hero.intro}</p>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Button href={hero.ctaPrimary.href}>{hero.ctaPrimary.label}</Button>
              <Button href={hero.ctaSecondary.href} variant="outline">
                {hero.ctaSecondary.label}
              </Button>
            </div>
          </Reveal>

          <Reveal delay={220} className="shrink-0">
            <div className="flex flex-wrap gap-2">
              {hero.badges.map((badge) => (
                <span
                  key={badge}
                  className="rounded-full border border-line bg-white px-4 py-2 text-[0.7rem] font-bold uppercase tracking-[0.12em] text-ink"
                >
                  {badge}
                </span>
              ))}
            </div>
            <p className="mt-5 text-sm text-muted md:text-right">
              Building digital products since {company.founded}
            </p>
          </Reveal>
        </div>
      </div>

      {/* Bridge panel */}
      <Reveal delay={160} className="shell mt-14">
        <div className="relative h-[215px] overflow-hidden rounded-[28px] border border-line bg-gradient-to-b from-paper-2 to-white sm:h-[320px] md:h-[400px]">
          <BridgeArt />

          <div className="absolute inset-0 flex items-center justify-center">
            <div className="flex flex-col items-center rounded-2xl border border-line/80 bg-white/80 px-6 py-5 backdrop-blur-md md:rounded-3xl md:px-8 md:py-7">
              <LogoMark className="h-11 w-11 md:h-16 md:w-16" />
              <p className="mt-2.5 text-center text-[0.6rem] font-bold uppercase tracking-[0.24em] text-muted md:mt-3 md:text-[0.68rem] md:tracking-[0.28em]">
                {company.tagline}
              </p>
            </div>
          </div>
        </div>
      </Reveal>

      {/* Keyword ticker */}
      <div className="mt-16 border-y border-line bg-paper-2 py-5 md:mt-24">
        <Marquee duration={38}>
          {marqueeWords.map((word) => (
            <span key={word} className="flex items-center gap-8 px-8">
              <span className="whitespace-nowrap text-sm font-bold uppercase tracking-[0.18em] text-ink-900">
                {word}
              </span>
              <span className="h-1.5 w-1.5 rounded-full bg-brand" />
            </span>
          ))}
        </Marquee>
      </div>
    </section>
  )
}
