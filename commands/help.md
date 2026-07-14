---
description: Show the sysdesign command list and reference topics
---

Use the `system-design` skill. Print this card, then stop:

```
sysdesign — system design knowledge, self-contained

commands
  /sysdesign:plan <system>            design end to end: full interview → complete plan
  /sysdesign:explain <concept>        what it is, when to use it, the tradeoff
  /sysdesign:compare <a> vs <b>       compare options, recommend one for a constraint
  /sysdesign:review <architecture>    pressure-test for SPOFs and missing safeguards
  /sysdesign:choose <component>       pick a DB/queue/cache/deploy under constraints
  /sysdesign:estimate <system>        back-of-envelope QPS/storage/bandwidth/memory
  /sysdesign:tradeoffs <choice>       name what a choice gains and gives up
  /sysdesign:diagram <system>         sketch the architecture as Mermaid/ASCII
  /sysdesign:interview <problem>      7-step framework, estimates, tradeoffs
  /sysdesign:cheatsheet <area>        condense an area into a scannable sheet
  /sysdesign:help                     this card

topics (references/)
  api-web · data-storage · caching-performance · distributed-systems
  security-auth · devops-k8s · architecture-patterns · case-studies
  networking · os-concurrency · payments · ai-ml-systems · dev-tools · interview

principle
  state the constraint → pick the fitting option → name what you gave up
```