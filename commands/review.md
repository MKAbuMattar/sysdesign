---
description: Pressure-test an architecture or diagram for gaps, SPOFs, and missing safeguards
---

Use the `system-design` skill. Review the architecture the user describes or the diagram/file they point to: `$ARGUMENTS`.

Check for, and report only what actually applies:
- Single points of failure and missing redundancy
- No timeouts / retries / circuit breakers / backpressure
- Cache hazards (stampede, penetration, hot keys, no TTL)
- Data hazards (dual writes, unbounded growth, missing idempotency)
- Auth/authz gaps, secrets handling, input validation at boundaries
- Missing observability (metrics/logs/traces, health probes)
- Scaling bottlenecks tied to the stated load

Hand back a prioritized list: critical → nice-to-have. Don't invent problems; if it's sound, say so.
