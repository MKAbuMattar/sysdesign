# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [0.10.0] - 2026-07-16

### Changed

- **`/sysdesign:plan` resumes instead of restarting.** If `.sysdesign-<project>/requirements.md`
  already exists, the command reads it and asks whether to resume (re-interview only the areas
  you want to change) or start over — it never silently overwrites a locked plan.
- **`/sysdesign:evolve` gains the same output convention as `plan`**: the current-state map and
  constraints go to `.sysdesign-<project>/requirements.md`, the target design and migration path
  to `EVOLUTION.md`, building on any prior plan files instead of clobbering them.

## [0.9.0] - 2026-07-15

### Added

- **`/sysdesign:evolve`** — brownfield companion to `plan`: maps the current system, names the
  forcing function, then designs the target state and a **rollback-safe migration path**
  (strangler-fig, dual-write + backfill, cutover) with the metric that gates each step.
- Command glyphs for `find` and `evolve` (`assets/commands/`), and both wired into the site.

## [0.8.0] - 2026-07-15

### Added

- **`/sysdesign:find`** — searches the reference knowledge base and surfaces the specific `##`
  section(s) that cover a term, ranked and pointing to each source by name. Discovery/navigation
  across all 14 references, distinct from `explain` (which teaches one concept in depth).

## [0.7.2] - 2026-07-15

### Changed

- Broaden the skill's auto-invoke `description` to name all fourteen reference domains
  (adds payments, networking, OS & concurrency, AI/ML systems, and architecture patterns), so
  the skill activates on those prompts, not just the original set.

## [0.7.1] - 2026-07-15

### Added

- **`argument-hint`** on every command (e.g. `/sysdesign:plan [system to design]`), so the
  slash-command menu shows what each expects — a documented Claude Code best practice.
- **`repository`** field in `plugin.json` (the documented, recommended source-code URL).

## [0.7.0] - 2026-07-14

### Added

- **Cost model.** Every plan now includes a rough monthly **cost table** — order-of-magnitude for
  the big line items (CDN/egress, primary DB, search, compute, storage) derived from the capacity
  estimate — and names the dominant cost.
- **Money/critical-path sequence diagram.** The architecture section now includes a Mermaid
  `sequenceDiagram` for the reserve → deposit → webhook → ledger → payout flow, not just a flowchart.

### Changed

- Plan template and skill mandate `<br/>` (never `\n`) in Mermaid labels so diagrams render.
- `validate.sh` and CI now enforce that **every reference keeps its Ask-first (`AskUserQuestion`)
  note**, alongside the existing manifest / self-contained / mapping / frontmatter checks.

## [0.6.0] - 2026-07-14

### Added

- **`/sysdesign:plan`** — a dedicated command that runs the full multi-round interview and emits
  a complete, concrete plan following a fixed section template
  (`skills/system-design/plan-template.md`). All files are written to `.sysdesign-<project-name>/`
  at the repo root (`PLAN.md` + `requirements.md`), and it closes with a validation round.
- A **worked example plan** (`examples/marketplace-plan.md`) demonstrating the target depth.

### Changed

- **Full designs are now a multi-round interview.** The skill runs at least ~8 rounds of
  `AskUserQuestion` — one system area per round (product/scope, users/scale, data/consistency,
  API/clients, auth/security, money path, media/search, infra/delivery, reliability/cost) —
  adapting each round to the previous answers before it designs anything, and **closes with a
  mandatory validation round** to confirm the design and resolve any residual conflicts.
- **Plans must be complete and concrete.** The output now covers every section — requirements →
  estimate → data model → API → architecture + diagram → component choices → money path →
  security → caching → search/media → deployment → reliability/observability → tradeoffs →
  risks — grounded in the answers and real numbers, never a generic summary.

## [0.5.0] - 2026-07-14

### Added

- **Clarify-first behavior.** The skill now gathers requirements with the `AskUserQuestion`
  tool *before* designing. The first question establishes the **project type** (web app, API
  service, marketplace, real-time app, data/ML pipeline, infra/platform, …), which decides
  which references and commands even apply.
- **Iterative questioning with "Other".** Questions are asked a couple at a time; a custom
  "Other" answer opens the next adapted question and can change the design direction. Looping
  continues until the design-determining inputs are settled.
- An **"Ask first" note on every reference file** naming that domain's design-changing forks —
  deployment target (K8s · Docker · VM · serverless · on-prem), auth model (session · JWT ·
  SSO · passwordless), data shape, RAG vs fine-tune, PSP vs direct acquiring, and so on.
- **No silent assumptions.** A missing input is always asked, never invented; if the user
  delegates the call, the pick is stated explicitly and can be vetoed.
- **Conflict detection.** When answers pull against each other (strong consistency + huge write
  scale, HA on a tiny budget, passwordless + legacy clients), the skill names the conflict,
  explains why it can't all hold, and asks how to resolve it before designing.

### Changed

- All commands except `help` now prefer asking with `AskUserQuestion` over assuming; assumptions
  are a labelled fallback only when the user declines or says "just assume".
- Work is **scoped to what the project needs** — no mechanical dump of every command or artifact.

## [0.4.0] - 2026-07-14

### Added

- Initial public release: **1 skill (`system-design`), 10 commands, 14 self-contained reference files.**
- Commands: `explain`, `compare`, `review`, `choose`, `estimate`, `tradeoffs`, `diagram`,
  `interview`, `cheatsheet`, `help`.
- References covering all fifteen *System Design 101* categories, including `networking`,
  `os-concurrency`, `payments`, `ai-ml-systems`, and `dev-tools`.
- `artifacts/` — generic Mermaid diagrams and a self-contained `uv` export script that bundles
  the references into Markdown / PDF / docx.
- `scripts/validate.sh` and a CI workflow enforcing valid manifests, zero external links, mapped
  references, and frontmatter.
- Community-health files, brand assets (logo, icon, favicons, per-command glyphs), and an Astro
  landing page for [sysdesign.mkabumattar.com](https://sysdesign.mkabumattar.com).

### Notes

- The knowledge is **self-contained** — original prose with no external links, inspired by (never
  copied from) ByteByteGo's *System Design 101*. MIT-licensed.

[0.10.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.10.0
[0.9.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.9.0
[0.8.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.8.0
[0.7.2]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.7.2
[0.7.1]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.7.1
[0.7.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.7.0
[0.6.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.6.0
[0.5.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.5.0
[0.4.0]: https://github.com/mkabumattar/sysdesign/releases/tag/v0.4.0
