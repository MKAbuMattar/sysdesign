---
description: Back-of-envelope capacity estimate — QPS, storage, bandwidth, memory
---

Use the `system-design` skill, `references/interview.md`. Estimate for: `$ARGUMENTS`.

1. State assumptions out loud (DAU, actions/user/day, read:write ratio, payload size, retention). Assume and label anything the user didn't give; ask only for a number that materially changes the answer.
2. Derive, showing one line of arithmetic each: QPS (average, then peak ≈ avg × 2–10), storage/day and /year, bandwidth, and cache working-set memory.
3. Round hard to powers of ten.
4. End with the single resource that drives the design (the bottleneck) and what it implies for the architecture.
