"""Pixel2Motion lockup: verified mark (uniform scale) + Montserrat wordmark outlines, motion-ready.

    python build_lockup.py <Montserrat variable TTF>

Inputs  ../../outputs/fit_work/geometry.json, motion_timing.json   verified mark + pens
        mark_transform.json      similarity fit of the mark onto source_lockup.png (measure_mark.py)
        wordmark_glyphs.json     per-letter boxes from the source (segment_wordmark.py)
Outputs ../logo_lockup.svg       deliverable: tight viewBox, one element per letter
        lockup_srcframe.svg      static copy in the source frame (overlay QA)
        wordmark.json            glyph paths for the site generator
Typography: Montserrat wght 630 (font-match winner, ink ratio ~1.0), HarfBuzz kerning,
tracking fitted per word on line 1 (the source sets JEMBATAN tighter than SELARAS) and per line on line 2.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
MARK = HERE.parents[1] / 'outputs' / 'fit_work'
G = json.loads((MARK / 'geometry.json').read_text())
T = json.loads((MARK / 'motion_timing.json').read_text())
TR = json.loads((HERE / 'mark_transform.json').read_text())
SRC = json.loads((HERE / 'wordmark_glyphs.json').read_text())
WGHT = 630
BLUE, GRAY = G['colors']['blue'], G['colors']['gray']


def fmt(v):
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return '0' if s == '-0' else s


tt = instantiateVariableFont(TTFont(sys.argv[1]), {'wght': WGHT})
buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
gs = tt.getGlyphSet(); cap = tt['OS/2'].sCapHeight
hbfont = hb.Font(hb.Face(data))


def shape(text):
    b = hb.Buffer(); b.add_str(text); b.guess_segment_properties(); hb.shape(hbfont, b, {'kern': True})
    out, x = [], 0.0
    for info, pos in zip(b.glyph_infos, b.glyph_positions):
        name = tt.getGlyphName(info.codepoint); bp = BoundsPen(gs); gs[name].draw(bp)
        out.append({'name': name, 'x': x, 'bounds': bp.bounds}); x += pos.x_advance
    return out


def layout(key, text, words):
    """Fit x0 + tracking per word (index ranges into the shaped run) to the source letter centres."""
    m = SRC[key + '_metrics']; s = m['cap_height'] / cap; base = m['baseline']
    glyphs = shape(text); ink = [i for i, g in enumerate(glyphs) if g['bounds']]
    src_c = {i: (g['x0'] + g['x1'] + 1) / 2 for i, g in zip(ink, SRC[key])}
    placed, res_all = [], []
    for lo, hi in words:
        idx = [i for i in ink if lo <= i < hi]
        mc = np.array([s * (glyphs[i]['x'] + (glyphs[i]['bounds'][0] + glyphs[i]['bounds'][2]) / 2) for i in idx])
        A = np.c_[np.ones(len(idx)), np.array(idx, float)]
        (x0, tr), *_ = np.linalg.lstsq(A, np.array([src_c[i] for i in idx]) - mc, rcond=None)
        for i, c in zip(idx, mc):
            res_all.append(src_c[i] - (c + x0 + tr * i))
            placed.append((i, glyphs[i]['name'], x0 + tr * i + s * glyphs[i]['x']))
    letters = []
    for i, name, dx in sorted(placed):
        pen = SVGPathPen(gs, ntos=fmt)
        gs[name].draw(TransformPen(pen, (s, 0, 0, -s, dx, base)))
        b = glyphs[i]['bounds']
        letters.append({'char': text[i], 'd': pen.getCommands(),
                        'bbox': [dx + s * b[0], base - s * b[3], dx + s * b[2], base - s * b[1]]})
    print(f'{key}: {len(letters)} letters, centre residual max {np.abs(res_all).max():.2f} px')
    return letters


line1 = layout('line1', 'JEMBATAN SELARAS', [(0, 8), (9, 16)])
line2 = layout('line2', 'DIGITAL', [(0, 7)])
(HERE / 'wordmark.json').write_text(json.dumps({'font': f'Montserrat wght {WGHT}', 'line1': line1, 'line2': line2}, indent=1))

# ---------------------------------------------------------------- lockup frame
s, tx, ty = TR['scale'], TR['tx'], TR['ty']
mark_box = [177.6 * s + tx, 166.1 * s + ty, 846.4 * s + tx, 694.5 * s + ty]
xs = [mark_box[0], mark_box[2]] + [v for L in (line1, line2) for g in L for v in (g['bbox'][0], g['bbox'][2])]
ys = [mark_box[1], mark_box[3]] + [v for L in (line1, line2) for g in L for v in (g['bbox'][1], g['bbox'][3])]
pad = 6
vb = [min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad]
VIEWBOX = ' '.join(fmt(v) for v in vb)
MARK_TRANSFORM = f'translate({fmt(tx)} {fmt(ty)}) scale({s:.5f})'
print('lockup viewBox', VIEWBOX, 'aspect', round(vb[2] / vb[3], 4), '| mark', MARK_TRANSFORM)


def mark_body(motion: bool, indent='    '):
    """The verified mark, drawn in its own (source-1) units under MARK_TRANSFORM."""
    rect = lambda r, extra='': (f'<rect x="{fmt(r["x"])}" y="{fmt(r["y"])}" width="{fmt(r["width"])}" '
                                f'height="{fmt(r["height"])}"{extra}/>')
    hang = G['hangers']['left'] + G['hangers']['right']
    i2 = indent + '  '
    lines = [f'{indent}<g transform="{MARK_TRANSFORM}">', f'{i2}<g fill="{GRAY}">']
    if motion:
        lines += [f'{i2}  <g clip-path="url(#lk-rise)"><g id="lk-tower" class="jsd-tower">']
    lines += [f'{i2}    <path d="{d}"/>' for d in G['legs']] + [f'{i2}    {rect(r)}' for r in G['crossbars']]
    if motion:
        lines += [f'{i2}  </g></g>']
    for side, d in (('l', G['cables']['left']), ('r', G['cables']['right'])):
        lines.append(f'{i2}  <path d="{d}"' + (f' mask="url(#lk-cable-{side})"' if motion else '') + '/>')
    for i, r in enumerate(hang):
        lines.append(f'{i2}  ' + rect(r, f' class="jsd-hanger jsd-hanger-{i % 3 + 1}"' if motion else ''))
    lines += [f'{i2}</g>', f'{i2}<path' + (' class="jsd-deck"' if motion else '') + f' fill="{BLUE}" d="{G["deck"]["d"]}"/>',
              f'{i2}<path fill="{BLUE}" d="{G["arc"]["d"]}"' + (' mask="url(#lk-arc)"' if motion else '') + '/>',
              f'{indent}</g>']
    return lines


def defs():
    pen = lambda cls, d, w: (f'<path class="{cls}" d="{d}" fill="none" stroke="#fff" stroke-width="{w}" '
                             f'pathLength="1" stroke-dasharray="1 1"/>')
    m = lambda mid, *ps: [f'    <mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">'] + \
        [f'      {p}' for p in ps] + ['    </mask>']
    P = T['pens']
    return (['  <defs>', f'    <clipPath id="lk-rise"><path d="{T["rise_clip"]}"/></clipPath>']
            + m('lk-cable-l', pen('jsd-cable-pen', P['cable_l'], P['cable_width']))
            + m('lk-cable-r', pen('jsd-cable-pen', P['cable_r'], P['cable_width']))
            + m('lk-arc', pen('jsd-arc-pen', P['arc_l'], P['arc_width']), pen('jsd-arc-pen', P['arc_r'], P['arc_width']))
            + ['  </defs>'])


def wordmark(motion: bool):
    out = [f'  <g id="wordmark" fill="{GRAY}">', '    <g id="wordmark-line1" class="jsd-word-1">']
    out += [f'      <path id="w1-{i}" d="{g["d"]}"/>' for i, g in enumerate(line1)]
    out += ['    </g>', '    <g id="wordmark-line2" class="jsd-word-2">']
    out += [f'      <path id="w2-{i}"' + (f' class="jsd-letter" style="--i:{i}"' if motion else '') + f' d="{g["d"]}"/>'
            for i, g in enumerate(line2)]
    return out + ['    </g>', '  </g>']


svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="' + VIEWBOX + f'" width="{fmt(vb[2])}" height="{fmt(vb[3])}" '
       'class="jsd-mark jsd-lockup" data-motion="intro" role="img" aria-label="Jembatan Selaras Digital">',
       '  <title>Jembatan Selaras Digital</title>', *defs(), *mark_body(True, '  '), *wordmark(True), '</svg>', '']
(HERE.parent / 'logo_lockup.svg').write_text('\n'.join(svg), encoding='utf-8')
qa = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">',
      *mark_body(False, '  '), *wordmark(False), '</svg>', '']
(HERE / 'lockup_srcframe.svg').write_text('\n'.join(qa), encoding='utf-8')
(HERE / 'lockup_frame.json').write_text(json.dumps({'viewBox': VIEWBOX, 'mark_transform': MARK_TRANSFORM}, indent=1))
print('wrote logo_lockup.svg, lockup_srcframe.svg, wordmark.json')
