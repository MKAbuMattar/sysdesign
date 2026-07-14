---
description: Run system design interview prep — framework, a problem, or a topic drill
---

Use the `system-design` skill, `references/interview.md`. Topic: `$ARGUMENTS`.

- If given a problem (e.g. "design a URL shortener"): walk the 7-step framework, doing estimates out loud, and pause at the deep-dive step to let the user choose the component.
- If given a topic (e.g. "consistent hashing"): explain it interview-style — definition, why it matters, where it shows up, the tradeoff.
- If nothing specific: pick a classic problem and run it.

Model good interview behavior: clarify first, estimate, state tradeoffs, stay concise.

If this is a **real design task** (not mock-interview practice) — e.g. "design/plan our app" — gather the missing requirements up front with `AskUserQuestion` (scope & content, scale, consistency/latency, tech stack & hosting, constraints) instead of only narrating the clarify step, then design against the answers.
