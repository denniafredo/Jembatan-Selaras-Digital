"""Pixel2Motion Phase 2 -> 3 bridge: wrap the fitted geometry in motion-ready structure.

Reads geometry.json (fit_logo.py) and writes
    ../../logo.svg              deliverable: tight viewBox, one element per semantic part,
                                draw-on pens (pathLength=1) in masks, rise clip under the deck
    logo_motion_srcframe.svg    the same structure in the 1024 source frame (final-frame QA)
    motion_timing.json          pen geometry facts the choreography is derived from

Part inventory (ids are stable; CSS targets the jsd-* classes):
    #tower        legs + crossbars, rises out of the deck inside #rise-clip
    #cable-l/-r   tapered cables, revealed by #cable-l-pen / #cable-r-pen
    #hanger-l1..3, #hanger-r1..3   drop from the cable (scaleY from the top)
    #deck         crescent, unfurls from the centre (clip-path inset)
    #arc          ring, revealed by #arc-pen-l / #arc-pen-r meeting at the top
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
G = json.loads((HERE / 'geometry.json').read_text())
AX = G['axis']
BLUE, GRAY = G['colors']['blue'], G['colors']['gray']
VIEWBOX = '166 84.5 692 692'  # content bbox x 177-847, y 166-694, centred on the axis


def fmt(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


def P(p):
    return f'{fmt(p[0])} {fmt(p[1])}'


def cubic(Pts, t):
    t = np.asarray(t)[:, None]
    Q = [np.asarray(p, float) for p in Pts]
    return ((1 - t) ** 3) * Q[0] + 3 * ((1 - t) ** 2) * t * Q[1] + 3 * (1 - t) * t * t * Q[2] + (t ** 3) * Q[3]


TS = np.linspace(0, 1, 4001)


def x_at(curve, ys):
    s = cubic(curve, TS); o = np.argsort(s[:, 1])
    return np.interp(ys, s[o, 1], s[o, 0])


# ---------------------------------------------------------------- cable pen (left; right mirrors)
o1, o2 = G['cables']['outer']; inn = G['cables']['inner']
notch_y = inn[0][1]
tip = np.array(o2[3])
ys = np.arange(256.0, tip[1] - 0.5, 1.0)
outer_x = np.where(ys <= o1[3][1], x_at(o1, ys), x_at(o2, ys))
hidden_x = 448.0  # inside the leg, where the cable outline closes (fit_logo CAB_HIDDEN, SVG frame)
inner_x = np.where(ys < notch_y, hidden_x, x_at(inn, np.maximum(ys, notch_y)))
mid = np.c_[(outer_x + inner_x) / 2, ys]
half_w = np.abs(inner_x - outer_x) / 2
# tip direction from the last 12 units of the outer edge, extend the pen 10 units past the tip
d_tip = tip - cubic(o2, [0.97])[0]; d_tip /= np.linalg.norm(d_tip)
start = np.array([mid[0, 0], 246.0])
end = tip + 10 * d_tip


def catmull_rom(points):
    """C1 cubic segments through the given points (uniform Catmull-Rom -> Bezier)."""
    Q = np.vstack([2 * points[0] - points[1], points, 2 * points[-1] - points[-2]])
    return [[Q[i], Q[i] + (Q[i + 1] - Q[i - 1]) / 6, Q[i + 1] - (Q[i + 2] - Q[i]) / 6, Q[i + 1]]
            for i in range(1, len(Q) - 2)]


# knots on the cable midline; spacing tightens where the cable bends (knee ~395)
knot_y = [300, 350, 395, 450, 510, 570, 615]
knots = np.vstack([start] + [mid[np.argmin(np.abs(ys - y))] for y in knot_y] + [tip - 4 * d_tip, end])
PEN_L = catmull_rom(knots)
pen_s = np.vstack([cubic(seg_, TS) for seg_ in PEN_L])
err = max(np.hypot(pen_s[:, 0] - x, pen_s[:, 1] - y).min() for x, y in mid)
# pen half-width needed: distance from pen centreline to the cable edges, plus AA margin
need = 0.0
for x0, y in np.r_[np.c_[outer_x, ys], np.c_[inner_x, ys]]:
    need = max(need, np.hypot(pen_s[:, 0] - x0, pen_s[:, 1] - y).min())
PEN_W = math.ceil(2 * (need + 4))
free = ys >= notch_y  # below the notch the cable is free of the leg: this is where centring shows
dev_free = max(np.hypot(pen_s[:, 0] - x, pen_s[:, 1] - y).min() for x, y in mid[free])
print(f'cable pen: max centre deviation {err:.2f} (free cable {dev_free:.2f}), '
      f'farthest cable edge {need:.2f} -> stroke-width {PEN_W}')


def mirror(p):
    return (2 * AX - p[0], p[1])


PEN_R = [[mirror(p) for p in seg_] for seg_ in PEN_L]
pen_d = lambda segs: f'M{P(segs[0][0])}' + ''.join(f'C{P(s[1])} {P(s[2])} {P(s[3])}' for s in segs)

# arc length fraction along the pen where it passes each hanger top (for the drop stagger)
seg = np.hypot(*np.diff(pen_s, axis=0).T); cum = np.r_[0, np.cumsum(seg)]; L = cum[-1]
hanger_fracs = []
for h in G['hangers']['left']:
    hx = h['x'] + h['width'] / 2
    i = np.argmin(np.abs(pen_s[:, 0] - hx) + np.where(pen_s[:, 1] > h['y'] - 40, 0, 1e6))
    hanger_fracs.append(cum[i] / L)
print('pen length', round(L, 1), 'hanger pass fractions', [round(f, 3) for f in hanger_fracs])

# ---------------------------------------------------------------- arc pens (centre ellipse of the ring)
icx, icy, ir = G['arc']['inner']; ocx, ocy, orx, ory = G['arc']['outer']
ecy, erx, ery = (icy + ocy) / 2, (ir + orx) / 2, (ir + ory) / 2
ARC_W = math.ceil((orx - ir) + 16)     # band is 27-33 wide; pen covers it with AA margin
corners = G['arc']['corners']           # out_L, in_L, in_R, out_R
ang = lambda p: math.degrees(math.atan2(p[1] - ecy, p[0] - AX))
start_ang = min(ang(corners[0]), ang(corners[1])) - 3.0   # 3 deg beyond the face's far corner
OVERLAP = 1.5                                               # halves overlap past the top centre


def ell(deg):
    t = math.radians(deg)
    return (AX + erx * math.cos(t), ecy + ery * math.sin(t))


arc_pen_l = f'M{P(ell(start_ang))}A{fmt(erx)} {fmt(ery)} 0 0 1 {P(ell(270 + OVERLAP))}'
arc_pen_r = f'M{P(ell(180 - start_ang))}A{fmt(erx)} {fmt(ery)} 0 0 0 {P(ell(270 - OVERLAP))}'
arc_half_len = math.radians(270 + OVERLAP - start_ang) * (erx + ery) / 2
print(f'arc pens: centre ellipse cy={ecy:.2f} rx={erx:.2f} ry={ery:.2f}, start {start_ang:.2f} deg, '
      f'stroke-width {ARC_W}, half length ~{arc_half_len:.0f}')

# ---------------------------------------------------------------- rise clip: everything above the deck top edge + 3
top = G['deck']['top']  # left half: apex -> left tip (SVG frame)
tr = [mirror(p) for p in top]
dy = 3.0
sh = lambda p: (p[0], p[1] + dy)
clip_d = (f'M{P(sh(top[3]))}C{P(sh(top[2]))} {P(sh(top[1]))} {P(sh(top[0]))}'
          f'C{P(sh(tr[1]))} {P(sh(tr[2]))} {P(sh(tr[3]))}V0H{fmt(top[3][0])}Z')


# ---------------------------------------------------------------- write SVGs
def rect(r, **attrs):
    extra = ''.join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<rect x="{fmt(r["x"])}" y="{fmt(r["y"])}" width="{fmt(r["width"])}" height="{fmt(r["height"])}"{extra}/>'


def motion_svg(view_box, size):
    hl, hr = G['hangers']['left'], G['hangers']['right']
    def pen(pid, cls, d, w):
        return (f'<path id="{pid}" class="jsd-pen {cls}" d="{d}" fill="none" stroke="#fff" '
                f'stroke-width="{w}" pathLength="1" stroke-dasharray="1 1"/>')

    def mask(mid, *pens):
        return '\n'.join([f'    <mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">']
                         + [f'      {pn}' for pn in pens] + ['    </mask>'])
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" width="{size}" height="{size}" '
        f'class="jsd-mark" data-motion="intro" role="img" aria-label="Jembatan Selaras Digital">',
        '  <title>Jembatan Selaras Digital</title>',
        '  <defs>',
        f'    <clipPath id="rise-clip"><path d="{clip_d}"/></clipPath>',
        mask('cable-l-mask', pen('cable-l-pen', 'jsd-cable-pen', pen_d(PEN_L), PEN_W)),
        mask('cable-r-mask', pen('cable-r-pen', 'jsd-cable-pen', pen_d(PEN_R), PEN_W)),
        mask('arc-mask', pen('arc-pen-l', 'jsd-arc-pen', arc_pen_l, ARC_W),
             pen('arc-pen-r', 'jsd-arc-pen', arc_pen_r, ARC_W)),
        '  </defs>',
        f'  <g id="bridge" fill="{GRAY}">',
        '    <g clip-path="url(#rise-clip)">',
        '      <g id="tower" class="jsd-tower">',
        f'        <path d="{G["legs"][0]}"/>',
        f'        <path d="{G["legs"][1]}"/>',
        *[f'        {rect(r)}' for r in G['crossbars']],
        '      </g>',
        '    </g>',
        f'    <path id="cable-l" class="jsd-cable" d="{G["cables"]["left"]}" mask="url(#cable-l-mask)"/>',
        f'    <path id="cable-r" class="jsd-cable" d="{G["cables"]["right"]}" mask="url(#cable-r-mask)"/>',
        *[f'    {rect(r, id=f"hanger-l{i + 1}", class_=f"jsd-hanger jsd-hanger-{i + 1}")}' for i, r in enumerate(hl)],
        *[f'    {rect(r, id=f"hanger-r{i + 1}", class_=f"jsd-hanger jsd-hanger-{i + 1}")}' for i, r in enumerate(hr)],
        '  </g>',
        f'  <path id="deck" class="jsd-deck" fill="{BLUE}" d="{G["deck"]["d"]}"/>',
        f'  <path id="arc" class="jsd-arc" fill="{BLUE}" d="{G["arc"]["d"]}" mask="url(#arc-mask)"/>',
        '</svg>', ''])


(ROOT / 'logo.svg').write_text(motion_svg(VIEWBOX, 692), encoding='utf-8')
(HERE / 'logo_motion_srcframe.svg').write_text(motion_svg('0 0 1024 1024', 1024), encoding='utf-8')
timing = {'cable_pen_length': L, 'hanger_pass_fraction': hanger_fracs, 'arc_half_length': arc_half_len,
          'pens': {'cable_l': pen_d(PEN_L), 'cable_r': pen_d(PEN_R), 'arc_l': arc_pen_l, 'arc_r': arc_pen_r,
                   'cable_width': PEN_W, 'arc_width': ARC_W},
          'rise_clip': clip_d, 'viewBox': VIEWBOX}
(HERE / 'motion_timing.json').write_text(json.dumps(timing, indent=1))
print('wrote logo.svg, logo_motion_srcframe.svg, motion_timing.json')
