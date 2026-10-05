import { useEffect, useId, useRef, useState } from 'react'
import {
  ARC,
  ARC_PENS,
  ARC_PEN_WIDTH,
  CABLES,
  CABLE_PENS,
  CABLE_PEN_WIDTH,
  CROSSBARS,
  DECK,
  HANGERS,
  LEGS,
  LOCKUP_MARK_TRANSFORM,
  LOCKUP_VIEW_BOX,
  RISE_CLIP,
  VIEW_BOX,
  WORDMARK_LINE_1,
  WORDMARK_LINE_2,
} from './logoGeometry'

/**
 * Jembatan Selaras Digital — vector mark and lockups.
 * Minimal geometry fitted to the master artwork (brand/logo-motion): Primary Blue ring and
 * deck around a gray-blue suspension bridge, one element per part so each can move on its own.
 * Rendered as SVG so it stays crisp and costs zero image requests.
 *
 * Motion lives in index.css (the jsd-* keyframes); components only set data-motion:
 *   motion="intro"   build once on mount
 *   motion="inview"  build once when scrolled into view
 *   loop             while true, play the build over and over (hover / focus)
 */
const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

// How long a looping mark rests, finished, before it builds again.
const LOOP_REST_MS = 800

function useLogoMotion(motion, loop, isBuildEnd) {
  const ref = useRef(null)
  const [state, setState] = useState(() => {
    if (!motion || prefersReducedMotion()) return 'idle'
    return motion === 'inview' ? 'pending' : 'intro'
  })
  const stateRef = useRef(state)
  stateRef.current = state
  const loopRef = useRef(loop)
  loopRef.current = loop

  useEffect(() => {
    if (state !== 'pending') return
    if (!('IntersectionObserver' in window)) {
      setState('intro')
      return
    }

    let timer = 0
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return
        observer.disconnect()
        // Let the surrounding card's own fade-in lead by a beat.
        timer = setTimeout(() => setState('intro'), 200)
      },
      { threshold: 0.6 },
    )
    observer.observe(ref.current)
    return () => {
      observer.disconnect()
      clearTimeout(timer)
    }
  }, [state])

  // Only an idle mark starts a loop: never cut into a build. A build already running just
  // rolls into the loop when it ends.
  useEffect(() => {
    if (loop && stateRef.current === 'idle' && !prefersReducedMotion()) setState('intro')
  }, [loop])

  // Rest on the finished mark, then build again unless the loop was released meanwhile.
  useEffect(() => {
    if (state !== 'rest') return
    const timer = setTimeout(() => setState(loopRef.current ? 'intro' : 'idle'), LOOP_REST_MS)
    return () => clearTimeout(timer)
  }, [state])

  // Releasing the loop mid-build lets that build finish, so the mark never snaps.
  const onAnimationEnd = (e) => {
    if (isBuildEnd(e)) setState(loopRef.current ? 'rest' : 'idle')
  }

  return { ref, state, onAnimationEnd }
}

/** Clip and draw-on pens for one mark instance (ids must be unique per page). */
function MarkDefs({ id }) {
  return (
    <>
      <clipPath id={`${id}-rise`}>
        <path d={RISE_CLIP} />
      </clipPath>
      {CABLE_PENS.map((d, i) => (
        <mask key={d} id={`${id}-cable-${i}`} maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">
          <path
            className="jsd-cable-pen"
            d={d}
            fill="none"
            stroke="#fff"
            strokeWidth={CABLE_PEN_WIDTH}
            pathLength="1"
            strokeDasharray="1 1"
          />
        </mask>
      ))}
      <mask id={`${id}-arc`} maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">
        {ARC_PENS.map((d) => (
          <path
            key={d}
            className="jsd-arc-pen"
            d={d}
            fill="none"
            stroke="#fff"
            strokeWidth={ARC_PEN_WIDTH}
            pathLength="1"
            strokeDasharray="1 1"
          />
        ))}
      </mask>
    </>
  )
}

function MarkParts({ id, gray, blue }) {
  return (
    <>
      <g fill={gray}>
        <g clipPath={`url(#${id}-rise)`}>
          <g className="jsd-tower">
            {LEGS.map((d) => (
              <path key={d} d={d} />
            ))}
            {CROSSBARS.map((r) => (
              <rect key={r.y} x={r.x} y={r.y} width={r.width} height={r.height} />
            ))}
          </g>
        </g>
        {CABLES.map((d, i) => (
          <path key={d} d={d} mask={`url(#${id}-cable-${i})`} />
        ))}
        {HANGERS.map((r) => (
          <rect
            key={r.x}
            className={`jsd-hanger jsd-hanger-${r.step}`}
            x={r.x}
            y={r.y}
            width={r.width}
            height={r.height}
          />
        ))}
      </g>
      <path className="jsd-deck" fill={blue} d={DECK} />
      <path fill={blue} d={ARC} mask={`url(#${id}-arc)`} />
    </>
  )
}

const colors = (mono) => ({
  gray: mono ? 'currentColor' : 'var(--color-logo-gray)',
  blue: mono ? 'currentColor' : 'var(--color-brand)',
})

// Every mark animation shares one clock, so the deck ending means the build is done.
const markBuildEnd = (e) => e.animationName === 'jsd-deck'

/** The bare mark: whoever owns its motion puts .jsd-mark + data-motion on it or an ancestor. */
function MarkSvg({ className, mono, svgRef, ...rest }) {
  const id = useId().replace(/:/g, '')
  const { gray, blue } = colors(mono)

  return (
    <svg
      ref={svgRef}
      viewBox={VIEW_BOX}
      className={className}
      role="img"
      aria-label="Jembatan Selaras Digital"
      xmlns="http://www.w3.org/2000/svg"
      {...rest}
    >
      <defs>
        <MarkDefs id={id} />
      </defs>
      <MarkParts id={id} gray={gray} blue={blue} />
    </svg>
  )
}

export function LogoMark({ className = 'h-10 w-10', mono = false, motion, loop = false }) {
  const { ref, state, onAnimationEnd } = useLogoMotion(motion, loop, markBuildEnd)

  return (
    <MarkSvg
      svgRef={ref}
      className={`jsd-mark ${className}`}
      mono={mono}
      data-motion={state}
      onAnimationEnd={onAnimationEnd}
    />
  )
}

// The wordmark finishes last: the final DIGITAL letter ends the build.
const lockupBuildEnd = (e) => e.animationName === 'jsd-letter' && 'last' in e.target.dataset

/**
 * Stacked lockup: mark above JEMBATAN SELARAS / DIGITAL (Montserrat outlines, no font request).
 * The build adds the wordmark after the mark: line 1 is written left to right, then each
 * DIGITAL letter rises out of its baseline. Hovering it loops the whole build.
 */
export function LogoLockup({ className = 'w-64', mono = false, motion }) {
  const id = useId().replace(/:/g, '')
  const [hovered, setHovered] = useState(false)
  const { ref, state, onAnimationEnd } = useLogoMotion(motion, hovered, lockupBuildEnd)
  const { gray, blue } = colors(mono)

  return (
    <svg
      ref={ref}
      viewBox={LOCKUP_VIEW_BOX}
      className={`jsd-mark jsd-lockup ${className}`}
      data-motion={state}
      onAnimationEnd={onAnimationEnd}
      onPointerEnter={() => setHovered(true)}
      onPointerLeave={() => setHovered(false)}
      role="img"
      aria-label="Jembatan Selaras Digital"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <MarkDefs id={id} />
      </defs>
      <g transform={LOCKUP_MARK_TRANSFORM}>
        <MarkParts id={id} gray={gray} blue={blue} />
      </g>
      <g fill={gray}>
        <g className="jsd-word-1">
          {WORDMARK_LINE_1.map((d) => (
            <path key={d} d={d} />
          ))}
        </g>
        <g>
          {WORDMARK_LINE_2.map((d, i) => (
            <path
              key={d}
              className="jsd-letter"
              style={{ '--i': i }}
              data-last={i === WORDMARK_LINE_2.length - 1 ? '' : undefined}
              d={d}
            />
          ))}
        </g>
      </g>
    </svg>
  )
}

/** One span per letter so each can rise on its own (jsd-letter); screen readers get the word. */
function RisingLetters({ text }) {
  const letters = [...text]

  return (
    <>
      <span aria-hidden="true">
        {letters.map((letter, i) => (
          <span
            key={i}
            className="jsd-letter inline-block"
            style={{ '--i': i }}
            data-last={i === letters.length - 1 ? '' : undefined}
          >
            {letter}
          </span>
        ))}
      </span>
      <span className="sr-only">{text}</span>
    </>
  )
}

/**
 * Mark + wordmark, side by side. The motion state sits on the whole lockup, so with
 * `animateText` the wordmark joins the build exactly as in LogoLockup (line 1 written left to
 * right, then each DIGITAL letter rising); without it only the mark moves.
 * While hovered (or keyboard-focused) the build loops. Pass `href` to render it as a link;
 * `motion` ("intro" / "inview") builds it once.
 */
export function Logo({
  className = '',
  compact = false,
  mono = false,
  motion,
  animateText = false,
  href,
  ...rest
}) {
  const [hovered, setHovered] = useState(false)
  const [focused, setFocused] = useState(false)
  const { ref, state, onAnimationEnd } = useLogoMotion(
    motion,
    hovered || focused,
    animateText ? lockupBuildEnd : markBuildEnd,
  )
  const Tag = href ? 'a' : 'span'

  return (
    <Tag
      ref={ref}
      href={href}
      className={`jsd-mark ${animateText ? 'jsd-lockup ' : ''}inline-flex items-center gap-2.5 ${className}`}
      data-motion={state}
      onAnimationEnd={onAnimationEnd}
      onPointerEnter={() => setHovered(true)}
      onPointerLeave={() => setHovered(false)}
      onFocus={(e) => setFocused(e.currentTarget.matches(':focus-visible'))}
      onBlur={() => setFocused(false)}
      {...rest}
    >
      <MarkSvg className={compact ? 'h-9 w-9' : 'h-11 w-11'} mono={mono} />
      <span className="flex flex-col leading-none">
        <span
          className={`${animateText ? 'jsd-word-1 ' : ''}font-extrabold tracking-tight ${
            mono ? 'text-current' : 'text-ink-900'
          } ${compact ? 'text-[0.94rem]' : 'text-base'}`}
        >
          Jembatan Selaras
        </span>
        <span
          className={`mt-[3px] text-[0.6rem] font-semibold uppercase tracking-[0.34em] ${
            mono ? 'text-current opacity-70' : 'text-muted'
          }`}
        >
          {animateText ? <RisingLetters text="Digital" /> : 'Digital'}
        </span>
      </span>
    </Tag>
  )
}
