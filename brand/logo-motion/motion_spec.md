# Logo motion spec — Jembatan Selaras Digital

Pixel2Motion v2 run (github.com/nolangz/pixel2motion): raster logo → minimal vector → choreographed motion.
Everything below traces back to the brief in §1. Source of truth for each layer:

| Layer | File | Regenerate with |
|---|---|---|
| Source raster | `source.jpg` (1024², RGB JPG, no alpha) | — |
| Geometry | `outputs/fit_work/geometry.json` | `measure.py` → `measure_parts.py` → `measure_arc.py` → `fit_logo.py` |
| Motion structure | `logo.svg` (+ `outputs/fit_work/motion_timing.json`) | `build_motion_svg.py` |
| Choreography | `motion.css` (+ `outputs/motion_work/timeline.json`) | edit by hand; hanger cues from `timeline.py` |
| Showcase | `logo_motion.html` | `outputs/motion_work/build_showcase.py <pixel2motion>/scripts` |
| Website | `src/components/logoGeometry.js`, the `logo-motion` block in `src/index.css`, `public/favicon.svg`, `public/og-image.svg` | `outputs/motion_work/gen_site_assets.py` |

Edit `motion.css` or the fit, then re-run the generators; never edit generated files by hand.

## 1. Brief

- **Personality:** steady · precise · harmonious. From the name (*jembatan* = bridge, *selaras* = in harmony), the mark's
  engineered geometry (circle, ellipse, straight tower, strict symmetry) and the studio's promise ("fast", "hold up after
  launch"). Preset: **Trustworthy / Professional**: no squash, no overshoot, one easing family.
- **Usage contexts:**
  - **Navbar:** builds once on page load.
  - **About card and footer:** the same build, once, when scrolled into view. Both include the wordmark (line 1
    written left to right, then each DIGITAL letter rising); in the footer it is the HTML text beside the mark.
  - **Hover / keyboard focus (navbar, footer and About lockups):** the full build loops, resting 800 ms on the finished
    mark between passes; on leave the current pass finishes, then the logo stays static.
  - **Reduced motion:** the static logo, immediately.
- **Choreography sketch:** the bridge is built, then harmony closes around it.
  1. The deck is laid from the centre out.
  2. The tower rises out of the deck.
  3. The cables are drawn down from the tower tops, and each hanger drops as the cable reaches it.
  4. The two halves of the ring rise from the banks and meet at the top.

## 2. Geometry (Phase 2)

| Part | id | Construction | Fit residual (source px) |
|---|---|---|---|
| Ring | `#arc` | Outer edge: axis-aligned ellipse rx 330.50 / ry 325.68. Inner edge: circle r 300.61. Two mirrored straight end faces at 32.25°. | outer rms 0.26, max 0.83 (a circle gave 2.19); inner rms 0.31; faces ≤ 0.55 |
| Deck | `#deck` | Crescent, 4 cubics, sharp tips | rms 0.21, max 0.83 |
| Tower | `#tower` | 2 tapered legs (6-point polygons) + 3 crossbars (rects) | edges from sub-pixel row/column crossings |
| Cables | `#cable-l/-r` | Outer edge 2 cubics (G1 knee), inner edge 1 cubic; closes inside the leg | rms 0.18, max 0.76; tip pinned to the last dark pixels |
| Hangers | `#hanger-l1..r3` | 6 rects (widths 11 / 9.8 / 9.5), tops inside the cable, bottoms under the deck | — |

- **Complexity:** 10 cubic segments in total. Everything else is arcs, lines and rects.
- **Symmetry:** enforced about x = 512 (the source's parts disagree by ≤ 0.35 px).
- **Path audit** (`svg_path_audit.py`): the only flagged joins are the deck's two tips and the cable tip. All three are intentional sharp corners.

**Iterations** (skill overlay at the 720 threshold; IoU@50% computed on coverage):

| # | Change | IoU | src_only | render_only |
|---|---|---|---|---|
| 00 | potrace trace (shipped before this run, level-5 baseline) | 0.9733 | 2320 | 388 |
| 01 | primitives + few cubics | 0.6186 | 2710 | 57797 (cable handle flipped upward) |
| 02 | handles constrained, no upward travel | 0.9559 | 3006 | 1510 |
| 03 | +0.5 px pixel-centre shift (measurement frame → SVG space) | 0.9740 | 2256 | 376 |
| 04 | tips measured to the real ends | **0.9740** | 2248 | 387 |

**Accepted at 04.** At the unbiased 50% threshold the vector scores 0.9773 against the potrace trace's 0.9809. That gap is deliberate smoothing:
- Residual clusters are all 1 px wide (no structural misfit).
- They are explained by JPEG halos, the enforced symmetry, and a ≤ 0.8 px flare of the ring's inner edge just before each face.

At 400% the vector is clean where the JPG stair-steps (`outputs/smoothness_zoom_400.png`). Evidence: `outputs/fit_iterations/`, `outputs/overlay_progress_strip.png`, `outputs/final_render.png`.

**Motion structure:**
- **Draw-on pens:** butt caps, `pathLength="1"`, `stroke-dasharray="1 1"`, inside masks.
  - Cable pens: a C1 spline on the cable midline (≤ 0.6 px off-centre on the free cable), 35 wide.
  - Arc pens: two elliptical arcs on the ring's centre ellipse, starting 3° past the far face corner and overlapping 1.5° past the top, 46 wide.
- **Tower clip:** the tower rises inside a clip that runs 3 units under the deck's top edge.
- **No static footprint:** the static logo with all masks and clips renders pixel-identical to the plain geometry (0 px).

## 3. Choreography (Phase 3)

One shared clock: every build part runs the full 1000 ms with `fill-mode: both`. Phases live in keyframe percentages, so `?t=` seeks the whole thing 1:1.

| Beat | Part | Window | Easing | Pattern |
|---|---|---|---|---|
| anticipation | (empty canvas) | 0–60 ms | — | beat before the first mark |
| anticipation | deck | 60–300 ms | ease-enter | mask wipe, centre → banks (`clip-path: inset`) |
| action | tower | 140–440 ms | ease-enter | rise 350 units out of the deck (`--jsd-rise`) |
| action | cables (both) | 420–740 ms | ease-settle | draw-on, tower top → deck end |
| action | hangers 1 / 2 / 3 | 517 / 537 / 555 ms, +150 ms each | ease-enter | drop from the cable (`clip-path` wipe) |
| action → follow-through | arc halves (both) | 480–1000 ms; meet ≈ 925 ms | ease-settle | draw-on from the banks, meeting at the top |
| hover | arc halves | 280 ms | ease-out | re-draw |

- **Shape:** 20 : 50 : 30.
  - Anticipation (0–200 ms): the empty beat plus the deck laying the ground line.
  - Action (200–700 ms): the tower lands, the suspension goes in, the arc accelerates.
  - Follow-through (700–1000 ms): the cables finish and the arc decelerates into the meeting.
- **Hanger cues:** derived, not picked. `timeline.py` inverts the cable easing at each hanger's arc-length fraction along the pen (0.377 / 0.538 / 0.658).
  - The cables start only once the tower is < 1 unit from home, so nothing detaches.
  - The hangers are staggered by 18–20 ms, which is 12–13 % of a drop.
- **Duration:** the 1000 ms build stretches the 300–800 ms header band on purpose. It has three beats, plays once per page load, and was agreed at "~1 s".

**Tokens:**
- `--p2m-duration: 1000ms`
- `--p2m-hover-duration: 280ms`
- `--p2m-ease-enter: cubic-bezier(0, 0, 0.2, 1)`
- `--p2m-ease-settle: cubic-bezier(0.4, 0, 0.2, 1)`

Keyframes carry the literal curves, because `var()` is dropped inside `@keyframes`.

**Principles:**
- **Staging:** one beat at a time, in the order ground → tower → suspension → closure.
- **Anticipation:** the empty beat plus the deck.
- **Slow in / out:** probe-verified.
- **Timing:** the ring is heaviest, so it is slowest (520 ms); a hanger takes 150 ms.
- **Follow-through and overlapping action:** the hangers are cued by the pen, and the ring overlaps the cables.
- **Arcs:** the ring's halves travel its own curve.
- **Solid drawing:** nothing scales or deforms (only wipes, draws and one rise), and the end state lands pixel-exact.
- **Appeal:** the two halves joining is the "harmony" moment.

**Not used:** squash & stretch, exaggeration and secondary action, all gated off by the personality.

**Implementation constraint:** there are no compositor (transform) animations. A transform animation makes Chromium raster the whole SVG on another path; edge anti-aliasing changed by up to 109 levels and would flip back when the animation detaches. So:
- the tower rises through the registered property `--jsd-rise` (needs `@property` at top level);
- the hangers drop via `clip-path`.

Without `@property` support the tower snaps up at ~290 ms instead of rising.

**Atomic studies** (showcase only): hover re-draw, deck, tower, cables + hangers. Each one isolates a single beat of the same SVG.

**Tunables:**
- `--p2m-duration` scales the whole build.
- `--p2m-hover-duration` sets the hover re-draw length.
- The rise distance (350) must stay ≥ 345 or the tower peeks out of the deck at t = 0.
- The arc start angle and overlap live in `build_motion_svg.py`.

## 3b. Stacked lockup (About card) — `lockup/`

**Source.** `lockup/source_lockup.png` is the mark above "JEMBATAN SELARAS / DIGITAL".

**Mark.** It is the same design as before, and the verified mark is reused at uniform scale 0.80764 (`lockup/fit_work/measure_mark.py`).
- This rendition differs by ≤ 2 px at 1024 px in ring thickness and hanger placement. That is generation noise, not design.
- Reuse keeps one mark site-wide. Overlay IoU@50% is 0.85; a non-uniform scale would only reach 0.90.

**Wordmark font.** Matched letter by letter against 35 OFL candidates (`match_font.py`, cap height fitted, baseline pinned).

| Font, weight | IoU line 1 | Ink line 1 | IoU line 2 | Ink line 2 | Note |
|---|---|---|---|---|---|
| Montserrat 620–640 | 0.877 | ≈ 1.0 | 0.90 | ≈ 1.0 | chosen |
| Work Sans 600 | 0.834 | | | | runner-up |
| Onest 600 | 0.822 | | | | |

The wordmark is Montserrat at wght 630, set as outlines (`build_lockup.py`): no font request, and OFL allows the use.
- Spacing: HarfBuzz kerning, with tracking fitted per word on line 1 and per line on line 2.
  - The source sets JEMBATAN at −59 units and SELARAS at −7 units. Kept, because this is the logo as given.
  - DIGITAL is set at +243 units.
- Centre residuals are ≤ 3 px (line 1) and ≤ 1.3 px (line 2).
- Region IoU@50% is 0.80 / 0.81 with ink ratios of 1.02 / 1.01. The rest is font substitution: the source letterforms (e.g. a narrower M) are not exactly Montserrat.

**Motion.**
- The mark runs its 1000 ms build unchanged.
- The wordmark runs on a 1600 ms clock that starts at the same moment.
  - Line 1, 800–1250 ms: a left-to-right `clip-path` wipe (reading order) with ease-settle, beginning as the ring decelerates into its meeting.
  - Line 2, 1100–1590 ms: each DIGITAL letter rises out of its baseline (`clip-path`, 220 ms, ease-enter), 45 ms apart.
- Drag hierarchy: mark → line 1 → line 2.

**QA.**
- Frames (`lockup/motion_frames/`, `lockup/motion_strip.png`) and showcase `lockup/logo_lockup_motion.html`.
- Easing probe: line-1 inset 82.13 % at 900 ms (designed); first letter at 80.4 % progress at 1200 ms (designed).
- Ink sweep 760–1160 ms: smooth, no stall.
- Final Frame Contract at 1600 ms: 0 px against `?static=1`, the plain static vector, and the hover end state.
- On the site: the About lockup waits off-screen, builds on scroll, and its settled state equals the static logo (0 px).

## 4. QA (evidence in `outputs/`)

| Check | Result |
|---|---|
| Frames at beats + risk windows (`motion_frames/`, `motion_strip.png`) | reading order holds, nothing clips, t = 0 has 0 ink pixels |
| Easing probe (cable, arc, tower, hanger at 4 times each) | 16 / 16 on the designed curve (e.g. tower @ 250 ms: 97.39, linear would be 221.67) |
| Ink sweeps (cable/hanger hand-offs 400–580, ring meeting 860–1000) | no stall+pop. The quiet 430–470 ms is the tower → cable beat; ink stops at ≈ 925 ms because the remaining pen travel is under the overlap |
| Final Frame Contract (same pipeline, `final_frame_contract.py`) | `?t=1000` = `?static=1` = plain static vector = hover end state, 0 px each |
| Website (`site_qa.py`, vite preview, Edge) | 11 / 11: build → idle with 0 animations left; hover and keyboard focus re-draw and return to the exact rest pixels; About waits for scroll; footer re-draws on hover; reduced motion is static with 0 animations; settled builds == static logo (0 px); no console errors |

QA scripts drive the installed Edge through `outputs/motion_work/p2m_edge.py` (no Playwright browser download).
