"""Is the lockup's mark the same design as the verified mark? Fit a similarity transform.

Unmix the lockup raster (same coverage model as ../../outputs/fit_work/measure.py), measure
the ring's edges by rays, and compare with geometry.json landmarks.
"""
import json, math
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
G = json.loads((HERE.parents[1] / 'outputs' / 'fit_work' / 'geometry.json').read_text())
a = np.asarray(Image.open(HERE.parent / 'source_lockup.png').convert('RGB')).astype(float)
H, W, _ = a.shape
WHITE = np.array([255, 255, 255.]); BLUE = np.array([0, 145, 213.]); GRAY = np.array([76, 97, 115.])
Mx = np.stack([BLUE - WHITE, GRAY - WHITE], axis=1)
d = (a - WHITE).reshape(-1, 3) @ np.linalg.pinv(Mx).T
blue = np.clip(d[:, 0], 0, 1).reshape(H, W); gray = np.clip(d[:, 1], 0, 1).reshape(H, W)
np.save(HERE / 'lockup_blue_cov.npy', blue.astype(np.float32)); np.save(HERE / 'lockup_gray_cov.npy', gray.astype(np.float32))


def bilinear(img, x, y):
    x0 = np.clip(np.floor(x).astype(int), 0, W - 2); y0 = np.clip(np.floor(y).astype(int), 0, H - 2)
    fx, fy = x - x0, y - y0
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def crossings(v, ts, lvl=0.5):
    out = []
    for i in range(1, len(v)):
        p, q = v[i - 1] - lvl, v[i] - lvl
        if p * q < 0:
            out.append(ts[i - 1] + (ts[i] - ts[i - 1]) * p / (p - q))
    return out


ring = blue.copy(); ring[560:] = 0  # deck excluded (ring ends ~y 512 here)
cx, cy = 512.0, 400.0
inner, outer = [], []
for it in range(3):
    inner, outer = [], []
    for deg in np.arange(168, 372, 0.5):
        th = math.radians(deg % 360); rs = np.arange(180, 300, 0.05)
        v = bilinear(ring, cx + rs * math.cos(th), cy + rs * math.sin(th)); cr = crossings(v, rs)
        if len(cr) == 2:
            inner.append((cx + cr[0] * math.cos(th), cy + cr[0] * math.sin(th)))
            outer.append((cx + cr[1] * math.cos(th), cy + cr[1] * math.sin(th)))
    pi, po = np.array(inner), np.array(outer)
    # circle fits for a centre estimate
    def circ(p):
        A = np.c_[2 * p[:, 0], 2 * p[:, 1], np.ones(len(p))]
        s, *_ = np.linalg.lstsq(A, (p ** 2).sum(1), rcond=None)
        return s[0], s[1], math.sqrt(s[2] + s[0] ** 2 + s[1] ** 2)
    ci, co = circ(pi), circ(po); cx, cy = (ci[0] + co[0]) / 2, (ci[1] + co[1]) / 2


def ellipse_axis(p, axis):
    X = p[:, 0] - axis; Y = p[:, 1]
    Mm = np.c_[X * X, Y * Y, Y, np.ones(len(X))]
    _, _, vt = np.linalg.svd(Mm); A_, B_, C_, D_ = vt[-1]
    c = -C_ / (2 * B_); k = B_ * c * c - D_
    return math.sqrt(k / A_), math.sqrt(k / B_), c


axis = (ci[0] + co[0]) / 2
rx_o, ry_o, cy_o = ellipse_axis(po, axis)
r_i = ci[2]
# measurement frame -> SVG user space (+0.5), as in fit_logo.py
axis_s, cy_o_s, cy_i_s = axis + 0.5, cy_o + 0.5, ci[1] + 0.5
ox, ocy, orx, ory = G['arc']['outer']; ix, icy, ir = G['arc']['inner']
s_rx, s_ry, s_ri = rx_o / orx, ry_o / ory, r_i / ir
print(f'lockup ring: axis x {axis_s:.2f}; outer ellipse rx {rx_o:.2f} ry {ry_o:.2f} cy {cy_o_s:.2f}; inner circle r {r_i:.2f} cy {cy_i_s:.2f}')
print(f'scale implied by: outer rx {s_rx:.4f}, outer ry {s_ry:.4f}, inner r {s_ri:.4f}')
s = (s_rx + s_ry + s_ri) / 3
ty_o, ty_i = cy_o_s - s * ocy, cy_i_s - s * icy
tx = axis_s - s * G['axis']
print(f'mean scale {s:.4f}; offset from outer centre ty {ty_o:.2f}, from inner centre ty {ty_i:.2f}; tx {tx:.2f}')
json.dump({'scale': s, 'tx': tx, 'ty': (ty_o + ty_i) / 2, 'axis': axis_s,
           'scales': [s_rx, s_ry, s_ri]}, open(HERE / 'mark_transform.json', 'w'), indent=1)
