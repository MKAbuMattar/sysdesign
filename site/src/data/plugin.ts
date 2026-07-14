// Single source for the plugin's commands, topics, and install steps.

export interface Command {
  name: string;
  short: string;
  long: string;
  example: string;
}

export const commands: readonly Command[] = [
  {
    name: "plan",
    short: "design end to end: full interview → complete plan",
    long: "Runs the full multi-round requirements interview (about 8 to 9 rounds, one system area per round), reconciles any conflicting answers, then writes a complete, concrete plan to a .sysdesign-<project>/ folder and closes with a validation round.",
    example: "/sysdesign:plan a car marketplace",
  },
  {
    name: "explain",
    short: "what it is, when to use it, the tradeoff",
    long: "Explains a concept in plain terms: what it is, when to reach for it and when not to, the tradeoff it makes, and one concrete example. Tight, not a textbook.",
    example: "/sysdesign:explain consistent hashing",
  },
  {
    name: "compare",
    short: "options compared, one recommended for a constraint",
    long: "Puts options side by side for your stated constraint and commits to a recommendation instead of a neutral 'it depends'. Names what would change the call.",
    example: "/sysdesign:compare REST vs GraphQL vs gRPC",
  },
  {
    name: "review",
    short: "pressure-test a design for SPOFs and safeguards",
    long: "Pressure-tests an architecture you describe: single points of failure, missing timeouts / retries / backpressure, cache and data hazards, auth gaps, scaling bottlenecks. Ranked by what fails first.",
    example: "/sysdesign:review gateway → monolith → one Postgres",
  },
  {
    name: "choose",
    short: "pick a DB / queue / cache / deploy under constraints",
    long: "Picks a component under real constraints. Shortlists two or three realistic options from the matching reference and recommends one, naming what it costs.",
    example: "/sysdesign:choose a queue for 50k events/sec, replayable",
  },
  {
    name: "estimate",
    short: "back-of-envelope QPS, storage, bandwidth, memory",
    long: "Back-of-envelope capacity math: QPS (average and peak), storage per day and per year, bandwidth, cache working set. Rounds hard and names the bottleneck resource.",
    example: "/sysdesign:estimate a URL shortener at 100M links/day",
  },
  {
    name: "tradeoffs",
    short: "name what a choice gains and gives up",
    long: "Lists what a choice gains and gives up, one axis per line, then the single tradeoff that dominates for your constraint and the condition that would flip the decision.",
    example: "/sysdesign:tradeoffs single Postgres vs sharding",
  },
  {
    name: "diagram",
    short: "sketch the architecture as Mermaid or ASCII",
    long: "Sketches the architecture as a Mermaid flowchart (or ASCII): clients → edge → services → data, cache, queue, with the critical path and single points of failure called out.",
    example: "/sysdesign:diagram a chat app",
  },
  {
    name: "interview",
    short: "7-step framework, estimates, tradeoffs",
    long: "Runs system-design interview prep: the 7-step framework on a problem, or a focused topic drill. Models clarify-first, estimate, and state-the-tradeoff behavior.",
    example: "/sysdesign:interview design a news feed",
  },
  {
    name: "cheatsheet",
    short: "condense an area into a scannable sheet",
    long: "Condenses an area into a scannable sheet: the key choices, a when-to-use table, the failure modes, and the numbers worth knowing.",
    example: "/sysdesign:cheatsheet caching",
  },
  {
    name: "help",
    short: "list commands and reference topics",
    long: "Lists every command and the reference topics, with the one principle the skill runs on: state the constraint, pick the option, name the tradeoff.",
    example: "/sysdesign:help",
  },
] as const;

export interface Topic {
  slug: string;
  covers: string;
}

export const topics: readonly Topic[] = [
  { slug: "api-web", covers: "REST/GraphQL/gRPC, gateways vs load balancers vs reverse proxies, polling/SSE/WebSocket, HTTP versions, pagination, API security." },
  { slug: "data-storage", covers: "SQL vs NoSQL, sharding, replication, isolation and ACID, CAP, Kafka and queues, CDC, B-tree vs LSM, consistency patterns." },
  { slug: "caching-performance", covers: "Cache strategies, eviction, stampede, CDN, Redis, Memcached vs Redis, latency budgets, the order of attack for 'it's slow'." },
  { slug: "distributed-systems", covers: "The scaling ladder, resiliency (retry, circuit breaker, backpressure), idempotency, unique IDs, 12-factor, IaC, the tradeoffs to always name." },
  { slug: "security-auth", covers: "Sessions vs JWT, OAuth 2.0 and OIDC, SSO, encoding vs encryption vs hashing, secrets, RBAC/ABAC/ReBAC." },
  { slug: "devops-k8s", covers: "K8s service types and patterns, deployment strategies, Docker best practices, CI/CD, observability, DevOps vs SRE vs platform." },
  { slug: "architecture-patterns", covers: "Monolith vs microservices, architectural patterns, orchestration vs choreography, DDD, the reflex design patterns." },
  { slug: "case-studies", covers: "Netflix, Discord, Twitter, Uber, Figma, Airbnb and more, plus the classic 'design X' problems." },
  { slug: "networking", covers: "OSI, TCP vs UDP, IP and NAT, DNS, protocols and ports, latency and geography." },
  { slug: "os-concurrency", covers: "Process vs thread, concurrency vs parallelism, async and the event loop, locks and deadlock, paging, garbage collection." },
  { slug: "payments", covers: "Payment flow, idempotency, double-entry ledgers and reconciliation, hot accounts, PCI and tokenization, escrow." },
  { slug: "ai-ml-systems", covers: "Data pipelines, training vs inference serving, vector search, RAG vs fine-tune, MLOps." },
  { slug: "dev-tools", covers: "The git model, merge vs rebase, branching, Linux essentials, diagram-as-code, shipping to production." },
  { slug: "interview", covers: "The answer framework, estimation numbers, building blocks, algorithms to know, classic problems, the tradeoff checklist." },
] as const;

export const INSTALL_1 = "plugin marketplace add mkabumattar/sysdesign";
export const INSTALL_2 = "plugin install sysdesign@sysdesign";
