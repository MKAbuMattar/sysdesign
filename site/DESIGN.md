# DESIGN — sysdesign site

The visual system for the landing page. Tokens live in `src/styles/global.css`; this documents
them and the rules. **Dark-only** (OLED, terminal-native) — there is no light theme.

## Palette (CSS custom properties)

| Token | Value | Role |
|---|---|---|
| `--ink` | `#0e1116` | body background |
| `--ink-2` | `#161d27` | surface (cards, terminal) |
| `--ink-3` | `#1d2632` | elevated surface, chips-on-hover |
| `--line` | `#2d3748` | 1px borders (separation is a border + tonal step, never a shadow) |
| `--line-2` | `#3a465a` | stronger border / hairline connectors |
| `--paper` | `#f6f8fb` | primary text |
| `--muted` | `#97a1b2` | secondary text (≥4.5:1 on ink) |
| `--faint` | `#6b7688` | tertiary / meta |
| `--accent` | `#5b8def` | **primary brand (blue) — the hub** |
| `--teal` | `#3bb89a` | secondary accent |
| `--amber` | `#e0a458` | secondary accent |
| `--accent-soft` / `--accent-line` | rgba(91,141,239,.14 / .42) | glow, tinted borders |

The blue/teal/amber triad mirrors the three outer nodes of the logo. Use `--accent` as the
default; bring in teal + amber only where the triad is meaningful (the principle nodes, the
terminal's REST/GraphQL/gRPC lines, the feature dots).

## Typography

- **Mono** (`--mono`): `ui-monospace, "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace` — headings, wordmark, code, terminal, labels, the brand voice.
- **Sans** (`--sans`): `Inter, ui-sans-serif, system-ui, …` — body prose (readability).
- Contrast-axis pairing (mono display + humanist-sans body), not two similar sans.
- Sizes are `clamp()`-driven: hero `clamp(1.6rem, 7vw, 3.9rem)`, h2 `clamp(1.5rem, 5vw, 2.5rem)`. `text-wrap: balance` on headings; `overflow-wrap: break-word` guards long words.
- System font stacks only — **no web-font fetch** (self-contained, fast, offline-safe).

## Layout & spacing

- Container: `.wrap`, `max-width: 1120px`, padding `0 24px` (18px < 760px).
- Section rhythm: `92px` vertical (`68px` < 760px).
- Grid for 2D (command grid, features), flex for 1D (nav, cta rows). Responsive grids use `repeat(auto-fill, minmax(min(100%, N), 1fr))` so cards never overflow small screens.
- Radius `--r: 14px`; pills `999px`.

## Motion (GSAP + Three.js)

- **Hero node-field** (`components/HeroCanvas.astro`): a Three.js network of ~120 additive-blended nodes with three glowing, pulsing brand hubs (blue/teal/amber = the logo), depth fog, slow rotation, cursor parallax, and a **scroll-scrubbed camera dolly** (the field pushes out and spins as the hero scrolls). Masked off the left-side copy; behind the hero at `z-index: 0`, `pointer-events: none`, `aria-hidden`.
- **GSAP** (`Base.astro`): a hero entrance timeline (tag → **clip-reveal headline** → lead → CTA → command), `ScrollTrigger.batch` section reveals, and a scroll-scrub **parallax** on the hero terminal. Ease `power3.out`; `--ease: cubic-bezier(0.22, 1, 0.36, 1)` for CSS transitions. No bounce.
- `.reveal` is **visible in CSS by default**; GSAP hides then animates only when motion is allowed, so a JS failure never blanks a section.
- **Micro-interactions** (motion-gated in `Base.astro`): the hero terminal *types* its command then prints the result rows; primary CTAs are **magnetic** (drift toward the cursor via `gsap.quickTo`); command-card glyphs pop on hover (CSS). The nav **condenses** (elevation) once scrolled — a functional state kept regardless of motion pref.
- Keep it to a few distinctive, content-fitting motions per view, not one uniform entrance on everything (that reflex is the AI tell).
- **Reduced motion is gated in JS**: `prefers-reduced-motion` skips the GSAP timelines and renders the Three.js scene as a single static frame; the cursor stops blinking. Also pause the render loop on `visibilitychange`.

## Components

Layout `Base.astro` (head, meta, skip-link, scripts). Sections: `Nav, Hero, Principle, Commands,
Topics, Features, About, Install, Footer`. Primitives in `components/ui/`: `Button, Eyebrow,
Terminal, CommandCard, Chip, Node, CopyLine`. Data in `src/data/plugin.ts`.

## Bans (match-and-refuse)

- No gradient text, no decorative glassmorphism, no shadows for separation (use 1px `--line`).
- No **side-stripe** accents — the hue lives in a full border or a node dot (see the principle cards).
- No **em/en dashes** in copy (`grep -rn '[—–]' src` must be 0) — periods, colons, commas instead.
- No light theme, no web-font fetch, no UI framework. Motion dependencies are limited to **GSAP** and **Three.js**; everything else stays native.
- No text that overflows its container at any breakpoint (test 375px).
