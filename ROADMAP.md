# Roadmap

Paced improvements to the plugin, one increment per day or two. Each increment lands as its own
conventional commit; skill/command content changes bump **both** manifests, get a `CHANGELOG.md`
entry, must pass `bash scripts/validate.sh`, and ship as a tagged GitHub release.

Scope is the plugin (skill, commands, references, scripts, artifacts, docs). The site only gets
one-line count syncs so it never drifts.

| # | Days | Increment | Status |
|---|---|---|---|
| 1 | 1–2 | **Observability reference** — split observability out of `devops-k8s.md` into `references/observability.md`: SLOs/SLIs/error budgets, the three pillars and their costs, RED/USE, alerting philosophy, runbooks. 15th reference. | ✅ v0.11.0 |
| 2 | 3–4 | **Worked evolve example** — `examples/monolith-evolution.md`: monolith on one Postgres → strangler-fig + replicas + queue, rollback-gated steps. The brownfield depth bar, as `marketplace-plan.md` is for `/plan`. | planned |
| 3 | 5 | **Prose polish + hard gate** — convert excess em-dashes in the five references over the density guideline to colons/periods, then flip `lint-prose.py`'s density check from advisory to hard. | planned |
| 4 | 6–7 | **Cost-engineering reference** — `references/cost-engineering.md`: cloud unit economics, egress dominance, storage tiers, commitment discounts, cost-per-request math, the dominant-line-item method. 16th reference. | planned |
| 5 | 8 | **Rendered diagrams in exports** — `scripts/export.py` renders `artifacts/diagrams/*.mmd` to SVG when `mmdc` is available and embeds real images in the PDF/docx bundle; raw fences stay as the fallback. Nothing generated is committed. | planned |
| 6 | 9–10 | **Deepen case-studies** — the thinnest reference gains 3–4 more precedents (Stripe idempotency/ledger, Shopify flash-sale pods, Slack real-time messaging) in constraint→lesson framing. Original prose, license-clean. | planned |
| 7 | 11–12 | **README i18n** — `README.ar.md` (RTL-correct) + `README.es.md` with a language-switcher line. | planned |
| 8 | 13 | **v1.0.0 milestone** — full audit (validate + lint + official `claude plugin validate`), README polish, count/consistency sweep, CHANGELOG, tag + release. | planned |

Rejected on purpose (lean rule): new commands (the 13 intents are complete; more would be
dupes), a second skill (`AGENTS.md`'s 1-skill convention), committed generated artifacts
(drift), a "last-reviewed" process for references (ceremony).
