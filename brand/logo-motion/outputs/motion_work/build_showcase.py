"""Build logo_motion.html with the Pixel2Motion showcase template, then specialise it.

    python build_showcase.py <pixel2motion>/scripts

1. Runs the skill's animate_svg_showcase.py on logo.svg + motion.css (hero, tuners, QA hooks).
2. Replaces the template's generic image atoms (scale / squash / spin, off-personality for a
   no-squash professional brand) with semantic studies cloned from the same logo.svg:
   hover re-draw, deck, tower, cables + hangers. Clones get prefixed ids so masks stay unique.
3. Narrows the principles strip to the principles this choreography uses.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
scripts = Path(sys.argv[1])
# optional: <svg> <out.html> <duration ms> <title>   (default: the mark)
svg_in = ROOT / (sys.argv[2] if len(sys.argv) > 2 else 'logo.svg')
out = ROOT / (sys.argv[3] if len(sys.argv) > 3 else 'logo_motion.html')
duration = sys.argv[4] if len(sys.argv) > 4 else '1000'
title = sys.argv[5] if len(sys.argv) > 5 else 'Jembatan Selaras Digital — Logo Motion'
subprocess.run([sys.executable, str(scripts / 'animate_svg_showcase.py'), str(svg_in),
                '--css', str(ROOT / 'motion.css'), '--out', str(out),
                '--title', title, '--duration-hint', duration], check=True)
html = out.read_text(encoding='utf-8')


def swap(old: str, new: str) -> None:
    global html
    if old not in html:
        raise SystemExit(f'template changed, cannot find: {old[:60]!r}')
    html = html.replace(old, new, 1)


swap('--accent: #e64036;', '--accent: #0E93D3;')
# registered property for the tower rise: must sit at top level, outside the template's
# reduced-motion @media wrapper (see the note at the top of motion.css)
swap('  <style>\n', "  <style>\n    @property --jsd-rise { syntax: '<length>'; inherits: false; initial-value: 0px; }\n\n")

swap('''    <div class="atom" data-atom="hover"><div class="atom-stage"></div><span class="atom-label">Hover</span></div>
    <div class="atom" data-atom="pulse"><div class="atom-stage"></div><span class="atom-label">Pulse</span></div>
    <div class="atom" data-atom="arc"><div class="atom-stage"></div><span class="atom-label">Arc</span></div>
    <div class="atom" data-atom="press"><div class="atom-stage"></div><span class="atom-label">Press</span></div>''',
     '''    <div class="atom" data-atom="redraw"><div class="atom-stage"></div><span class="atom-label">Hover · re-draw</span></div>
    <div class="atom" data-atom="deck"><div class="atom-stage"></div><span class="atom-label">Deck</span></div>
    <div class="atom" data-atom="tower"><div class="atom-stage"></div><span class="atom-label">Tower</span></div>
    <div class="atom" data-atom="cables"><div class="atom-stage"></div><span class="atom-label">Cables</span></div>''')

swap('''    <span class="pill" data-p="squashstretch">Squash &amp; stretch</span>
    <span class="pill" data-p="anticipation">Anticipation</span>
    <span class="pill" data-p="staging">Staging</span>
    <span class="pill" data-p="followthrough">Follow through</span>
    <span class="pill" data-p="overlap">Overlapping</span>
    <span class="pill" data-p="slowinout">Slow in / out</span>
    <span class="pill" data-p="arc">Arc</span>
    <span class="pill" data-p="secondary">Secondary action</span>
    <span class="pill" data-p="timing">Timing</span>
    <span class="pill" data-p="appeal">Appeal</span>''',
     '''    <span class="pill" data-p="anticipation">Anticipation</span>
    <span class="pill" data-p="staging">Staging</span>
    <span class="pill" data-p="slowinout">Slow in / out</span>
    <span class="pill" data-p="timing">Timing</span>
    <span class="pill" data-p="overlap">Overlapping</span>
    <span class="pill" data-p="followthrough">Follow through</span>
    <span class="pill" data-p="arc">Arcs</span>
    <span class="pill" data-p="solid">Solid drawing</span>
    <span class="pill" data-p="appeal">Appeal</span>''')

swap('''      const phases = [
        ["staging", "timing"],
        ["anticipation", "squashstretch"],
        ["arc", "slowinout"],
        ["overlap", "followthrough"],
        ["appeal"]
      ];''', '''      const phases = [
        ["anticipation", "staging"],    // 0-200 ms: the deck lays the ground line
        ["timing", "slowinout"],        // 200-400: the tower rises and eases into place
        ["overlap", "followthrough"],   // 400-600: cables draw, hangers drop as the pen passes
        ["arc", "solid"],               // 600-800: the ring's halves travel its own curve
        ["appeal"]                      // 800-1000: the halves meet at the top
      ];''')

# atom studies: same geometry, prefixed ids, one beat isolated per atom
swap('''    .atom-stage img {''', '''    .atom-stage svg {
      width: 100%;
      height: 100%;
      overflow: visible;
    }

    .atom[data-atom="deck"] :is(.jsd-tower, .jsd-cable-pen, .jsd-hanger, .jsd-arc-pen),
    .atom[data-atom="tower"] :is(.jsd-deck, .jsd-cable-pen, .jsd-hanger, .jsd-arc-pen),
    .atom[data-atom="cables"] :is(.jsd-deck, .jsd-tower, .jsd-arc-pen) {
      animation: none !important;
    }

    .atom-stage img {''')

start = html.index('    function setupAtomImages() {')
end = html.index('    function applyQaMode() {')
html = html[:start] + '''    function cloneLogo(prefix, motion) {
      const json = JSON.stringify(LOGO)
        .replace(/"id":"([^"]+)"/g, (_, id) => `"id":"${prefix}${id}"`)
        .replace(/url\\(#([^)]+)\\)/g, (_, id) => `url(#${prefix}${id})`);
      const svg = createSvgNode(JSON.parse(json));
      svg.removeAttribute("width");
      svg.removeAttribute("height");
      svg.setAttribute("data-motion", motion);
      return svg;
    }

    const ATOM_MOTION = { redraw: "redraw", deck: "intro", tower: "intro", cables: "intro" };
    const ATOM_PILLS = {
      redraw: ["slowinout", "appeal"], deck: ["anticipation", "staging"],
      tower: ["timing", "solid"], cables: ["overlap", "followthrough"]
    };

    function playAtom(atom) {
      const kind = atom.dataset.atom;
      flashPills(...ATOM_PILLS[kind]);
      atom.querySelector(".atom-stage").replaceChildren(cloneLogo(`atom-${kind}-`, ATOM_MOTION[kind]));
    }

    function setupAtomImages() {
      document.querySelectorAll(".atom").forEach(atom => {
        atom.querySelector(".atom-stage").replaceChildren(cloneLogo(`atom-${atom.dataset.atom}-`, "static"));
      });
    }

    function setupAtoms() {
      document.querySelectorAll(".atom").forEach(atom => {
        const stage = atom.querySelector(".atom-stage");
        stage.addEventListener("mouseenter", () => playAtom(atom));
        stage.addEventListener("click", () => playAtom(atom));
      });
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      if (new URLSearchParams(location.search).has("t") || new URLSearchParams(location.search).has("static")) return;
      document.querySelectorAll(".atom").forEach((atom, i) => {
        setTimeout(() => playAtom(atom), DURATION / Math.max(playbackRate, 0.25) + 400 + i * 600);
      });
    }

''' + html[end:]
out.write_text(html, encoding='utf-8')
print(out)
