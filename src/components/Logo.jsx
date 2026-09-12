/**
 * Jembatan Selaras Digital — vector mark.
 * Blue arc + blue swoosh (Primary Blue) with a gray-blue suspension bridge.
 * Rendered as SVG so it stays crisp and costs zero image requests.
 */
export function LogoMark({ className = 'h-10 w-10', mono = false }) {
  const blue = mono ? 'currentColor' : 'var(--color-brand)'
  const gray = mono ? 'currentColor' : '#5A6B78'

  return (
    <svg
      viewBox="0 0 512 512"
      className={className}
      role="img"
      aria-label="Jembatan Selaras Digital"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Outer arc */}
      <path
        d="M146 305 A152 152 0 1 1 366 305"
        stroke={blue}
        strokeWidth="15"
        strokeLinecap="round"
      />

      {/* Bridge — main cables */}
      <path
        d="M236 136 C200 210 150 285 92 320"
        stroke={gray}
        strokeWidth="8"
        strokeLinecap="round"
      />
      <path
        d="M276 136 C312 210 362 285 420 320"
        stroke={gray}
        strokeWidth="8"
        strokeLinecap="round"
      />

      {/* Bridge — deck */}
      <path
        d="M92 320 C170 292 342 292 420 320"
        stroke={gray}
        strokeWidth="4"
        strokeLinecap="round"
      />

      {/* Bridge — suspenders */}
      <g stroke={gray} strokeWidth="4" strokeLinecap="round">
        <path d="M200 202 V305" />
        <path d="M172 243 V301" />
        <path d="M142 279 V297" />
        <path d="M312 202 V305" />
        <path d="M340 243 V301" />
        <path d="M370 279 V297" />
      </g>

      {/* Bridge — tower */}
      <g fill={gray}>
        <rect x="231" y="128" width="12" height="175" rx="2" />
        <rect x="269" y="128" width="12" height="175" rx="2" />
        <rect x="231" y="128" width="50" height="11" rx="3" />
        <rect x="231" y="182" width="50" height="10" rx="3" />
        <rect x="231" y="236" width="50" height="10" rx="3" />
      </g>

      {/* Base swoosh */}
      <path
        d="M88 352 C150 288 362 288 424 352 C362 330 150 330 88 352 Z"
        fill={blue}
      />
    </svg>
  )
}

export function Logo({ className = '', compact = false, mono = false }) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <LogoMark className={compact ? 'h-9 w-9' : 'h-11 w-11'} mono={mono} />
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
    </span>
  )
}
