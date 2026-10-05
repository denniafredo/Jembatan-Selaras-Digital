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
 *   redraw           bump this number to re-draw the arc (hover / focus)
 */
const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

function useLogoMotion(motion, redraw, isBuildEnd) {
  const ref = useRef(null)
  const [state, setState] = useState(() => {
    if (!motion || prefersReducedMotion()) return 'idle'
    return motion === 'inview' ? 'pending' : 'intro'
  })
  const stateRef = useRef(state)
  stateRef.current = state

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

  // Only an idle mark re-draws: never cut into the build.
  useEffect(() => {
    if (redraw && stateRef.current === 'idle' && !prefersReducedMotion()) setState('redraw')
  }, [redraw])

  const onAnimationEnd = (e) => {
    if (isBuildEnd(e) || e.animationName === 'jsd-arc-redraw') setState('idle')
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

export function LogoMark({ className = 'h-10 w-10', mono = false, motion, redraw = 0 }) {
  const id = useId().replace(/:/g, '')
  const { ref, state, onAnimationEnd } = useLogoMotion(motion, redraw, markBuildEnd)
  const { gray, blue } = colors(mono)

  return (
    <svg
      ref={ref}
      viewBox={VIEW_BOX}
      className={`jsd-mark ${className}`}
      data-motion={state}
      onAnimationEnd={onAnimationEnd}
      role="img"
      aria-label="Jembatan Selaras Digital"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <MarkDefs id={id} />
      </defs>
      <MarkParts id={id} gray={gray} blue={blue} />
    </svg>
  )
}

// The wordmark finishes last: the final DIGITAL letter ends the build.
const lockupBuildEnd = (e) => e.animationName === 'jsd-letter' && 'last' in e.target.dataset

/**
 * Stacked lockup: mark above JEMBATAN SELARAS / DIGITAL (Montserrat outlines, no font request).
 * The build adds the wordmark after the mark: line 1 is written left to right, then each
 * DIGITAL letter rises out of its baseline.
 */
export function LogoLockup({ className = 'w-64', mono = false, motion, redraw = 0 }) {
  const id = useId().replace(/:/g, '')
  const { ref, state, onAnimationEnd } = useLogoMotion(motion, redraw, lockupBuildEnd)
  const { gray, blue } = colors(mono)

  return (
    <svg
      ref={ref}
      viewBox={LOCKUP_VIEW_BOX}
      className={`jsd-mark jsd-lockup ${className}`}
      data-motion={state}
      onAnimationEnd={onAnimationEnd}
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

/**
 * Mark + wordmark. Hovering (or keyboard-focusing) the lockup re-draws the arc.
 * Pass `href` to render it as a link; `intro` builds the mark once on mount.
 */
export function Logo({ className = '', compact = false, mono = false, intro = false, href, ...rest }) {
  const [redraw, setRedraw] = useState(0)
  const replay = () => setRedraw((n) => n + 1)
  const Tag = href ? 'a' : 'span'

  return (
    <Tag
      href={href}
      className={`inline-flex items-center gap-2.5 ${className}`}
      onPointerEnter={replay}
      onFocus={(e) => e.currentTarget.matches(':focus-visible') && replay()}
      {...rest}
    >
      <LogoMark
        className={compact ? 'h-9 w-9' : 'h-11 w-11'}
        mono={mono}
        motion={intro ? 'intro' : undefined}
        redraw={redraw}
      />
      <span className="flex flex-col leading-none">
        <span
          className={`font-extrabold tracking-tight ${
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
          Digital
        </span>
      </span>
    </Tag>
  )
}
