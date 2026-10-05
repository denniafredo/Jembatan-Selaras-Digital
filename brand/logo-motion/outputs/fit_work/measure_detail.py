"""Detail measurements: arc residual pattern, arc end faces, deck symmetry, tower columns."""
import json, math
import numpy as np
from measure_parts import bilinear, crossings, arc_cov, deck_cov, bridge_cov, out, fit_circle

A = out['arc']; (icx, icy, ir), (ocx, ocy, orr) = A['inner'], A['outer']
cx, cy = A['center']

# 1. residual pattern by angle (systematic = ellipse / non-circular)
for name, (ccx, ccy, rr) in (('inner', (icx, icy, ir)), ('outer', (ocx, ocy, orr))):
    res = []
    for deg in list(range(165, 360, 15)) + list(range(0, 20, 5)):
        th = math.radians(deg); rs = np.arange(rr - 12, rr + 12, 0.05)
        v = bilinear(arc_cov, ccx + rs * math.cos(th), ccy + rs * math.sin(th))
        cr = crossings(v, rs)
        if cr:
            res.append((deg, round((cr[0] if name == 'outer' and len(cr) == 1 else (cr[-1] if name == 'outer' else cr[0])) - rr, 2)))
    print(name, 'residual(deg: px):', res)

# 2. end faces: end angle at many radii -> points -> line fit
def end_face(rng):
    pts = []
    for rr in np.arange(ir + 2, orr - 2, 1.0):
        # radius measured from each circle is ambiguous; use the mean center
        vals = bilinear(arc_cov, cx + rr * np.cos(np.radians(rng)), cy + rr * np.sin(np.radians(rng)))
        cr = crossings(vals, rng)
        if cr:
            t = math.radians(cr[0]); pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    pts = np.array(pts)
    # total least squares line
    m = pts.mean(0); u, s, vt = np.linalg.svd(pts - m); d = vt[0]
    ang = math.degrees(math.atan2(d[1], d[0]))
    resid = np.abs((pts - m) @ vt[1])
    return pts, m, d, ang, resid.max()

for side, rng in (('right', np.arange(0, 40, 0.01)), ('left', np.arange(180, 140, -0.01))):
    pts, m, d, ang, rmax = end_face(rng)
    print(f'{side} end face: through ({m[0]:.2f},{m[1]:.2f}) dir angle {ang:.2f}deg, line resid max {rmax:.2f}px; '
          f'first {pts[0].round(2)}, last {pts[-1].round(2)}')
    A[f'{side}_face'] = {'point': m.tolist(), 'dir': d.tolist()}

# 3. deck symmetry about x=511.5: compare top/bottom edges
cols = np.array(out['deck']['columns'])
def edge_at(x, k):
    return np.interp(x, cols[:, 0], cols[:, k])
print('deck edges (x: top, bottom) and mirror diffs about 511.5:')
for dx in (0, 50, 100, 150, 200, 250, 280, 300, 310, 320):
    l, r = 511.5 - dx, 511.5 + dx
    print(f'  d={dx}: L top {edge_at(l,1):.2f} bot {edge_at(l,2):.2f} | R top {edge_at(r,1):.2f} bot {edge_at(r,2):.2f}')

# 4. tower columns: crossings along vertical lines
for x in (451.0, 459.0, 470.0, 511.5, 552.0, 572.0):
    ys = np.arange(240, 640, 0.05)
    v = bilinear(bridge_cov, np.full_like(ys, x), ys)
    print(f'col x={x}: ' + ' '.join(f'{c:.2f}' for c in crossings(v, ys)))
# hanger columns
for x in (413.0, 372.7, 333.1, 610.0, 650.4, 690.4):
    ys = np.arange(380, 640, 0.05)
    v = bilinear(bridge_cov, np.full_like(ys, x), ys)
    print(f'hanger col x={x}: ' + ' '.join(f'{c:.2f}' for c in crossings(v, ys)))
# diagnostic only: does not write measurements.json
