---
name: system-design
description: Use when designing, reviewing, or explaining backend/distributed system architecture — API styles, databases and storage, caching, messaging, scalability, resiliency, security/auth, DevOps/Kubernetes deployment, or preparing for a system design interview.
---

# System Design

## Overview

A concise, opinionated reference for reasoning about backend and distributed systems. Use it to explain a concept, compare options, pressure-test an architecture, or drill interview topics. Each topic leads to a fuller, self-contained reference file under `references/` — the knowledge lives here, not behind a link.

**Core principle:** design is a chain of tradeoffs, not a stack of best practices. State the constraint, pick the option that fits it, name what you gave up.

## When to use

- "How does X work / explain X" for a system-design concept (polling vs SSE vs WebSocket, CDN, sharding, Kafka, OAuth, K8s service types...)
- "X vs Y" comparisons (REST vs GraphQL vs gRPC, SQL vs NoSQL, Redis vs Memcached, orchestration vs choreography)
- Reviewing an architecture or diagram for gaps (single points of failure, missing backpressure, cache stampede, auth holes)
- Choosing a component under real constraints (which DB, which queue, which deployment strategy)
- Interview prep (framework for answering, algorithms to know, common problems)

Not for: writing application code (use language skills), or product/business decisions.

## Reference map

Load the file that matches the topic. Each is a standalone quick-reference.

| Area | File | Covers |
|------|------|--------|
| API & web | `references/api-web.md` | REST/GraphQL/gRPC, gateways vs LBs vs reverse proxies, polling/SSE/WebSocket, HTTP versions, pagination, API security |
| Data & storage | `references/data-storage.md` | SQL vs NoSQL, sharding, replication, isolation/ACID, CAP, Kafka & queues, CDC, consistency patterns |
| Caching & performance | `references/caching-performance.md` | cache strategies, eviction, stampede, CDN, Redis, latency budgets |
| Scale & distributed | `references/distributed-systems.md` | scalability strategies, resiliency/retry/idempotency, fault tolerance, unique IDs, IaC, 12-factor |
| Security & auth | `references/security-auth.md` | sessions/cookies/JWT, OAuth 2.0 flows, SSO, encryption vs encoding vs tokenization, secrets, permissions |
| DevOps & K8s | `references/devops-k8s.md` | K8s patterns & service types, deployment strategies, Docker best practices, CI/CD, observability |
| Architecture & patterns | `references/architecture-patterns.md` | monolith vs microservices, architectural patterns, orchestration vs choreography, DDD, design patterns |
| Case studies | `references/case-studies.md` | real-world architectures (Netflix, Uber, Discord, Figma...) and classic "design X" problems |
| Networking | `references/networking.md` | OSI, TCP/UDP, IP/NAT, DNS, protocols & ports, latency/geography |
| OS & concurrency | `references/os-concurrency.md` | process vs thread, concurrency vs parallelism, async/event loop, locks/deadlock, GC |
| Payments & fintech | `references/payments.md` | payment flow, idempotency, ledgers/reconciliation, hot accounts, PCI/tokenization |
| AI/ML systems | `references/ai-ml-systems.md` | data pipelines, inference serving, vector search, RAG vs fine-tune, MLOps |
| Dev tools | `references/dev-tools.md` | git model, merge vs rebase, branching, Linux essentials, diagram-as-code, shipping |
| Interview | `references/interview.md` | answer framework, algorithms to know, common design problems, tradeoff checklist |

## How to answer

Regardless of command, follow this shape:

0. **Clarify the requirements first — ask, don't assume.** **Start with what they're building.** The very first `AskUserQuestion` establishes the **project type** and its core purpose — e.g. web app · API / backend service · mobile app · marketplace · real-time / chat · data or ML pipeline · infra / platform · CLI / library — because that answer decides which references and commands even apply. **Don't run every command or emit every artifact by default; scope the work to what the project actually needs** (a static site and a payments platform share almost nothing). From there, whenever a real choice or unknown would change the outcome, **ask with `AskUserQuestion`** — never silently invent it. Offer concrete options and let the user pick; every question also lets them answer **"Other"** with their own value. Cover the dimensions that actually change the design:
   - **Scope & content** — what the app/system does, its core entities and top user actions, what's explicitly out of scope.
   - **Scale** — users / DAU, read:write ratio, data volume, growth, peak vs average.
   - **Consistency & latency** — where strong consistency is required (money, inventory) vs where eventual is fine; the latency budget.
   - **Tech stack & hosting** — preferred or mandated language, framework, database, and cloud (managed vs self-hosted); existing systems to fit.
   - **Constraints** — budget, team size / ops maturity, timeline, compliance (PCI, GDPR).

   **Ask iteratively.** Read every answer before the next question. An answer — especially a custom **"Other"** — can open a new decision or change the design's direction; when it does, ask the next `AskUserQuestion` adapted to it (e.g. "Postgres" → ask about read-replica vs sharding; a custom stack → ask what it must integrate with). Keep looping, a couple of questions at a time, until the inputs that determine the design are settled — then design against them and let those answers drive every later choice.

   Skip a dimension only when the user already gave it. **Never assume a missing input — ask.** If the user won't answer or says "you decide," don't fabricate a requirement silently: present the realistic options with their consequences via `AskUserQuestion` and either let them pick or make an explicit, labelled recommendation they can veto. A pure concept `explain` needs questions only when the user's stack or use case changes the answer.

   **Then check for conflicts, and push back.** Test the answers against each other and against the constraints before designing. When choices pull against each other — strong consistency with very high single-node write throughput, multi-region HA on a hobby budget, passwordless-only alongside a legacy-client requirement — name the conflict, explain *why* it can't all hold, and ask another `AskUserQuestion` offering concrete ways to resolve it (relax one side, pay the cost, split the requirement). Never quietly pick the winner for them.

   **A full system design or build plan is a multi-round interview — not two questions.** Cover the whole system across **at least ~8 rounds** of `AskUserQuestion` (one area per round, 1–4 questions each), adapting each round to the previous answers; do not start designing early. Work the rounds in order, skipping only what a smaller project genuinely lacks:
   1. **Product & scope** — what it is, core entities, top user actions, in/out of scope, the success metric.
   2. **Users & scale** — audience, DAU/MAU, object counts (listings, users, events…), read:write ratio, growth, regions.
   3. **Data & consistency** — each core entity's shape, where strong vs eventual consistency is required, retention, PII.
   4. **API & clients** — style (REST/GraphQL/gRPC), web vs mobile, real-time (SSE/WebSocket), third-party integrations.
   5. **Auth & security** — auth model (session/JWT/SSO/passwordless), roles/permissions, compliance.
   6. **Money path** (if any) — checkout/deposits/payouts, PSP vs direct, escrow, refunds, the ledger.
   7. **Media & search** — image/video volume, upload path, CDN, search engine, and the filters/facets that matter.
   8. **Infra & delivery** — cloud, deploy target (K8s/serverless/VM/on-prem), regions/DR, CI/CD, IaC.
   9. **Reliability, cost & team** — availability target (SLO, RTO/RPO), observability, budget, team size, timeline.

   After the rounds, reconcile conflicts, **confirm the locked requirements back to the user**, then design.
1. **Restate the constraint** you're designing against (from their answers).
2. **Pick the rung that fits.** Reuse before build, managed before self-hosted, boring before novel. Name the option.
3. **Name the tradeoff.** Every choice costs something (consistency, ops burden, cost, latency). Say it.
4. **Flag the non-negotiables.** Validation at trust boundaries, data-loss handling, auth, and observability are never dropped to "keep it simple."
5. **For a full plan, deliver every section — concrete, not generic.** Ground every choice in the answers and the estimate's real numbers. Cover, in order: locked requirements → capacity estimate (QPS, storage, bandwidth) → data model → API surface → high-level architecture with a diagram → component choices (each: constraint → option → cost) → the money path (if any) → security & auth → caching & performance → search & media → deployment & regions → reliability & observability → tradeoff ledger → risks and what would change the design. Commit to specifics — named tech, concrete numbers, real endpoints/schemas where they clarify. A plan that could be pasted onto any app hasn't been designed. Write the plan and everything it needs into `.sysdesign-<project-name>/` at the root of the current repo/working directory (kebab-case the system's name): the locked `requirements.md`, the `PLAN.md`, and any diagrams all live in that one directory.
6. **Validate the finished design with the user — one more `AskUserQuestion` round.** After the plan is written, don't call it done. Re-read the design against itself and surface its consequential decisions and any residual conflict, risk, or gap the answers didn't fully settle (e.g. the estimate now says one node won't hold; the chosen store fights the consistency need; the region plan outruns the budget). Ask the user to confirm each or choose how to resolve it, then revise the plan from their answers. This closing round is mandatory — never assume the design is right, and never resolve a conflict silently.

## Attribution & licensing

The topic taxonomy is inspired by ByteByteGo's *System Design 101* (CC BY-NC-ND 4.0). This skill is original prose written to stand alone; it does not reproduce their text or images. The source, with diagrams, lives at the ByteByteGoHq/system-design-101 repository on GitHub.
