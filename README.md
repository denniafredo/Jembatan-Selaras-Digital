# Jembatan Selaras Digital — Company Profile

Single-page company profile built with **React 18 + Vite 6 + Tailwind CSS v4**.
Design direction follows the Textio agency template: light background, large display
type, uppercase eyebrow labels, marquee tickers, and card grids.

## Run it

```bash
npm install
npm run dev       # http://localhost:5173
npm run build     # outputs to dist/
npm run preview   # serve the production build
```

## Where the content lives

**All copy is in [`src/data/site.js`](src/data/site.js).** Edit that one file to change
the site — nothing in the components needs touching.

Placeholders you should replace before going live:

| What | Where in `site.js` |
| --- | --- |
| Email, phone, WhatsApp, address | `company` |
| Social links | `company.social` |
| Project case studies | `projects` |
| Testimonial quotes and names | `testimonials` |
| Client roster in the ticker | `clients` |
| Stats (120+, 60+, 7 yrs, 98%) | `stats` |
| Budget ranges in the form | `contact.budgets` |

## Sections

| Component | Section |
| --- | --- |
| `Navbar` | Sticky header, mobile drawer |
| `Hero` | Headline, CTAs, SVG bridge illustration, keyword ticker |
| `Manifesto` | The load-speed / mobile argument + performance targets |
| `Services` | Four service cards |
| `About` | Studio story, three principles, animated stat counters |
| `Work` | Filterable project grid |
| `Testimonials` | Client quote carousel + client name ticker |
| `Contact` | Contact details + brief form |
| `Footer` | Sitemap, social, address |

## Contact form

The form has no backend. Two options:

1. **Leave it as is** — it opens the visitor's mail client with the brief pre-filled
   and sends to `company.email`.
2. **Wire a form backend** — copy `.env.example` to `.env` and set:

   ```
   VITE_CONTACT_ENDPOINT=https://formspree.io/f/xxxxxxx
   ```

   The form then POSTs JSON (`name`, `company`, `email`, `phone`, `interest`,
   `budget`, `message`) to that URL.

## Brand

Defined as CSS custom properties in [`src/index.css`](src/index.css) under `@theme`,
so every Tailwind utility (`bg-brand`, `text-ink`, `border-line`, …) comes from here.

| Token | Hex | Use |
| --- | --- | --- |
| `--color-brand` | `#0E93D3` | Primary blue — bridge & arcs |
| `--color-brand-dark` | `#0B76AB` | Hover / pressed states |
| `--color-brand-soft` | `#E7F4FB` | Tinted chips and pills |
| `--color-ink` | `#6A7A87` | Body text & details |
| `--color-ink-900` | `#2C3A44` | Headings, dark sections (deepened `#6A7A87` for contrast) |
| `--color-muted` | `#98B0BE` | Secondary text |
| `--color-line` | `#CDD9E0` | Borders & dividers |
| `--color-paper` | `#FEFEFE` | Background |
| `--color-paper-2` | `#F4F7F9` | Alternating section background |

The logo is redrawn as vector in [`src/components/Logo.jsx`](src/components/Logo.jsx)
(`LogoMark` for the mark alone, `Logo` for mark + wordmark, `mono` prop for the dark
footer). `public/favicon.svg` and `public/og-image.svg` use the same paths.

## Performance notes

This is the studio's own argument, so the site has to hold up to it:

- **No image files.** The logo, the bridge illustration, and the project thumbnails
  are all inline SVG — nothing to download, nothing to lazy-load, no layout shift.
- **Production bundle: ~58 KB JS + ~7 KB CSS gzipped.** React is the only dependency.
- **No animation library.** Scroll reveals use one `IntersectionObserver` per element
  that disconnects after firing; marquees are pure CSS `transform` animations.
- **`prefers-reduced-motion` is respected** — reveals, marquees, counters, and the
  testimonial autoplay all stop.
- **Fonts**: one family (Plus Jakarta Sans) with `preconnect` and `display=swap`.
  Self-host it in `public/` if you want to drop the third-party request entirely.
- **Responsive from 320px up.** Verified at 390px and 1400px.

### Replacing the placeholder project thumbnails

`ProjectVisual` in [`src/components/Work.jsx`](src/components/Work.jsx) draws an
abstract dashboard. When you have real screenshots, swap it for:

```jsx
<img src={project.image} alt="" loading="lazy" decoding="async"
     width="480" height="300" className="h-full w-full object-cover" />
```

Keep `width`/`height` so the layout does not shift, and export at ~1.5× the rendered
size as WebP or AVIF.

## Deploy

Static output — `npm run build`, then serve `dist/`.

- **Vercel / Netlify / Cloudflare Pages**: build command `npm run build`, output
  directory `dist`.
- **Shared hosting**: upload the contents of `dist/` to the web root.

Before launch: replace the placeholder content, set the real domain in the `canonical`
and `og:*` tags in [`index.html`](index.html), and update the `Organization` JSON-LD
block there.
