# Plan template

The section skeleton every `/sysdesign:plan` output follows. Each section is **concrete** —
named tech, real numbers, actual endpoints/schemas — never generic. Drop a section only if the
project genuinely lacks it (e.g. no money path) and say so explicitly.

1. **Requirements (locked)** — functional + non-functional, in/out of scope, the success metric, and the answers gathered in the interview. Name the non-negotiables (validation at trust boundaries, data-loss handling, auth, observability).
2. **Capacity & cost estimate** — QPS (average + peak), storage/day and /year, bandwidth, cache working set (one line of arithmetic each; round hard; name the bottleneck resource). Then a **rough monthly cost table** — order-of-magnitude for the big line items (CDN/egress, primary DB, search, compute, object storage) derived from those numbers — and name the dominant cost. Ranges, not false precision.
3. **Data model** — core entities with key fields and relationships; the store each lives in; hot vs cold; retention.
4. **API surface** — the handful of endpoints (or GraphQL/gRPC equivalents) that carry the load; auth on each; pagination; idempotency where writes retry.
5. **High-level architecture** — a Mermaid `flowchart` (clients → edge → services → data + cache + queue) plus the critical path and the async paths, **and a Mermaid `sequenceDiagram` for the critical/money path** (e.g. reserve → deposit → PSP webhook → ledger → payout). In every Mermaid label use `<br/>` for line breaks, never `\n` (it doesn't render).
6. **Component choices** — a table, each row `constraint → option → what it costs`: primary DB, cache, queue/log, search, blob + CDN, deploy target.
7. **Money path** (if any) — authorize/capture/settle or deposit/escrow/payout; idempotency keys; the ledger (double-entry, append-only); reconciliation; PCI scope.
8. **Security & auth** — auth model, permission model, secrets management, TLS, input validation, the threat surface.
9. **Caching & performance** — what's cached at each tier, TTLs, invalidation, the latency budget, the order of attack for "it's slow".
10. **Search & media** — the search engine and the facets that matter; image/video upload, transcode, CDN delivery.
11. **Deployment & regions** — cloud, deploy target and strategy (rolling/blue-green/canary), region topology, DR (RTO/RPO), CI/CD, IaC.
12. **Reliability & observability** — SLOs; failure modes and mitigations (timeouts, retries + backoff, circuit breakers, backpressure, idempotency); metrics/logs/traces; alert on symptoms users feel.
13. **Tradeoff ledger** — every major choice and the bill it comes with; what the design optimized for and what it deferred.
14. **Risks & what would change the design** — the metric or event that flips each "not yet" decision (the number that says "now shard", "now go multi-region", …).
