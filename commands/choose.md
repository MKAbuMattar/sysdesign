---
description: Choose a component (DB, queue, cache, deployment strategy) under real constraints
---

Use the `system-design` skill. Help choose: `$ARGUMENTS`.

1. Extract the constraints from the request; ask for the missing ones with `AskUserQuestion` before shortlisting (read/write ratio, scale, consistency, ops capacity, tech-stack / hosting).
2. Shortlist 2-3 realistic options from the relevant reference file.
3. Recommend one, tied to the constraints, and name what it costs.
4. Prefer boring/managed/reuse over novel/self-hosted unless justified.
