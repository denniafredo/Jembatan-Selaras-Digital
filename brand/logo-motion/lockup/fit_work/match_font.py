"""Rank candidate fonts against the wordmark letter by letter (pixel2motion wordmark matching).

Per letter: cap height matched to the source, baseline pinned, horizontal centre aligned with a
quarter-pixel search; score = IoU of 0.5-coverage masks and ink-weight ratio (render ink / source ink).

    python match_font.py <fonts_dir> [weights...]
"""
import io, json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
cov = np.load(HERE / 'wordmark_cov.npy').astype(float)
G = json.load(open(HERE / 'wordmark_glyphs.json'))
fonts_dir = Path(sys.argv[1]); weights = [int(w) for w in sys.argv[2:]] or [400, 450, 500, 550, 600]
SS = 4


def instances(path):
    tt = TTFont(path)
    if 'fvar' not in tt:
        yield None, tt; return
    axes = {a.axisTag: a for a in tt['fvar'].axes}
    lo, hi = axes['wght'].minValue, axes['wght'].maxValue
    for w in weights:
        if lo <= w <= hi:
            loc = {t: (w if t == 'wght' else a.defaultValue) for t, a in axes.items()}
            yield w, instantiateVariableFont(TTFont(path), loc)


def score_line(tt, key):
    m = G[key + '_metrics']; cap_px = m['cap_height']; base = m['baseline']
    upm = tt['head'].unitsPerEm; cap = tt['OS/2'].sCapHeight or 0.7 * upm
    buf = io.BytesIO(); tt.save(buf); buf.seek(0)
    size = cap_px * upm / cap
    font = ImageFont.truetype(buf, int(round(size * SS)))
    ious, src_ink, ren_ink = [], 0.0, 0.0
    for g in G[key]:
        x0, x1, y0, y1 = g['x0'] - 3, g['x1'] + 4, g['y0'] - 3, g['y1'] + 4
        win = cov[y0:y1, x0:x1]
        # mask out neighbours: only this letter's own pixels count on the source side
        srcm = win > 0.5
        W_, H_ = (x1 - x0) * SS, (y1 - y0) * SS
        best = (-1, 0)
        canvas_w = W_ + 400
        img = Image.new('L', (canvas_w, H_), 0); d = ImageDraw.Draw(img)
        d.text((200, (base - y0) * SS), g['char'], font=font, fill=255, anchor='ls')
        arr = np.asarray(img).astype(float) / 255
        cols = np.nonzero(arr.max(0) > 0.5)[0]
        if not len(cols):
            return None
        ink_c = (cols[0] + cols[-1]) / 2
        src_c = ((g['x0'] + g['x1'] + 1) / 2 - x0) * SS
        for dx in range(-6, 7):
            off = int(round(ink_c - src_c)) + dx
            if off < 0 or off + W_ > canvas_w:
                continue
            crop = arr[:, off:off + W_]
            r = Image.fromarray((crop * 255).astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BOX)
            rc = np.asarray(r).astype(float) / 255
            rm = rc > 0.5
            iou = (rm & srcm).sum() / max(1, (rm | srcm).sum())
            if iou > best[0]:
                best = (iou, rc.sum())
        ious.append(best[0]); src_ink += win.sum(); ren_ink += best[1]
    return float(np.mean(ious)), ren_ink / src_ink, ious


rows = []
for path in sorted(fonts_dir.glob('*.ttf')):
    for w, tt in instances(path):
        res = [score_line(tt, k) for k in ('line1', 'line2')]
        if None in res:
            continue
        (i1, r1, g1), (i2, r2, g2) = res
        rows.append({'font': path.stem, 'wght': w, 'iou1': i1, 'ink1': r1, 'iou2': i2, 'ink2': r2, 'per1': g1, 'per2': g2})
rows.sort(key=lambda r: -(r['iou1'] * 15 + r['iou2'] * 7) / 22)
json.dump(rows, open(HERE / 'font_match.json', 'w'), indent=1)
print(f"{'font':24} {'wght':>5} {'IoU line1':>9} {'ink1':>6} {'IoU line2':>9} {'ink2':>6}")
for r in rows[:18]:
    print(f"{r['font']:24} {str(r['wght']):>5} {r['iou1']:9.4f} {r['ink1']:6.3f} {r['iou2']:9.4f} {r['ink2']:6.3f}")
