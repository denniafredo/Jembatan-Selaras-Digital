"""Logo motion QA on the real site (vite preview), Playwright + Edge.

    python site_qa.py http://localhost:4790 <out_dir>

Checks: navbar build (seeked frames), hand-off to idle, end state == static (pixel-exact),
hover + keyboard re-draw, About waits for scroll, footer hover, reduced motion, console errors.
"""
import io
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

URL, OUT = sys.argv[1], Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
NAV = 'header .jsd-mark'
SCHEME = os.environ.get('QA_SCHEME', 'light')  # run the same checks in either theme
results = []


def check(name, ok, detail=''):
    results.append(ok)
    print(f'{"PASS" if ok else "FAIL"}  {name}{"  — " + detail if detail else ""}')


def shot(page, sel):
    return np.asarray(Image.open(io.BytesIO(page.locator(sel).first.screenshot())).convert('RGB')).astype(int)


def seek(page, sel, t):
    page.evaluate("""([sel, t]) => document.querySelector(sel).getAnimations({ subtree: true })
        .forEach(a => { a.pause(); a.currentTime = t; })""", [sel, t])


with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge')
    errors = []

    # --- 1. navbar build, seeked frame by frame (4x DPR so a 36 px mark is inspectable)
    ctx = browser.new_context(viewport={'width': 1280, 'height': 800}, device_scale_factor=4, color_scheme=SCHEME)
    page = ctx.new_page()
    page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(URL)
    page.wait_for_selector(NAV)
    state0 = page.get_attribute(NAV, 'data-motion')
    n_anims = page.evaluate(f"document.querySelector('{NAV}').getAnimations({{ subtree: true }}).length")
    registered = page.evaluate("CSS.registerProperty ? getComputedStyle(document.querySelector('header .jsd-tower')).getPropertyValue('--jsd-rise') : 'n/a'")
    check('navbar starts in intro with all part animations attached', state0 == 'intro' and n_anims == 12,
          f'data-motion={state0}, {n_anims} animations, --jsd-rise={registered!r}')
    # t=0 first: seeking to the end fires animationend, which (correctly) settles the mark.
    # empty = identical to the same spot with the logo hidden (works on any theme background)
    box = page.locator(NAV).bounding_box()
    clip = lambda: np.asarray(Image.open(io.BytesIO(page.screenshot(clip=box))).convert('RGB')).astype(int)
    seek(page, NAV, 0); t0 = clip()
    page.evaluate(f"document.querySelector('{NAV}').style.visibility = 'hidden'"); bg = clip()
    page.evaluate(f"document.querySelector('{NAV}').style.visibility = ''")
    d0 = int((np.abs(t0 - bg).max(2) > 2).sum())
    check('navbar frame t=0 is empty', d0 == 0, f'{d0} px differ from the bare background')
    frames = []
    for t in (0, 200, 300, 445, 537, 600, 740, 850, 930, 1000):
        seek(page, NAV, t)
        frames.append((t, shot(page, NAV)))
    w = frames[0][1].shape[1]
    strip = Image.new('RGB', (w * len(frames), frames[0][1].shape[0] + 22), 'white')
    for i, (t, im) in enumerate(frames):
        strip.paste(Image.fromarray(im.astype(np.uint8)), (i * w, 22))
        ImageDraw.Draw(strip).text((i * w + 4, 4), f'{t}ms', fill=(0, 0, 0))
    strip.save(OUT / 'site_navbar_strip.png')

    # fresh load: the rest of the checks use the natural flow (script-finished CSS animations
    # would stay attached and pollute later seeks)
    page.goto(URL)
    page.wait_for_function(f"document.querySelector('{NAV}').dataset.motion === 'idle'", timeout=5000)
    left = page.evaluate(f"document.querySelector('{NAV}').getAnimations({{ subtree: true }}).length")
    check('build hands off to idle and detaches every animation', left == 0, f'{left} animations left')
    page.evaluate("document.querySelector('main').style.visibility = 'hidden'")  # compare the logo, not the hero
    idle_nav = shot(page, NAV)

    # --- 2. hover re-draw: mid-flight frame, then back to idle and identical to rest
    page.hover('header a[href="#top"]')
    page.wait_for_function(f"document.querySelector('{NAV}').dataset.motion === 'redraw'", timeout=2000)
    seek(page, NAV, 90)
    mid = shot(page, NAV)
    Image.fromarray(mid.astype(np.uint8)).save(OUT / 'site_navbar_hover_90ms.png')
    page.evaluate(f"document.querySelector('{NAV}').getAnimations({{ subtree: true }}).forEach(a => a.play())")
    page.wait_for_function(f"document.querySelector('{NAV}').dataset.motion === 'idle'", timeout=3000)
    page.mouse.move(640, 500)
    after = shot(page, NAV)
    check('hover re-draw runs and returns to the exact rest state', int(np.abs(mid - idle_nav).max()) > 0
          and int((np.abs(after - idle_nav).max(2) > 0).sum()) == 0)

    # --- 3. keyboard focus parity
    page.evaluate("document.activeElement && document.activeElement.blur()")
    page.evaluate(f"""() => {{ window.__motionLog = []; new MutationObserver(() =>
        window.__motionLog.push(document.querySelector('{NAV}').dataset.motion))
        .observe(document.querySelector('{NAV}'), {{ attributes: true, attributeFilter: ['data-motion'] }}); }}""")
    page.keyboard.press('Tab')  # skip link
    page.keyboard.press('Tab')  # logo link
    focused = page.evaluate("document.activeElement.getAttribute('href')")
    page.wait_for_timeout(500)
    state_k = page.evaluate("window.__motionLog.join(' > ')")
    check('keyboard focus on the logo link re-draws too', focused == '#top' and state_k == 'redraw > idle',
          f'focused {focused}, data-motion={state_k}')

    # --- 4. About: waits for scroll, then builds and settles
    about = '#about .jsd-mark'
    st = page.get_attribute(about, 'data-motion')
    page.evaluate("document.querySelector('main').style.visibility = ''")
    check('About mark waits off-screen (pending)', st == 'pending', f'data-motion={st}')
    page.locator(about).scroll_into_view_if_needed()
    page.wait_for_function(f"document.querySelector('{about}').dataset.motion === 'intro'", timeout=4000)
    page.wait_for_function(f"document.querySelector('{about}').dataset.motion === 'idle'", timeout=4000)
    page.wait_for_timeout(900)  # let the card's own reveal transition finish
    about_idle = shot(page, about)

    # --- 5. footer hover
    foot = 'footer .jsd-mark'
    page.locator(foot).scroll_into_view_if_needed()
    st_f = page.get_attribute(foot, 'data-motion')
    page.hover('footer .jsd-mark')
    page.wait_for_function(f"document.querySelector('{foot}').dataset.motion === 'redraw'", timeout=2000)
    page.wait_for_function(f"document.querySelector('{foot}').dataset.motion === 'idle'", timeout=3000)
    check('footer: static at rest, re-draws on hover', st_f == 'idle')
    ctx.close()

    # --- 6. reduced motion: static immediately, no animations, same pixels as the settled build
    ctx = browser.new_context(viewport={'width': 1280, 'height': 800}, device_scale_factor=4, reduced_motion='reduce', color_scheme=SCHEME)
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_selector(NAV)
    st_r = page.get_attribute(NAV, 'data-motion')
    n_r = page.evaluate(f"document.querySelectorAll('.jsd-mark').length && [...document.querySelectorAll('.jsd-mark')].reduce((n, s) => n + s.getAnimations({{subtree:true}}).length, 0)")
    page.mouse.move(640, 500)
    page.evaluate("document.querySelector('main').style.visibility = 'hidden'")
    static_nav = shot(page, NAV)
    page.evaluate("document.querySelector('main').style.visibility = ''")
    check('reduced motion: static logo, zero animations', st_r == 'idle' and n_r == 0, f'data-motion={st_r}, {n_r} animations')
    d = np.abs(idle_nav - static_nav).max(2)
    check('Final Frame Contract on the site: settled navbar build == static logo', int((d > 0).sum()) == 0,
          f'{int((d > 0).sum())} differing px')
    page.locator(about).scroll_into_view_if_needed(); page.wait_for_timeout(900)
    d2 = np.abs(about_idle - shot(page, about)).max(2)
    check('Final Frame Contract on the site: settled About build == static logo', int((d2 > 0).sum()) == 0,
          f'{int((d2 > 0).sum())} differing px')
    ctx.close()
    # --- 7. About lockup at real size: seeked frames in a fresh page
    ctx = browser.new_context(viewport={'width': 1280, 'height': 800}, device_scale_factor=2, color_scheme=SCHEME)
    page = ctx.new_page(); page.goto(URL)
    page.locator(about).scroll_into_view_if_needed()
    page.wait_for_function(f"document.querySelector('{about}').dataset.motion === 'intro'", timeout=4000)
    page.wait_for_timeout(1200)  # the card's own reveal settles; then seek the build
    frames = []
    for t in (0, 400, 800, 1000, 1150, 1300, 1450, 1600):
        seek(page, about, t); frames.append((t, shot(page, about)))
    w = frames[0][1].shape[1]
    strip = Image.new('RGB', (w * len(frames), frames[0][1].shape[0] + 22), 'white')
    for i, (t, im) in enumerate(frames):
        strip.paste(Image.fromarray(im.astype(np.uint8)), (i * w, 22)); ImageDraw.Draw(strip).text((i * w + 4, 4), f'{t}ms', fill=(0, 0, 0))
    strip.save(OUT / 'site_about_lockup_strip.png')
    ctx.close()
    browser.close()

check('no console errors', not errors, '; '.join(errors[:3]))
print(f'\n{sum(results)}/{len(results)} checks passed')
