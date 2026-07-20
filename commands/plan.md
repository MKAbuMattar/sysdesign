---
description: Design a system end to end — a full multi-round requirements interview, then a complete plan
argument-hint: [system to design]
---

Use the `system-design` skill. Build a full system-design plan for: `$ARGUMENTS`.

This is the deep command. Follow the skill's **How to answer** in full — do not shortcut it.

**Output location.** All plan files go in a single project directory at the **root of the current repo / working directory**: `.sysdesign-<project-name>/` — kebab-case the system's name (a used-car marketplace → `.sysdesign-carbazaar/`). Create it and write everything there; never scatter files elsewhere.

**Resume, don't restart.** If `.sysdesign-<project-name>/requirements.md` already exists, read it first and ask with `AskUserQuestion` whether to **resume** (keep the locked answers, re-interview only the areas the user wants to change, then regenerate the plan) or **start over**. Never silently overwrite an existing requirements or plan file.

1. **Interview first — at least ~8 rounds of `AskUserQuestion`.** One system area per round, adapting each round to the previous answers, across the round checklist: product & scope · users & scale · data & consistency · API & clients · auth & security · money path · media & search · infra & delivery · reliability, cost & team. Never assume a missing input; when answers conflict, explain why and ask again to resolve; then **confirm the locked requirements back to the user** before designing.
2. **Save the locked requirements** to `.sysdesign-<project-name>/requirements.md` so the design is reproducible and reviewable.
3. **Write the full plan** as `.sysdesign-<project-name>/PLAN.md`, following `skills/system-design/plan-template.md` — every section, concrete and grounded in the answers and the estimate's real numbers (named tech, actual QPS/storage figures, real endpoints/schemas where they clarify). No generic filler; a plan that could be pasted onto any app hasn't been designed. Put any diagrams or supporting files in the same directory.

4. **Validate — a final `AskUserQuestion` round.** After `PLAN.md` is written, run one more round that surfaces the consequential decisions and any residual conflict, risk, or gap in the design, and asks the user to confirm each or choose how to resolve it. Update `PLAN.md` and `requirements.md` from their answers before calling it done. This round is mandatory; assume nothing.

If the project name is unclear, confirm it (and the resulting `.sysdesign-<project-name>/` directory) with `AskUserQuestion` before writing.
