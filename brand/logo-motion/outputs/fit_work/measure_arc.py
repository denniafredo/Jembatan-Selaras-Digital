"""Arc refinement: compare circle vs axis-aligned ellipse for each edge; measure end-face lines."""
import json, math
import numpy as np
from measure_parts import bilinear, crossings, arc_cov

AXIS = 511.5
m = json.load(open('measurements.json'))
cx, cy = m['arc']['center']

# edge points by rays from the provisional center, skipping 8 deg near each end
edges = {'inner': [], 'outer': []}
for deg in np.arange(168, 372, 0.5):
    th = math.radians(deg % 360); rs = np.arange(270, 360, 0.05)
    v = bilinear(arc_cov, cx + rs * math.cos(th), cy + rs * math.sin(th))
    cr = crossings(v, rs)
    if len(cr) == 2:
        edges['inner'].append((cx + cr[0] * math.cos(th), cy + cr[0] * math.sin(th)))
        edges['outer'].append((cx + cr[1] * math.cos(th), cy + cr[1] * math.sin(th)))

def fit_ellipse_axis(pts):
    """x = AXIS fixed; solve ((x-AXIS)/a)^2 + ((y-c)/b)^2 = 1 by Gauss-Newton on geometric-ish residual."""
    p = np.array(pts); X = p[:, 0] - AXIS; Y = p[:, 1]
    # linear init: X^2*A + Y^2*B + Y*C = 1 - ... -> use general conic with no XY, no X terms
    M = np.c_[X * X, Y * Y, Y, np.ones(len(X))]
    _, _, vt = np.linalg.svd(M); A, B, C, D = vt[-1]
    c = -C / (2 * B); k = B * c * c - D
    a = math.sqrt(k / A); b = math.sqrt(k / B)
    for _ in range(50):
        # residual: radial distance along the ray from (AXIS, c)
        ang = np.arctan2(Y - c, X)
        r_pt = np.hypot(X, Y - c)
        r_el = 1 / np.sqrt((np.cos(ang) / a) ** 2 + (np.sin(ang) / b) ** 2)
        res = r_pt - r_el
        J = np.zeros((len(X), 3)); eps = 1e-4
        for j in range(3):
            q = [a, b, c]; q[j] += eps
            ang2 = np.arctan2(Y - q[2], X); r2 = np.hypot(X, Y - q[2])
            re2 = 1 / np.sqrt((np.cos(ang2) / q[0]) ** 2 + (np.sin(ang2) / q[1]) ** 2)
            J[:, j] = ((r2 - re2) - res) / eps
        step, *_ = np.linalg.lstsq(J, -res, rcond=None)
        a, b, c = a + step[0], b + step[1], c + step[2]
    return a, b, c, float(np.sqrt((res ** 2).mean())), float(np.abs(res).max())

def fit_circle_axis(pts):
    p = np.array(pts); X = p[:, 0] - AXIS; Y = p[:, 1]
    A = np.c_[2 * Y, np.ones(len(Y))]
    sol, *_ = np.linalg.lstsq(A, X * X + Y * Y, rcond=None)
    c = sol[0]; r = math.sqrt(sol[1] + c * c)
    res = np.hypot(X, Y - c) - r
    return r, c, float(np.sqrt((res ** 2).mean())), float(np.abs(res).max())

res = {}
for k, pts in edges.items():
    r, c, rms, mx = fit_circle_axis(pts)
    a, b, ce, rms_e, mx_e = fit_ellipse_axis(pts)
    print(f'{k}: circle r={r:.2f} cy={c:.2f} rms={rms:.2f} max={mx:.2f} | ellipse a={a:.2f} b={b:.2f} cy={ce:.2f} rms={rms_e:.2f} max={mx_e:.2f}')
    res[k] = {'circle': [r, c], 'ellipse': [a, b, ce]}

# end faces: march along constant radius near the INNER part of the band only
faces = {}
for side, rng in (('left', np.arange(175, 145, -0.005)), ('right', np.arange(5, 35, 0.005))):
    pts = []
    r_in = res['inner']['circle'][0]
    for rr in np.arange(r_in + 3, r_in + 19, 0.5):
        vals = bilinear(arc_cov, cx + rr * np.cos(np.radians(rng)), cy + rr * np.sin(np.radians(rng)))
        cr = crossings(vals, rng)
        if cr:
            t = math.radians(cr[0]); pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    pts = np.array(pts); mu = pts.mean(0); _, _, vt = np.linalg.svd(pts - mu); d = vt[0]
    if d[0] < 0: d = -d
    resid = np.abs((pts - mu) @ vt[1])
    ang = math.degrees(math.atan2(-d[1], d[0]))  # degrees above horizontal (screen y flipped)
    print(f'{side} face: point ({mu[0]:.2f},{mu[1]:.2f}), {ang:.2f} deg above horizontal (rising to the right if >0), resid max {resid.max():.2f}, n={len(pts)}')
    faces[side] = {'point': mu.tolist(), 'dir': d.tolist(), 'angle_deg': ang}
m['arc_fit'] = res; m['arc_faces'] = faces
json.dump(m, open('measurements.json', 'w'))
