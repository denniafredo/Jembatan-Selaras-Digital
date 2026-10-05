"""Fit the wordmark's typographic layout: Montserrat @ wght, HarfBuzz shaping (kerning),
uniform tracking per line, cap height from the source. Reports per-letter centre residuals."""
import io, json, sys
from pathlib import Path
import numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).resolve().parent
G = json.load(open(HERE / 'wordmark_glyphs.json'))
WGHT = float(sys.argv[2]) if len(sys.argv) > 2 else 630
tt = instantiateVariableFont(TTFont(sys.argv[1]), {'wght': WGHT})
buf = io.BytesIO(); tt.save(buf); data = buf.getvalue()
(HERE / f'Montserrat-{int(WGHT)}.ttf').write_bytes(data)
upm = tt['head'].unitsPerEm; cap = tt['OS/2'].sCapHeight; gs = tt.getGlyphSet()
face = hb.Face(data); font = hb.Font(face)
out = {'wght': WGHT, 'upm': upm, 'cap': cap}
for key, text in (('line1', 'JEMBATAN SELARAS'), ('line2', 'DIGITAL')):
    m = G[key + '_metrics']; s = m['cap_height'] / cap           # px per font unit
    buf_ = hb.Buffer(); buf_.add_str(text); buf_.guess_segment_properties(); hb.shape(font, buf_, {'kern': True})
    names = [tt.getGlyphName(i.codepoint) for i in buf_.glyph_infos]
    pen_x, glyphs = 0.0, []
    for nm, pos in zip(names, buf_.glyph_positions):
        bp = BoundsPen(gs); gs[nm].draw(bp)
        glyphs.append((nm, pen_x, pos.x_advance, bp.bounds)); pen_x += pos.x_advance
    ink = [(nm, x, adv, b) for nm, x, adv, b in glyphs if b]           # skip the space
    src = G[key]
    # model: centre_px = x0 + s * (x + (b0+b2)/2) + i * track, i = glyph index in the run (incl. space)
    idx = [i for i, (nm, x, adv, b) in enumerate(glyphs) if b]
    A = np.c_[np.ones(len(ink)), np.array(idx, float)]
    model_c = np.array([s * (x + (b[0] + b[2]) / 2) for nm, x, adv, b in ink])
    src_c = np.array([(g['x0'] + g['x1'] + 1) / 2 for g in src])  # pixel-edge convention (+1 on the right)
    (x0, track), *_ = np.linalg.lstsq(A, src_c - model_c, rcond=None)
    res = src_c - (model_c + x0 + track * np.array(idx))
    widths_src = np.array([g['x1'] - g['x0'] + 1 for g in src]); widths_mod = np.array([s * (b[2] - b[0]) for nm, x, adv, b in ink])
    print(f'{key} "{text}": scale {s:.5f} px/unit (cap {m["cap_height"]} px), tracking {track:.2f} px '
          f'({track / s:.0f} units), x0 {x0:.2f}')
    print('   centre residuals px:', ' '.join(f'{t}{r:+.1f}' for t, r in zip(text.replace(' ', ''), res)))
    print('   width ratio src/model:', ' '.join(f'{t}{a / b:.2f}' for t, a, b in zip(text.replace(' ', ''), widths_src, widths_mod)))
    out[key] = {'text': text, 'scale': s, 'tracking_px': track, 'x0': x0, 'baseline': m['baseline'],
                'glyphs': [{'name': nm, 'x': x, 'adv': adv} for nm, x, adv, b in glyphs],
                'residual_px': res.tolist()}
json.dump(out, open(HERE / 'wordmark_layout.json', 'w'), indent=1)
