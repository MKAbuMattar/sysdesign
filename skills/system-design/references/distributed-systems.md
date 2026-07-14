# Scale & Distributed Systems

## Scaling ladder

Vertical (bigger box) → stateless horizontal + LB → read replicas → caching → async/queues → sharding → multi-region. Climb only when the current rung is exhausted. Statelessness is what makes horizontal scaling cheap — push session/state to Redis/DB.

## Resiliency

- **Timeouts** on every network call. No timeout = hung threads = cascading failure.
- **Retries** with exponential backoff + jitter, and a cap. Retry only idempotent ops.
- **Circuit breaker**: stop calling a failing dependency, fail fast, probe to recover.
- **Bulkhead**: isolate resource pools so one slow dependency can't drown the rest.
- **Backpressure**: bounded queues; shed or reject load rather than melt.
- **Graceful degradation**: serve stale/partial over nothing.

## Idempotency

Make retries safe: idempotency keys, dedup tables, or naturally idempotent operations (PUT, upsert). Essential for payments, webhooks, and any at-least-once delivery.

## Unique IDs at scale

Auto-increment doesn't distribute. Options: UUIDv4 (random, index-unfriendly), UUIDv7/ULID (time-sortable), Snowflake (timestamp + machine + sequence). Prefer time-sortable IDs so they index well.

## Failure detection

Heartbeats + timeouts, gossip for large clusters. Health checks feed the LB. Design for partial failure as normal, not exceptional.

## Config & delivery

- **12-factor**: config in env, stateless processes, logs as streams, dev/prod parity, disposable processes.
- **IaC** (Terraform/Crossplane): infra in version control, reviewed, repeatable. Immutable infra over hand-patched servers.

## Distributed data hazards

Dual writes drift (use outbox/CDC). Distributed locks are a smell — prefer idempotency or single-writer ownership; if you must, use a fenced lock (Redis Redlock has caveats). Clocks aren't synchronized — don't order events by wall clock across nodes; use logical clocks or a sequencer.

## Tradeoffs to always name

Consistency vs availability vs latency; cost vs redundancy; simplicity vs flexibility; strong vs eventual consistency; sync vs async. A design without a stated tradeoff is a design that hasn't been reasoned about.
