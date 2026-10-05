"""Final Frame Contract, same pipeline (Playwright + Edge, same viewport/DPR, same page).

  A  ?t=<end>           reveal seeked to its end (default 1000 ms)
  B  ?static=1          template's finished state
  C  data-motion=static the plain static vector (no animation attached at all)
  D  hover re-draw run to completion, then compared with C (interaction end-state)
Every pair must be pixel-identical.
"""
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

html = Path(sys.argv[1]).resolve().as_uri()
END = int(sys.argv[3]) if len(sys.argv) > 3 else 1000  # ms: the reveal's last frame
out_dir = Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)


def grab(page):
    return np.asarray(Image.open(io.BytesIO(page.locator('#logo-root').screenshot())).convert('RGB')).astype(int)


with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge')
    page = browser.new_page(viewport={'width': 900, 'height': 600}, device_scale_factor=2)
    shots = {}
    page.goto(f'{html}?t={END}'); page.wait_for_function('window.__p2mReady === true'); shots['A_t1000'] = grab(page)
    page.goto(f'{html}?static=1'); page.wait_for_function('window.__p2mReady === true'); shots['B_static1'] = grab(page)
    page.evaluate("""() => { const s = document.querySelector('#logo-root svg');
        s.getAnimations({subtree: true}).forEach(a => a.cancel()); s.setAttribute('data-motion', 'static'); }""")
    page.wait_for_timeout(100); shots['C_plain'] = grab(page)
    page.evaluate("""() => { const s = document.querySelector('#logo-root svg'); s.setAttribute('data-motion', 'redraw');
        s.getAnimations({subtree: true}).forEach(a => a.finish()); }""")
    page.wait_for_timeout(100); shots['D_redraw_end'] = grab(page)
    browser.close()

for k, v in shots.items():
    Image.fromarray(v.astype(np.uint8)).save(out_dir / f'ffc_{k}.png')
ok = True
for a, b in (('A_t1000', 'B_static1'), ('A_t1000', 'C_plain'), ('D_redraw_end', 'C_plain')):
    d = np.abs(shots[a] - shots[b]).max(axis=2)
    n = int((d > 0).sum()); ok &= n == 0
    print(f'{a:13} vs {b:10}: {n} differing pixels (max channel diff {int(d.max())})  {"PASS" if n == 0 else "FAIL"}')
print('Final Frame Contract:', 'PASS' if ok else 'FAIL')
