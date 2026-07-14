<p align="center">
  <img src="assets/logo.svg" alt="sysdesign" width="620">
</p>

# sysdesign

**System design knowledge, wired into your AI agent.** One skill, ten commands. Explain a concept, compare options, pressure-test an architecture, estimate capacity, or prep an interview — with tradeoffs stated, not hand-waved.

Inspired by [ByteByteGo's System Design 101](https://github.com/ByteByteGoHq/system-design-101). This is original prose that links back to the source guides, not a copy of them.

---

## What you get

**1 skill** — `system-design`. A router plus fourteen concise reference files (API & web, data & storage, caching, distributed systems, security/auth, DevOps/K8s, architecture & patterns, real-world case studies, networking, OS & concurrency, payments & fintech, AI/ML systems, dev tools, interview). The knowledge lives in the files — no external links to click. The agent loads only the file the task needs.

**10 commands:**

| Command | What it does |
| --- | --- |
| `/sysdesign:explain <concept>` | Explain a concept with tradeoffs and when to use it |
| `/sysdesign:compare <a> vs <b>` | Compare options, recommend one for your constraint |
| `/sysdesign:review <architecture>` | Pressure-test a design for SPOFs and missing safeguards |
| `/sysdesign:choose <component>` | Pick a DB / queue / cache / deploy strategy under constraints |
| `/sysdesign:estimate <system>` | Back-of-envelope capacity: QPS, storage, bandwidth, memory |
| `/sysdesign:tradeoffs <choice>` | Name what a design choice gains and gives up |
| `/sysdesign:diagram <system>` | Sketch the architecture as a Mermaid/ASCII diagram |
| `/sysdesign:interview <problem\|topic>` | Run interview prep with the 7-step framework |
| `/sysdesign:cheatsheet <area>` | Condense an area into a scannable cheatsheet |
| `/sysdesign:help` | List commands and reference topics |

The commands all run on the one skill, so the reasoning stays consistent: state the constraint, pick the fitting option, name the tradeoff, never drop validation/auth/observability to "keep it simple."

## Install

### Claude Code

```
/plugin marketplace add mkabumattar/sysdesign
```

```
/plugin install sysdesign@sysdesign
```

(Two separate prompts.)

### Use

```
/sysdesign:explain consistent hashing
/sysdesign:compare REST vs GraphQL vs gRPC
/sysdesign:review my checkout service: gateway -> monolith -> single Postgres
/sysdesign:choose a queue for 50k events/sec, replayable
/sysdesign:interview design a URL shortener
/sysdesign:cheatsheet caching
```

Or just talk — the `system-design` skill activates on architecture/design questions without a command.

## Layout

```
sysdesign/
  .claude-plugin/
    marketplace.json
    plugin.json
  skills/
    system-design/
      SKILL.md
      references/
        api-web.md              data-storage.md
        caching-performance.md  distributed-systems.md
        security-auth.md        devops-k8s.md
        architecture-patterns.md  case-studies.md
        networking.md  os-concurrency.md  payments.md
        ai-ml-systems.md  dev-tools.md
        interview.md
  commands/
    explain.md   compare.md    review.md    choose.md
    estimate.md  tradeoffs.md  diagram.md
    interview.md cheatsheet.md help.md
  scripts/
    validate.sh   # bash scripts/validate.sh — same checks CI runs
    export.py     # uv run scripts/export.py — build md/PDF/docx bundle → dist/
  artifacts/
    README.md     # index of shareable outputs
    diagrams/     # generic Mermaid sources (auth, sharding, caching, deploy, …)
  assets/
    logo.svg      # horizontal lockup   icon.svg  # square mark
```

## License

MIT for this repo's original content. Topic taxonomy inspired by ByteByteGo's System Design 101 (CC BY-NC-ND 4.0) — no text or images from it are reproduced here.
