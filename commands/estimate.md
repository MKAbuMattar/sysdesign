---
description: Back-of-envelope capacity estimate — QPS, storage, bandwidth, memory
---

Use the `system-design` skill, `references/interview.md`. Estimate for: `$ARGUMENTS`.

1. Get the inputs that swing the result with `AskUserQuestion` (DAU, actions/user/day, read:write ratio, payload size, retention). Don't invent a number the user won't give — offer realistic ranges via `AskUserQuestion` and estimate against the chosen range.
2. Derive, showing one line of arithmetic each: QPS (average, then peak ≈ avg × 2–10), storage/day and /year, bandwidth, and cache working-set memory.
3. Round hard to powers of ten.
4. End with the single resource that drives the design (the bottleneck) and what it implies for the architecture.
