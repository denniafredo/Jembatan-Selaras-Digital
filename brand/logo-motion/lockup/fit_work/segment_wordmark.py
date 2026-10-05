"""Segment the lockup's wordmark into per-letter coverage masks (connected components)."""
import json
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
a = np.asarray(Image.open(HERE.parent / 'source_lockup.png').convert('RGB')).astype(float)
INK = np.array([74, 95, 113.])
cov = np.clip((255 - a.mean(2)) / (255 - INK.mean()), 0, 1)
np.save(HERE / 'wordmark_cov.npy', cov.astype(np.float32))
LINES = {'line1': ('JEMBATANSELARAS', (660, 730)), 'line2': ('DIGITAL', (735, 795))}
out = {}
for key, (text, (y0, y1)) in LINES.items():
    m = cov[y0:y1] > 0.5
    lab = np.zeros(m.shape, int); comps = []
    for sy, sx in zip(*np.nonzero(m)):
        if lab[sy, sx]: continue
        q = deque([(sy, sx)]); lab[sy, sx] = len(comps) + 1; pts = []
        while q:
            y, x = q.popleft(); pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < m.shape[0] and 0 <= xx < m.shape[1] and m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = len(comps) + 1; q.append((yy, xx))
        if len(pts) > 30:
            p = np.array(pts); comps.append((int(p[:, 1].min()), int(p[:, 1].max()), int(p[:, 0].min()) + y0, int(p[:, 0].max()) + y0, len(pts)))
    comps.sort()
    assert len(comps) == len(text), (key, len(comps), comps)
    out[key] = [{'char': c, 'x0': b[0], 'x1': b[1], 'y0': b[2], 'y1': b[3], 'px': b[4]} for c, b in zip(text, comps)]
    flat = [g for g in out[key] if g['char'] in 'EBTNLRMDIK']
    top = float(np.median([g['y0'] for g in flat])); base = float(np.median([g['y1'] for g in flat])) + 1
    out[key + '_metrics'] = {'cap_top': top, 'baseline': base, 'cap_height': base - top}
    print(key, text, 'cap height', base - top, 'top', top, 'baseline', base)
    print('   ', ' '.join(f"{g['char']}:{g['x0']}-{g['x1']}" for g in out[key]))
json.dump(out, open(HERE / 'wordmark_glyphs.json', 'w'), indent=1)
