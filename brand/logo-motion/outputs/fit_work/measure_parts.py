"""Measure each semantic part on the unmixed coverage maps (from measure.py).

Sub-pixel edges = 0.5 crossings of coverage, sampled with bilinear interpolation.
Writes measurements.json for fit_logo.py.
"""
import json
import math
from collections import deque
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
blue = np.load(HERE / 'blue_cov.npy').astype(float)
gray = np.load(HERE / 'gray_cov.npy').astype(float)
H, W = blue.shape


def label(mask):
    lab = np.zeros(mask.shape, int); n = 0; sizes = {}
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0]:
            continue
        n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; c = 0
        while q:
            y, x = q.popleft(); c += 1
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and mask[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = n; q.append((yy, xx))
        sizes[n] = c
    return lab, sorted(sizes.items(), key=lambda kv: -kv[1])


def bilinear(img, x, y):
    x0 = np.clip(np.floor(x).astype(int), 0, W - 2); y0 = np.clip(np.floor(y).astype(int), 0, H - 2)
    fx = x - x0; fy = y - y0
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def crossings(vals, ts, level=0.5):
    out = []
    for i in range(1, len(vals)):
        a, b = vals[i - 1] - level, vals[i] - level
        if a == 0:
            continue
        if a * b < 0:
            out.append(ts[i - 1] + (ts[i] - ts[i - 1]) * a / (a - b))
    return out


def fit_circle(pts):
    pts = np.asarray(pts); x, y = pts[:, 0], pts[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    sol, *_ = np.linalg.lstsq(A, x * x + y * y, rcond=None)
    cx, cy = sol[0], sol[1]; r = math.sqrt(sol[2] + cx * cx + cy * cy)
    res = np.hypot(x - cx, y - cy) - r
    return cx, cy, r, float(np.sqrt((res ** 2).mean())), float(np.abs(res).max())


out = {}
blab, bcomp = label(blue > 0.5)
print('blue components (size):', bcomp[:4])
arc_id, deck_id = bcomp[0][0], bcomp[1][0]
arc_cov = np.where(blab == arc_id, blue, 0.0)
# dilate the component mask by 2px so AA edge pixels below 0.5 stay with their part
def grow(lab_mask, r=2):
    m = lab_mask.copy()
    for _ in range(r):
        m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m
arc_cov = np.where(grow(blab == arc_id), blue, 0.0)
deck_cov = np.where(grow(blab == deck_id), blue, 0.0)

# ---- Arc: ray profiles from an iteratively refined center
cx, cy = 511.0, 470.0
for it in range(4):
    inner, outer, angs = [], [], []
    for deg in np.arange(0, 360, 0.5):
        th = math.radians(deg)
        rs = np.arange(200, 400, 0.1)
        xs, ys = cx + rs * math.cos(th), cy + rs * math.sin(th)
        ok = (xs > 1) & (xs < W - 2) & (ys > 1) & (ys < H - 2)
        if ok.sum() < len(rs):
            continue
        v = bilinear(arc_cov, xs, ys)
        cr = crossings(v, rs)
        if len(cr) == 2 and v.max() > 0.9:
            inner.append((cx + cr[0] * math.cos(th), cy + cr[0] * math.sin(th)))
            outer.append((cx + cr[1] * math.cos(th), cy + cr[1] * math.sin(th)))
            angs.append(deg)
    ci = fit_circle(inner); co = fit_circle(outer)
    cx, cy = (ci[0] + co[0]) / 2, (ci[1] + co[1]) / 2
    print(f'iter {it}: inner c=({ci[0]:.2f},{ci[1]:.2f}) r={ci[2]:.2f} rms={ci[3]:.2f} max={ci[4]:.2f} | '
          f'outer c=({co[0]:.2f},{co[1]:.2f}) r={co[2]:.2f} rms={co[3]:.2f} max={co[4]:.2f}')
angs = np.array(angs)
# angular extent: the gap is at the bottom (around 90deg in screen coords)
gap = [a for a in np.arange(0, 360, 0.5) if a not in set(angs)]
print('arc covered angles: n', len(angs), 'gap range', min(gap), max(gap))
out['arc'] = {'inner': ci[:3], 'outer': co[:3], 'center': [cx, cy],
              'r_mid': (ci[2] + co[2]) / 2, 'width': co[2] - ci[2]}

# Arc end cuts: for each end, sample the end face — find where coverage along the arc centerline drops
rmid = (ci[2] + co[2]) / 2; wdt = co[2] - ci[2]
for side, rng in (('right_end', np.arange(0, 40, 0.02)), ('left_end', np.arange(180, 140, -0.02))):
    vals = []
    for deg in rng:
        th = math.radians(deg)
        vals.append(bilinear(arc_cov, np.array([cx + rmid * math.cos(th)]), np.array([cy + rmid * math.sin(th)]))[0])
    vals = np.array(vals); cr = crossings(vals, rng)
    end_mid = cr[0]
    # check cut orientation: end angle on inner vs outer radius
    ends = {}
    for rr, nm in ((ci[2] + 2.5, 'inner'), (co[2] - 2.5, 'outer')):
        v2 = []
        for deg in rng:
            th = math.radians(deg)
            v2.append(bilinear(arc_cov, np.array([cx + rr * math.cos(th)]), np.array([cy + rr * math.sin(th)]))[0])
        ends[nm] = crossings(np.array(v2), rng)[0]
    print(f'{side}: centerline end angle {end_mid:.2f}deg; inner {ends["inner"]:.2f}, outer {ends["outer"]:.2f}')
    out['arc'][side] = {'mid': end_mid, **ends}

# ---- Deck: per-column top / bottom edges
cols = []
for x in np.arange(150, 875, 1.0):
    ys = np.arange(560, 720, 0.05)
    v = bilinear(deck_cov, np.full_like(ys, x), ys)
    cr = crossings(v, ys)
    if len(cr) >= 2:
        cols.append((x, cr[0], cr[-1]))
cols = np.array(cols)
print('deck columns', len(cols), 'x range', cols[0, 0], cols[-1, 0])
i_top = cols[:, 1].argmin()
print('deck top-edge apex', cols[i_top, :2], 'bottom-edge apex', cols[cols[:, 2].argmin(), [0, 2]])
print('deck thickness at apex', cols[i_top, 2] - cols[i_top, 1])
# tips: extrapolate where thickness -> 0 using the horizontal profile at the ends
for side, xs_ in (('left', np.arange(165, 200, 0.02)), ('right', np.arange(860, 820, -0.02))):
    best = None
    for yy in np.arange(680, 700, 0.1):
        v = bilinear(deck_cov, xs_, np.full_like(xs_, yy))
        cr = crossings(v, xs_)
        if cr:
            x_edge = cr[0]
            if best is None or (side == 'left' and x_edge < best[0]) or (side == 'right' and x_edge > best[0]):
                best = (x_edge, yy)
    print(f'deck {side} tip ~', best)
    out.setdefault('deck', {})[f'{side}_tip'] = best
out['deck']['columns'] = cols.tolist()

# ---- Gray: per-row runs (left half), and mirrored right half
glab, gcomp = label(gray > 0.5)
print('gray components (size):', gcomp[:5])
bridge_cov = np.where(grow(glab == gcomp[0][0]), gray, 0.0)
rows = {}
for y in np.arange(250, 700, 1.0):
    xs = np.arange(150, 875, 0.05)
    v = bilinear(bridge_cov, xs, np.full_like(xs, y))
    rows[float(y)] = crossings(v, xs)
out['gray_rows'] = rows
for y in (256, 260, 270, 280, 290, 300, 320, 340, 360, 370, 375, 380, 400, 430, 460, 500, 540, 570, 590, 600, 610, 630, 640):
    print(f'y={y}: ' + ' '.join(f'{c:.1f}' for c in rows[float(y)]))
if __name__ == '__main__':  # importers reuse the data without clobbering later passes
    (HERE / 'measurements.json').write_text(json.dumps(out))
