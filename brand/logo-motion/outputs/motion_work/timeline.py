"""Derive the choreography's keyframe percentages (single 1000 ms clock) from pen geometry.

Hangers drop the moment the cable pen passes their top: invert the cable draw easing
(--p2m-ease-settle) at each hanger's arc-length fraction along the pen.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = json.loads((HERE.parent / 'fit_work' / 'motion_timing.json').read_text())

EASE_ENTER = (0.0, 0.0, 0.2, 1.0)    # --p2m-ease-enter  (Trustworthy/Professional preset)
EASE_SETTLE = (0.4, 0.0, 0.2, 1.0)   # --p2m-ease-settle


def bezier(p1, p2, s):
    return 3 * (1 - s) ** 2 * s * p1 + 3 * (1 - s) * s * s * p2 + s ** 3


def time_for_progress(ease, y):
    """t such that cubic-bezier(ease)(t) == y (bisection on the monotonic progress curve)."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        s = (lo + hi) / 2
        lo, hi = (s, hi) if bezier(ease[1], ease[3], s) < y else (lo, s)
    return bezier(ease[0], ease[2], (lo + hi) / 2)


CABLE = (42.0, 74.0)          # % of the clock (starts once the tower is < 1 unit from home)
HANGER_DROP = 15.0            # each hanger: 150 ms, ease-enter
tl = {'duration_ms': 1000,
      'deck': (6.0, 30.0), 'tower': (14.0, 44.0), 'cable': CABLE, 'arc': (48.0, 100.0), 'hangers': []}
for i, frac in enumerate(T['hanger_pass_fraction'], 1):
    tau = time_for_progress(EASE_SETTLE, frac)
    start = CABLE[0] + (CABLE[1] - CABLE[0]) * tau
    tl['hangers'].append((round(start, 1), round(start + HANGER_DROP, 1)))
    print(f'hanger {i}: pen passes at {frac:.3f} of its length -> t={tau:.3f} of the draw -> '
          f'{start:.1f}% ({start * 10:.0f} ms), drop until {start + HANGER_DROP:.1f}%')
(HERE / 'timeline.json').write_text(json.dumps(tl, indent=1))
print(json.dumps(tl))
