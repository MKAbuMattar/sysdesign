---
description: Compare two or more system design options and recommend one for a stated constraint
argument-hint: [option vs option]
---

Use the `system-design` skill. The user wants to compare: `$ARGUMENTS`.

1. Clarify the deciding constraint with `AskUserQuestion` if it isn't stated (scale, consistency, latency, ops burden, tech-stack fit). Don't assume it — if the user won't say, offer the options with their consequences and ask again.
2. Give a short comparison table: each option's strength, weakness, and the tradeoff.
3. Make a recommendation tied to the constraint — not a neutral "it depends."
4. Note what would change your recommendation.
