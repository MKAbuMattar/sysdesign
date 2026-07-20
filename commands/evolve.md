---
description: Evolve or migrate an existing system from its current state toward a goal, with a rollback-safe path
argument-hint: [current system → goal]
---

Use the `system-design` skill. Evolve: `$ARGUMENTS`.

Brownfield, not greenfield: start from what already exists, never a blank page. Follow the skill's **How to answer**, but interview around the *current* system first (with `AskUserQuestion`, one area at a time):

1. **Map the current state** — what's deployed now (stack, data stores, scale, the actual pain), what's forcing the change (a scale wall, cost, reliability, team), and the hard constraints: pieces that can't change, downtime budget, migration-risk tolerance.
2. **Name the forcing function** — the one limit or goal the evolution must hit. If the target and the constraints conflict (zero downtime + a schema rewrite, say), surface it and ask how to resolve it.
3. **Design the target state, then the migration path** — the ordered, reversible steps from here to there (strangler-fig, dual-write + backfill, read-replica cutover, shadow traffic), each with its rollback and the metric that says it's safe to proceed to the next.
4. Name what each step gives up and where data-loss or downtime risk lives. The non-negotiables (no data loss, auth, observability) hold throughout the migration, not just at the end.

**Output location.** Same convention as `/sysdesign:plan`: write to `.sysdesign-<project-name>/` at the repo root — the current-state map and locked constraints to `requirements.md`, the target design and step-by-step migration path to `EVOLUTION.md`. If the directory already has files (e.g. a prior plan), read them first and build on them; never silently overwrite.

Prefer the smallest change that removes the forcing function. Don't rewrite what isn't the bottleneck. For a from-scratch design use `/sysdesign:plan` instead.
