---
description: Pressure-test an architecture or diagram for gaps, SPOFs, and missing safeguards
argument-hint: [architecture or file]
---

Use the `system-design` skill. Review the architecture the user describes or the diagram/file they point to: `$ARGUMENTS`.

If the architecture, its target load, or its consistency needs aren't clear from the request, clarify with `AskUserQuestion` before reviewing — a review against unknown constraints is guesswork.

Check for, and report only what actually applies:
- Single points of failure and missing redundancy
- No timeouts / retries / circuit breakers / backpressure
- Cache hazards (stampede, penetration, hot keys, no TTL)
- Data hazards (dual writes, unbounded growth, missing idempotency)
- Auth/authz gaps, secrets handling, input validation at boundaries
- Missing observability (metrics/logs/traces, health probes)
- Scaling bottlenecks tied to the stated load

Hand back a prioritized list: critical → nice-to-have. Don't invent problems; if it's sound, say so.
