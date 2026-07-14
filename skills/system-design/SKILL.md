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

1. **Restate the constraint.** Traffic pattern, consistency need, latency budget, team/ops reality. No numbers → ask or assume out loud.
2. **Pick the rung that fits.** Reuse before build, managed before self-hosted, boring before novel. Name the option.
3. **Name the tradeoff.** Every choice costs something (consistency, ops burden, cost, latency). Say it.
4. **Flag the non-negotiables.** Validation at trust boundaries, data-loss handling, auth, and observability are never dropped to "keep it simple."

## Attribution & licensing

The topic taxonomy is inspired by ByteByteGo's *System Design 101* (CC BY-NC-ND 4.0). This skill is original prose written to stand alone; it does not reproduce their text or images. The source, with diagrams, lives at the ByteByteGoHq/system-design-101 repository on GitHub.
