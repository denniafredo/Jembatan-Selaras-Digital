"""Pixel2Motion Phase 2 — fit minimal, motion-ready geometry for the Jembatan Selaras Digital mark.

Every part is a primitive or a few-cubic path fitted to sub-pixel edge measurements
(measure.py -> measure_parts.py -> measure_detail.py -> measure_arc.py), symmetric about
the measured axis (x = 512 in SVG user space) of the 1024 x 1024 source.

    python fit_logo.py            # fit, write geometry.json + logo SVGs, print residuals

Outputs
    geometry.json            fitted parameters + path data (single source of truth)
    logo_srcframe.svg        QA copy in the source pixel frame (viewBox 0 0 1024 1024)
    ../../logo.svg           deliverable: same geometry, tight viewBox, motion structure
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
M = json.loads((HERE / 'measurements.json').read_text())
AXIS = 511.5
# The measurement scripts sample pixel values at integer coordinates, but in SVG user space a
# pixel's centre sits at +0.5. Fit in the measurement frame, shift once on output.
SHIFT = 0.5
BLUE, GRAY = '#0E93D3', '#51626F'


def mirror_x(x):
    return 2 * AXIS - x


def fmt(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def sv(p):
    """Measurement frame -> SVG user space."""
    return (p[0] + SHIFT, p[1] + SHIFT)


def pt(p):
    q = sv(p)
    return f'{fmt(q[0])} {fmt(q[1])}'


def cubic(P, t):
    t = np.asarray(t)[:, None]
    P = [np.asarray(p, float) for p in P]
    return ((1 - t) ** 3) * P[0] + 3 * ((1 - t) ** 2) * t * P[1] + 3 * (1 - t) * t * t * P[2] + (t ** 3) * P[3]


def lm(fun, x0, iters=200, lam=1e-2):
    """Tiny Levenberg-Marquardt with numeric Jacobian (numpy only)."""
    x = np.array(x0, float)
    r = fun(x); cost = r @ r
    for _ in range(iters):
        J = np.empty((len(r), len(x)))
        for j in range(len(x)):
            h = 1e-5 * max(1.0, abs(x[j]))
            xh = x.copy(); xh[j] += h
            J[:, j] = (fun(xh) - r) / h
        A = J.T @ J; g = J.T @ r
        while True:
            step = np.linalg.solve(A + lam * np.diag(np.diag(A) + 1e-9), -g)
            xn = x + step; rn = fun(xn); cn = rn @ rn
            if cn < cost:
                x, r, cost = xn, rn, cn; lam = max(lam / 3, 1e-9); break
            lam *= 4
            if lam > 1e9:
                return x, r
        if np.abs(step).max() < 1e-7:
            break
    return x, r


# ---------------------------------------------------------------- arc (ring)
af = M['arc_fit']
IN_R, IN_CY = af['inner']['circle']            # inner edge: circle (ellipse gave no gain)
OUT_RX, OUT_RY, OUT_CY = af['outer']['ellipse']  # outer edge: axis-aligned ellipse
fl, fr = M['arc_faces']['left'], M['arc_faces']['right']
FACE_ANG = math.radians((fl['angle_deg'] - fr['angle_deg']) / 2)       # mirrored average
FACE_PT = ((fl['point'][0] + mirror_x(fr['point'][0])) / 2, (fl['point'][1] + fr['point'][1]) / 2)


def line_circle(p, d, cx, cy, r):
    # p + s d on circle -> pick the root nearest p
    fx, fy = p[0] - cx, p[1] - cy
    b = 2 * (fx * d[0] + fy * d[1]); c = fx * fx + fy * fy - r * r
    disc = math.sqrt(b * b - 4 * c)
    s = min(((-b - disc) / 2, (-b + disc) / 2), key=abs)
    return (p[0] + s * d[0], p[1] + s * d[1])


def line_ellipse(p, d, cx, cy, rx, ry):
    q = (p[0] - cx, (p[1] - cy) * rx / ry); e = (d[0], d[1] * rx / ry)
    n = math.hypot(*e); e = (e[0] / n, e[1] / n)
    x, y = line_circle(q, e, 0, 0, rx)
    return (x + cx, y * ry / rx + cy)


face_dir = (math.cos(FACE_ANG), -math.sin(FACE_ANG))  # left face, pointing up-right (toward the ring's inside)
ARC_IN_L = line_circle(FACE_PT, face_dir, AXIS, IN_CY, IN_R)
ARC_OUT_L = line_ellipse(FACE_PT, face_dir, AXIS, OUT_CY, OUT_RX, OUT_RY)
ARC_IN_R = (mirror_x(ARC_IN_L[0]), ARC_IN_L[1])
ARC_OUT_R = (mirror_x(ARC_OUT_L[0]), ARC_OUT_L[1])
ARC_D = (f'M{pt(ARC_OUT_L)}A{fmt(OUT_RX)} {fmt(OUT_RY)} 0 1 1 {pt(ARC_OUT_R)}'
         f'L{pt(ARC_IN_R)}A{fmt(IN_R)} {fmt(IN_R)} 0 1 0 {pt(ARC_IN_L)}Z')

# ---------------------------------------------------------------- deck (crescent, 4 cubics)
cols = np.array(M['deck']['columns'])          # x, top, bottom (0.5-coverage crossings)
xl = np.arange(182.0, AXIS + 0.1, 1.0)
top = (np.interp(xl, cols[:, 0], cols[:, 1]) + np.interp(mirror_x(xl), cols[:, 0], cols[:, 1])) / 2
bot = (np.interp(xl, cols[:, 0], cols[:, 2]) + np.interp(mirror_x(xl), cols[:, 0], cols[:, 2])) / 2
keep = (bot - top) >= 1.0
xl, top, bot = xl[keep], top[keep], bot[keep]
TS = np.linspace(0, 1, 2001)


def deck_curves(p):
    yt, h1, h2, at, yb, k1, k2, ab, xT, yT = p
    h1, h2, k1, k2 = (abs(v) for v in (h1, h2, k1, k2))
    T = (xT, yT)
    top_c = [(AXIS, yt), (AXIS - h1, yt), (xT + h2 * math.cos(at), yT - h2 * math.sin(at)), T]
    bot_c = [(AXIS, yb), (AXIS - k1, yb), (xT + k2 * math.cos(ab), yT - k2 * math.sin(ab)), T]
    return top_c, bot_c


def y_at(curve, xs):
    s = cubic(curve, TS); order = np.argsort(s[:, 0])
    return np.interp(xs, s[order, 0], s[order, 1])


DECK_TIP = (176.5, 690.4)  # 0.25-coverage extent of the thin tip (columns x=176-182, both sides)


def deck_res(p):
    tc, bc = deck_curves(p)
    return np.r_[y_at(tc, xl) - top, y_at(bc, xl) - bot, 3 * (p[8] - DECK_TIP[0]), 3 * (p[9] - DECK_TIP[1])]


deck_p, deck_r = lm(deck_res, [593.8, 150, 120, math.radians(35), 633.7, 160, 120, math.radians(22), 176.5, 690.4])
deck_r = deck_r[:-2]
DECK_TOP, DECK_BOT = deck_curves(deck_p)


def mirror_curve(c):
    return [(mirror_x(x), y) for x, y in c]


dtR, dbR = mirror_curve(DECK_TOP), mirror_curve(DECK_BOT)
# outline: left tip -> top edge to apex -> right tip -> bottom edge back to apex -> left tip
DECK_D = (f'M{pt(DECK_TOP[3])}C{pt(DECK_TOP[2])} {pt(DECK_TOP[1])} {pt(DECK_TOP[0])}'
          f'C{pt(dtR[1])} {pt(dtR[2])} {pt(dtR[3])}'
          f'C{pt(dbR[2])} {pt(dbR[1])} {pt(dbR[0])}'
          f'C{pt(DECK_BOT[1])} {pt(DECK_BOT[2])} {pt(DECK_BOT[3])}Z')

# ---------------------------------------------------------------- tower (legs + crossbars)
LEG_OUT, LEG_IN = 441.3, 460.5                  # leg edges below the cable notch (rows 430-590)
LEG_TOP = 254.0                                 # columns x=451 / 572: 254.03 / 254.06
LEG_TOP_OUT, LEG_TOP_IN = 443.5, 458.6          # pinnacle is narrower: rows 256-280 taper
DECK_HIDE = 615.0                               # legs / hangers run into the deck (hidden)
CROSSBARS = [(285.64, 307.76), (385.90, 410.08), (491.30, 515.45)]  # columns x=470/511.5/552

leg_left = [(LEG_TOP_OUT, LEG_TOP), (LEG_TOP_IN, LEG_TOP), (LEG_IN, CROSSBARS[0][0]),
            (LEG_IN, DECK_HIDE), (LEG_OUT, DECK_HIDE), (LEG_OUT, 380.0)]


def poly_d(points):
    return 'M' + 'L'.join(pt(p) for p in points) + 'Z'


LEG_L_D = poly_d(leg_left)
LEG_R_D = poly_d([(mirror_x(x), y) for x, y in leg_left])

# ---------------------------------------------------------------- cables (tapered, 2 cubics each)
rows = {float(k): v for k, v in M['gray_rows'].items()}
HANGERS = [  # (left x0, x1) symmetric averages of measured runs; widths 11.0 / 9.8 / 9.5
    (407.5, 418.5), (367.75, 377.55), (328.05, 337.55)]
outer_pts, inner_pts = [], []
for y in np.arange(256.0, 646.0, 1.0):
    cr = rows.get(float(y), [])
    # each side on its own: near the tips a row can hold one cable but not the other
    left = [c for c in cr if c < AXIS]
    right = sorted((mirror_x(c) for c in cr if c > AXIS))  # mirrored into the left frame
    sides = [s for s in (left, right) if s]  # crossbar rows cross the axis: odd counts are fine
    if not sides:
        continue
    outs = [s[0] for s in sides]
    if len(outs) == 2 and abs(outs[0] - outs[1]) > 2.5:
        continue  # sides disagree: something else is crossing this row
    outer_pts.append((y, sum(outs) / len(outs)))
    if y >= 382:
        cand = []
        for s in (s for s in sides if len(s) >= 2):
            xi, x0 = s[1], s[0]
            near_hanger = any(abs(xi - h[1]) < 1.6 or abs(xi - h[0]) < 1.6 for h in HANGERS)
            if xi - x0 < 32 and not near_hanger and xi < LEG_OUT - 0.5:
                cand.append(xi)
        if len(cand) == 2 and abs(cand[0] - cand[1]) < 2.5:
            inner_pts.append((y, sum(cand) / 2))
        elif len(cand) == 1:
            inner_pts.append((y, cand[0]))
outer_pts = np.array(outer_pts); inner_pts = np.array(inner_pts)


def x_at(curve, ys):
    s = cubic(curve, TS); order = np.argsort(s[:, 1])
    return np.interp(ys, s[order, 1], s[order, 0])


def cable_curves(p):
    # outer edge: two cubics, G1 at the knee K; inner edge: one cubic from the notch N to the tip T
    xs, u1, kx, ky, ka, kl1, kl2, u2, ao, xT, yT, yN, ai1, v1, v2, ai2 = p
    u1, kl1, kl2, u2, v1, v2 = (abs(v) for v in (u1, kl1, kl2, u2, v1, v2))  # handles point inward
    S = (xs, LEG_TOP); T = (xT, yT); K = (kx, ky)
    kd = (-math.cos(ka), math.sin(ka))  # knee tangent, heading down-left
    o1 = [S, (xs, LEG_TOP + u1), (kx - kl1 * kd[0], ky - kl1 * kd[1]), K]
    o2 = [K, (kx + kl2 * kd[0], ky + kl2 * kd[1]), (xT + u2 * math.cos(ao), yT - u2 * math.sin(ao)), T]
    N = (LEG_OUT, yN)
    inn = [N, (LEG_OUT - v1 * math.cos(ai1), yN + v1 * math.sin(ai1)),
           (xT + v2 * math.cos(ai2), yT - v2 * math.sin(ai2)), T]
    return o1, o2, inn


CABLE_TIP = (196.5, 645.3)  # last dark pixels of the tip (rows 644-645)


def cable_res(p):
    o1, o2, inn = cable_curves(p)
    ky = p[3]
    yo = outer_pts[:, 0]
    xo = np.where(yo <= ky, x_at(o1, yo), x_at(o2, yo))
    xi = x_at(inn, inner_pts[:, 0])
    # monotonic-descent penalty: an edge that travels upward anywhere is not a cable
    climb = [np.clip(-np.diff(cubic(c, TS)[:, 1]), 0, None).sum() for c in (o1, o2, inn)]
    tip = [3 * (p[9] - CABLE_TIP[0]), 3 * (p[10] - CABLE_TIP[1])]
    return np.r_[xo - outer_pts[:, 1], xi - inner_pts[:, 1], tip, 50 * np.array(climb)]


cab_p, cab_r = lm(cable_res, [443.5, 40, 420.0, 395.0, math.radians(68), 30, 60, 60, math.radians(36),
                              197.0, 645.5, 376.5, math.radians(60), 40, 60, math.radians(33)])
CAB_O1, CAB_O2, CAB_IN = cable_curves(cab_p)
cab_r = cab_r[:-5]  # report edge residuals only (drop tip + penalty terms)
_no = len(outer_pts)
for lo, hi in ((256, 300), (300, 380), (380, 460), (460, 540), (540, 600), (600, 646)):
    so = (outer_pts[:, 0] >= lo) & (outer_pts[:, 0] < hi); si = (inner_pts[:, 0] >= lo) & (inner_pts[:, 0] < hi)
    ro = cab_r[:_no][so]; ri = cab_r[_no:][si]
    print(f'  cable y{lo}-{hi}: outer max {np.abs(ro).max() if len(ro) else 0:.2f} mean {ro.mean() if len(ro) else 0:+.2f}'
          f' | inner max {np.abs(ri).max() if len(ri) else 0:.2f} mean {ri.mean() if len(ri) else 0:+.2f}')
print('cable params', np.round(cab_p, 3).tolist())
# close the cable through the inside of the leg (hidden): N -> up the leg's inner region -> S
CAB_HIDDEN = [(LEG_OUT + 6, 330.0), (LEG_TOP_OUT + 4, LEG_TOP + 6)]


def cable_d(o1, o2, inn, hidden):
    return (f'M{pt(o1[0])}C{pt(o1[1])} {pt(o1[2])} {pt(o1[3])}'
            f'C{pt(o2[1])} {pt(o2[2])} {pt(o2[3])}'
            f'C{pt(inn[2])} {pt(inn[1])} {pt(inn[0])}'
            + ''.join(f'L{pt(h)}' for h in hidden) + 'Z')


CAB_L_D = cable_d(CAB_O1, CAB_O2, CAB_IN, CAB_HIDDEN)
CAB_R_D = cable_d(mirror_curve(CAB_O1), mirror_curve(CAB_O2), mirror_curve(CAB_IN),
                  [(mirror_x(x), y) for x, y in CAB_HIDDEN])

# ---------------------------------------------------------------- hangers
# top = inside the cable band (between its outer edge at the hanger's outer side and
# its inner edge at the hanger's inner side); bottom = hidden under the deck
HANGER_TOPS = [433.0, 505.0, 552.0]
HANGER_BOTTOMS = [612.0, 618.0, 626.0]


def rect(x0, y0, x1, y1):
    return {'x': x0 + SHIFT, 'y': y0 + SHIFT, 'width': x1 - x0, 'height': y1 - y0}


hangers_left = [rect(h[0], t, h[1], b) for h, t, b in zip(HANGERS, HANGER_TOPS, HANGER_BOTTOMS)]
hangers_right = [rect(mirror_x(h[1]), t, mirror_x(h[0]), b) for h, t, b in zip(HANGERS, HANGER_TOPS, HANGER_BOTTOMS)]
crossbar_rects = [rect(LEG_IN - 4, a, mirror_x(LEG_IN - 4), b) for a, b in CROSSBARS]

# ---------------------------------------------------------------- report + write
print(f'arc: inner circle r={IN_R:.2f} cy={IN_CY:.2f}; outer ellipse rx={OUT_RX:.2f} ry={OUT_RY:.2f} cy={OUT_CY:.2f}')
print(f'arc face {math.degrees(FACE_ANG):.2f} deg through {FACE_PT[0]:.2f},{FACE_PT[1]:.2f}; '
      f'corners in {pt(ARC_IN_L)} out {pt(ARC_OUT_L)}')
print(f'deck: rms {np.sqrt((deck_r ** 2).mean()):.3f} max {np.abs(deck_r).max():.3f}  tip {pt(DECK_TOP[3])}')
print(f'cable: rms {np.sqrt((cab_r ** 2).mean()):.3f} max {np.abs(cab_r).max():.3f}  tip {pt(CAB_O2[3])} '
      f'notch y {cab_p[11]:.2f} knee {pt(CAB_O1[3])}  n_outer={len(outer_pts)} n_inner={len(inner_pts)}')

geometry = {  # everything below is in SVG user space (source pixel grid, pixel centres at +0.5)
    'axis': AXIS + SHIFT, 'colors': {'blue': BLUE, 'gray': GRAY},
    'arc': {'d': ARC_D, 'inner': [AXIS + SHIFT, IN_CY + SHIFT, IN_R],
            'outer': [AXIS + SHIFT, OUT_CY + SHIFT, OUT_RX, OUT_RY],
            'face_deg': math.degrees(FACE_ANG),
            'corners': [sv(c) for c in (ARC_OUT_L, ARC_IN_L, ARC_IN_R, ARC_OUT_R)]},
    'deck': {'d': DECK_D, 'top': [sv(c) for c in DECK_TOP], 'bottom': [sv(c) for c in DECK_BOT]},
    'legs': [LEG_L_D, LEG_R_D], 'leg_left_points': [sv(c) for c in leg_left],
    'crossbars': crossbar_rects,
    'cables': {'left': CAB_L_D, 'right': CAB_R_D,
               'outer': [[sv(c) for c in CAB_O1], [sv(c) for c in CAB_O2]],
               'inner': [sv(c) for c in CAB_IN]},
    'hangers': {'left': hangers_left, 'right': hangers_right},
}
(HERE / 'geometry.json').write_text(json.dumps(geometry, indent=1))


def rect_tag(r, extra=''):
    return f'<rect x="{fmt(r["x"])}" y="{fmt(r["y"])}" width="{fmt(r["width"])}" height="{fmt(r["height"])}"{extra}/>'


def static_svg(view_box, size):
    """Plain static geometry (QA frame): no masks or clips, painted in z-order."""
    g = geometry
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" width="{size}" height="{size}">',
        f'  <g fill="{GRAY}">',
        f'    <path d="{g["legs"][0]}"/>', f'    <path d="{g["legs"][1]}"/>',
        *[f'    {rect_tag(r)}' for r in g['crossbars']],
        f'    <path d="{g["cables"]["left"]}"/>', f'    <path d="{g["cables"]["right"]}"/>',
        *[f'    {rect_tag(r)}' for r in g['hangers']['left'] + g['hangers']['right']],
        '  </g>',
        f'  <path fill="{BLUE}" d="{g["deck"]["d"]}"/>',
        f'  <path fill="{BLUE}" d="{g["arc"]["d"]}"/>',
        '</svg>', ''])


(HERE / 'logo_srcframe.svg').write_text(static_svg('0 0 1024 1024', 1024))
print('wrote geometry.json, logo_srcframe.svg')
