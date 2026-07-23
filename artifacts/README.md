# Artifacts

Generic, shareable outputs built from the `system-design` skill. Nothing here is tied to a
specific stack, vendor, or project — it's the same self-contained knowledge as the skill,
packaged for reading outside an AI agent.

## Diagrams

Original Mermaid sources in [`diagrams/`](diagrams/) (text — versionable, diffable, renders on
GitHub):

| File | Shows |
|---|---|
| `auth-oauth2-flow.mmd` | OAuth 2.0 Authorization Code + PKCE sequence |
| `db-replication-sharding.mmd` | Read replicas + sharding by key |
| `caching-layers.mmd` | Cache at every hop (CDN → app → Redis → DB) |
| `k8s-deploy-strategies.mmd` | Rolling vs blue-green vs canary |
| `request-lifecycle.mmd` | Baseline request path with async work |
| `payment-flow.mmd` | Card authorize → capture → settle |

## Building the bundle

The export script assembles the reference files (in curriculum order) plus the diagrams into a
numbered bundle: a combined Markdown, per-topic numbered Markdown, and best-effort PDF + docx.

```bash
uv run scripts/export.py          # → dist/ (git-ignored)
```

Output in `dist/`:

- `system-design-standard.md` — the whole reference as one numbered document
- `standard/NN-topic.md` — each topic as a standalone numbered file
- `system-design-standard.pdf` / `.docx` — if `weasyprint` / `htmldocx` load on your machine
- `diagrams/*.svg` — rendered diagrams (only if the mermaid CLI `mmdc` is installed); when rendered, the combined Markdown and PDF embed them as images instead of raw mermaid fences

The script is self-contained (uv/PEP 723 deps, paths relative to itself, no config, no network).
PDF/docx are best-effort: a missing optional dependency is a warning, not a failure — the
Markdown bundle always builds.
