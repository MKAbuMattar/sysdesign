# AGENTS.md — sysdesign site

Instructions for AI agents working in `site/`. Read **PRODUCT.md** (what it is) and **DESIGN.md**
(the visual system) before any UI change.

## Stack

**Astro 7**, static output, no integrations — plain `.astro` + one global stylesheet. Package
manager **pnpm**. No UI framework. Motion uses two deliberate deps: **GSAP** (+ ScrollTrigger) for
entrance/scroll animation and **Three.js** for the hero node-field; scripts are bundled Astro
`<script>` modules, gated on `prefers-reduced-motion`. System font stacks, no web-font fetch.

## Commands

| Command | What it does |
|---|---|
| `pnpm --dir site dev` | Local preview. Check every UI change here before commit. |
| `pnpm --dir site build` | Static build to `site/dist/`. **Must pass before commit.** |
| `grep -rn '[—–]' site/src` | Em/en-dash check — **must return 0** (humanizer rule). |

## Layout

- `src/pages/` — routes: `index.astro` (landing), `404.astro`.
- `src/layouts/Base.astro` — HTML shell: head/meta/OG, favicon + manifest, skip-link, the reveal + copy scripts.
- `src/components/` — section components (Nav, Hero, Principle, Commands, Topics, Features, About, Install, Footer).
- `src/components/ui/` — reusable primitives (Button, Eyebrow, Terminal, CommandCard, Chip, Node, CopyLine). UI-related components go here.
- `src/data/plugin.ts` — single source for the command list, topics, and install strings.
- `src/styles/global.css` — the design tokens and all styling.
- `public/` — served verbatim: `logo.svg`, `icon.svg`, `favicon.svg`, `commands/*.svg`, `robots.txt`, `llms.txt`, `sitemap.xml`, `manifest.webmanifest`, `CNAME` (custom domain).

## Conventions

- **Design system is normative.** Use the tokens in `DESIGN.md`; don't introduce new colors, fonts, or a light theme. Keep the blue/teal/amber triad meaningful, not decorative.
- **Content is data-driven.** Command/topic lists come from `src/data/plugin.ts` — update there, not in markup. Keep counts in sync with the plugin (`../.claude-plugin/plugin.json`).
- **Accessibility.** Keyboard-navigable, visible `:focus-visible` rings, skip-link, honor `prefers-reduced-motion`, contrast ≥ 4.5:1 for body text.
- **Self-contained assets.** SVG only, no external fonts/CDNs.

## Hard rules

- `pnpm --dir site build` passes and the em-dash grep returns 0 before any commit.
- Base path stays `/` (served at the root of a custom domain, `sysdesign.mkabumattar.com`; `CNAME` in `public/`).
- Keep the dependency surface tiny: GSAP and Three.js power the motion. Don't add a UI framework or further libraries for what native code already covers, and lazy-load / reduced-motion-gate anything heavy.
- The site is **not** the plugin — never move plugin files under `site/`, and keep site copy free of the plugin's editorial em-dash style (site copy has zero em dashes).
