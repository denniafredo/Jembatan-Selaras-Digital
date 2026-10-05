"""Theme toggle QA (vite preview, Playwright + Edge).    python theme_qa.py http://localhost:4790 <out_dir>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

URL, OUT = sys.argv[1], Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
BTN = 'header button[aria-label*="theme"]'
ok_all = []


def check(name, ok, detail=''):
    ok_all.append(ok); print(f'{"PASS" if ok else "FAIL"}  {name}{"  — " + detail if detail else ""}')


state = lambda page: page.evaluate("[document.documentElement.dataset.theme, localStorage.getItem('jsd-theme')]")
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    # record the theme and body colour as early as possible on every navigation (no-flash check)
    early = """document.addEventListener('DOMContentLoaded', () => { window.__early = [document.documentElement.dataset.theme,
        getComputedStyle(document.body).backgroundColor]; });"""

    ctx = b.new_context(viewport={'width': 1280, 'height': 800}, color_scheme='light', device_scale_factor=2)
    ctx.add_init_script(early); page = ctx.new_page(); errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(URL)
    check('no saved choice + OS light -> light', state(page) == ['light', None], str(state(page)))
    label0 = page.get_attribute(BTN, 'aria-label')
    page.click(BTN); page.wait_for_timeout(500)
    check('click switches to dark and remembers it', state(page) == ['dark', 'dark'], str(state(page)))
    label1 = page.get_attribute(BTN, 'aria-label')
    check('button label describes the next action', label0 == 'Switch to dark theme' and label1 == 'Switch to light theme',
          f'{label0!r} -> {label1!r}')
    page.locator('header').screenshot(path=str(OUT / 'theme_nav_dark.png'))
    page.reload()
    ev = page.evaluate('window.__early')
    check('reload keeps dark from the first paint (set before DOMContentLoaded)', ev[0] == 'dark' and ev[1] == 'rgb(12, 21, 27)', str(ev))
    page.focus(BTN); page.keyboard.press('Enter'); page.wait_for_timeout(500)
    check('keyboard Enter toggles back to light', state(page) == ['light', 'light'], str(state(page)))
    page.locator('header').screenshot(path=str(OUT / 'theme_nav_light.png'))
    logo_gray = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--color-logo-gray')")
    page.click(BTN); page.wait_for_timeout(500)
    logo_gray_d = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--color-logo-gray')")
    check('logo gray follows the theme', logo_gray.strip() == '#51626f' and logo_gray_d.strip() == '#c6d2db', f'{logo_gray} / {logo_gray_d}')
    page.locator('#services article').first.screenshot(path=str(OUT / 'theme_services_card_dark.png'))
    ctx.close()

    ctx = b.new_context(viewport={'width': 1280, 'height': 800}, color_scheme='dark')
    page = ctx.new_page(); page.goto(URL)
    check('no saved choice + OS dark -> dark', state(page) == ['dark', None], str(state(page)))
    page.emulate_media(color_scheme='light'); page.wait_for_timeout(300)
    check('follows an OS change while nothing is saved', state(page)[0] == 'light', str(state(page)))
    page.evaluate("localStorage.setItem('jsd-theme', 'light')"); page.emulate_media(color_scheme='dark'); page.reload()
    check('a saved choice beats the OS setting', state(page) == ['light', 'light'], str(state(page)))
    page.emulate_media(color_scheme='light'); page.emulate_media(color_scheme='dark'); page.wait_for_timeout(300)
    check('...and OS changes no longer override it', state(page)[0] == 'light', str(state(page)))
    ctx.close()

    ctx = b.new_context(viewport={'width': 390, 'height': 844}, color_scheme='light', device_scale_factor=2)
    page = ctx.new_page(); page.goto(URL)
    vis = page.is_visible(BTN); box = page.locator(BTN).bounding_box()
    check('mobile: toggle visible at the top right', vis and box['x'] > 250 and box['y'] < 80, str(box))
    page.locator('header').screenshot(path=str(OUT / 'theme_nav_mobile.png'))
    ctx.close(); b.close()
check('no page errors', not errors, '; '.join(errors[:2]))
print(f'\n{sum(ok_all)}/{len(ok_all)} theme checks passed')
