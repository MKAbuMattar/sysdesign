---
description: Search the reference knowledge base and surface the sections that cover a term
argument-hint: [term or question]
---

Use the `system-design` skill. Find: `$ARGUMENTS`.

Search across every `references/*.md` for where this is covered, and return it ranked by relevance:

1. The reference file(s) and the specific `##` section(s) that address it, quoted tightly or summarized.
2. If it spans several references, list each with a one-line note on what that file adds.
3. A one-line synthesis that answers the query from those sections.

Point to each source by name (e.g. `data-storage.md › Sharding`). Don't invent anything that isn't in the references; if it isn't covered, say so and name the closest topic. This is discovery, not a full teach-through — reach for `/sysdesign:explain` when the user wants the deep dive.
