---
description: Sketch a system architecture as a Mermaid (or ASCII) diagram
argument-hint: [system]
---

Use the `system-design` skill. Diagram: `$ARGUMENTS`.

If the system's scope or major components aren't clear from the request, clarify with `AskUserQuestion` first, then diagram.

Produce a Mermaid `flowchart` of the architecture: clients → edge (LB/gateway) → services → data + cache + queue, with the data flow labeled. Include only the components that matter for the question.

- Mark trust boundaries and label edges sync vs async.
- If the user asks for ASCII, use boxes and arrows instead of Mermaid.
- Follow the diagram with 2–3 lines: the critical path, the single points of failure, and where it scales next.
