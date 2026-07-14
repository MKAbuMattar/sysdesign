# Architecture & Patterns

## Monolith vs microservices

Start with a modular monolith. Split into services only when a concrete force demands it: independent scaling of one hot path, separate deploy cadence for separate teams, or a hard fault-isolation boundary. Microservices trade in-process calls for network calls — you buy independent deployability and pay in latency, partial failure, distributed transactions, and ops overhead.

Rule: don't distribute a system you don't yet understand. Extract services along seams the monolith already revealed, not up front.

## Architectural patterns (pick per force)

| Pattern | Fits when |
|---------|-----------|
| Layered (n-tier) | Standard CRUD app; clear separation, easy to staff |
| Event-driven | Loose coupling, spiky/async workloads, fan-out |
| Microkernel / plugin | Stable core + varying extensions (IDEs, workflow engines) |
| Microservices | Independent scaling & deploy per bounded context |
| CQRS | Read and write models diverge enough to justify two paths |
| Pipeline / pipes-and-filters | Staged data transformation (ETL, media processing) |

## Orchestration vs choreography

- **Orchestration**: a central coordinator tells each service what to do. Easy to reason about and observe; the coordinator is a coupling point and can become a bottleneck.
- **Choreography**: services react to events, no central brain. Loosely coupled and scalable; end-to-end flow is harder to trace and debug.

Default to orchestration for a workflow you must audit (payments, order fulfillment); choreography for broadcast/fan-out where no single owner needs the whole picture.

## Domain-Driven Design (the useful parts)

- **Bounded context**: an explicit boundary where a model and its language are consistent. Service boundaries should track bounded contexts, not database tables.
- **Ubiquitous language**: same terms in code, conversation, and docs.
- **Aggregate**: a consistency boundary — the unit you load and save transactionally.
- **Entity vs value object**: identity that persists vs a value defined only by its attributes.
- Use DDD to find seams; skip the ceremony on a simple app.

## Design patterns — the reflex ones

Strategy (swap behavior), Factory (defer construction), Observer (event notify), Adapter (fit a mismatched interface), Decorator (layer behavior), Facade (simplify a subsystem), Singleton (one instance — usually a smell; prefer DI). A pattern is a name for a shape you already needed, not a thing to add for its own sake.

UI/app structure: MVC, MVP, MVVM, VIPER — all separate rendering, state, and logic; they differ in who owns state and how the view binds to it.
