# Contributing to sysdesign

Thanks for helping improve the plugin. Before you start, read **`AGENTS.md`** (how the repo
works) and **`DESIGN.md`** (the editorial system). Contributions that don't follow the
editorial rules will be asked to change before merge.

## What this repo is

A Claude Code plugin: one skill (`system-design`), a set of `/sysdesign:<verb>` commands, and
nine self-contained reference files. It is plain Markdown + two JSON manifests — **no build,
no stack, no runtime.**

## Ways to contribute

- **Fix or sharpen a reference file** — correct a claim, tighten prose, add a missing tradeoff.
- **Add a topic** — a new `skills/system-design/references/<topic>.md` **and** a matching row in
  the `SKILL.md` reference map. Nothing is discoverable without the map row.
- **Add a command** — a new `commands/<verb>.md` wrapper over the one skill. Do **not** create a
  second skill for a new intent.

## The editorial rules (non-negotiable)

1. **Self-contained.** No external links inside `skills/`. The knowledge lives in the file; a
   reader never clicks out. Attribution to ByteByteGo is one line in `SKILL.md`.
2. **License-clean.** *System Design 101* is CC BY-NC-ND 4.0. Write original prose; never copy
   its text or reproduce its diagrams/images. The taxonomy is inspiration, not source.
3. **Tradeoff-first.** State the constraint → pick the fitting option → name what it costs. A
   best-practice list with no stated tradeoff will be rejected.
4. **House style.** Terse, opinionated. Colon definition lists (`- **Term**: explanation`),
   decision-first tables, concrete numbers, em-dash discipline (≤ ~3 per 300 words). No AI
   tells (`leverage`/`utilize`/`delve`/`robust`, filler adverbs, negative parallelism).

## Before you open a PR

Run the same checks CI runs (a few seconds, no install beyond `python3` + `bash`):

```bash
bash scripts/validate.sh
```

It checks: manifests parse and versions match, zero external links in `skills/`, every
reference file is in the SKILL.md map, and frontmatter is present on the skill and commands.

Then load the plugin in Claude Code and run a real query (e.g. `/sysdesign:explain consistent
hashing`) to confirm it reads well.

## Commits & PRs

- **Conventional-commit** subject + body (`feat:`, `fix:`, `docs:`, `refactor:` …).
- **No** `Co-Authored-By` trailer, **no** "Generated with Claude Code", **no** AI/assistant
  mention of any kind.
- Bump the version in **both** `plugin.json` and `marketplace.json` together when content or the
  command set changes.
- Keep PRs focused; don't bundle unrelated changes.

By contributing you agree your work is licensed under the repo's [MIT License](../LICENSE) and
that you follow the [Code of Conduct](CODE_OF_CONDUCT.md).
