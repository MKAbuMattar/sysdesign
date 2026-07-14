# AGENTS.md — sysdesign

Instructions for AI agents working in this repo. Human contributors: see `README.md`.

## What this is

A **Claude Code plugin** that gives an AI coding agent system-design knowledge:
one skill (`system-design`) plus commands for explaining, comparing, reviewing, choosing,
interview prep, cheatsheets, and help. The register is **reference** — the value is the
prose, not any UI. The editorial system lives in **`DESIGN.md`**; read it before writing
or editing any reference content.

There is **no build, no stack, no runtime**: the plugin is plain Markdown (the skill and
its reference files) plus two JSON manifests. It installs via
`/plugin marketplace add mkabumattar/sysdesign`. Knowledge is inspired by ByteByteGo's
*System Design 101* but written from scratch — see Conventions.

## Layout

- `.claude-plugin/plugin.json` — plugin manifest (name, version, description, keywords).
- `.claude-plugin/marketplace.json` — marketplace entry (source `./`, category, tags).
- `skills/system-design/SKILL.md` — the router: overview, when-to-use, reference map, how-to-answer, attribution.
- `skills/system-design/references/*.md` — nine self-contained topic files. The agent loads only the one a task needs.
- `commands/*.md` — one file per `/sysdesign:<verb>` slash command (thin wrappers that invoke the skill).
- `artifacts/` — generic, shareable outputs: `diagrams/*.mmd` (Mermaid sources) + a README index. Built into git-ignored `dist/` by `scripts/export.py`. Nothing here is project- or vendor-specific.
- `scripts/` — `validate.sh` (checks) and `export.py` (bundle builder). Both self-contained; `export.py` is a uv/PEP 723 script (no config, no network).
- `assets/` — `logo.svg` (horizontal lockup) + `icon.svg` (square mark). Self-contained SVG, no external fonts/assets. Amber-on-ink; generic (a distributed-node / CAP-tradeoff triangle).
- `README.md` — human-facing install + overview. `LICENSE` — MIT.

## Reference files (the knowledge)

`api-web` · `data-storage` · `caching-performance` · `distributed-systems` ·
`security-auth` · `devops-k8s` · `architecture-patterns` · `case-studies` ·
`networking` · `os-concurrency` · `payments` · `ai-ml-systems` · `dev-tools` · `interview`

Each stands alone: dense original prose, tradeoff-first, no external links. Adding a topic
means a new `references/<topic>.md` **and** a row in the SKILL.md reference map.

## Working commands

There is no compiler; "validation" is one script (the source of truth CI also runs):

| Command | What it does |
|---|---|
| `bash scripts/validate.sh` | Manifests parse + versions match, zero external links in `skills/`, every reference file mapped in SKILL.md, frontmatter present. **Must pass before commit.** |
| `uv run scripts/export.py` | Build the shareable bundle (numbered md + PDF + docx) from the reference files into git-ignored `dist/`. Optional. |
| `grep -rnE '(#\|//) ?ponytail:' .` | Deferred-shortcut ledger (should be empty for this repo). |

Test a change by loading the skill/command in Claude Code and running a real query
(`/sysdesign:explain consistent hashing`), not by any build step.

## Conventions

- **Self-contained content.** The knowledge lives in the reference files. **No external
  links inside `skills/`** — a reader must never need to click out. Attribution to
  ByteByteGo is a single line in `SKILL.md`, nothing more.
- **License.** *System Design 101* is CC BY-NC-ND 4.0. Write original prose; never copy
  their text or reproduce their diagrams/images. The taxonomy is inspiration, not source.
- **Editorial system is normative.** Terse, opinionated, tradeoff-first. Colon definition
  lists (`- **Term**: explanation`), tables for option-vs-need, em-dash discipline, no AI
  tells. See `DESIGN.md` for the full system and the bans.
- **1 skill, N commands.** New intents are new `commands/*.md` wrappers over the one skill,
  not new skills. Keep the reasoning consistent: state the constraint → pick the fitting
  option → name the tradeoff.

## Hard rules

- **Valid manifests.** Both JSON files must parse and versions must match before any commit.
- **Zero external guide links in `skills/`.** Run the grep above; it must return 0.
- **Clean commits.** Conventional-commit subject + body. **No** `Co-Authored-By` trailer,
  **no** "Generated with Claude Code", **no** Opus/Anthropic/AI mention of any kind.
- **Don't commit local tooling.** `.serena/`, `.claude/settings.local.json`, `.DS_Store`
  are git-ignored — never add them.
- **Bump the version in both manifests together** when the skill's content or command set
  changes; keep `plugin.json` and `marketplace.json` in sync.
- Push only when asked.
