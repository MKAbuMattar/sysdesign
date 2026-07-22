# Example evolution — order-management monolith, one Postgres, at its limit

A worked `/sysdesign:evolve` output, showing the target depth: brownfield, grounded in the
interview answers, ordered rollback-safe steps with a gating metric each. This is illustrative —
a real run derives every number from the user's own `AskUserQuestion` answers and writes to
`.sysdesign-orderhub/requirements.md` + `EVOLUTION.md` at the repo root.

> **Locked from the interview:** a B2B order-management SaaS. Django monolith, one Postgres
> (db.r6g.xlarge), ~400 tenants, ~600 peak QPS (95% reads), ~150 GB data. Team of 6, one on-call
> rotation. Pain: report queries starve checkout writes at month-end; deploys are all-or-nothing;
> p95 spikes from 180 ms to 2 s. **Can't change:** Django, Postgres, the public API contract.
> **Downtime budget:** zero for checkout, minutes for reports. Risk tolerance: low — revenue path.

## 1. Current state (map before you move)

- **App**: one Django deploy serving web, API, admin, report rendering, and cron jobs. One image, one rollout, ~25 min deploy cycle.
- **Data**: single Postgres primary. OLTP tables (orders, inventory) share the box with reporting aggregates. No replica.
- **Side-effects inline**: order confirmation emails, webhook fan-out to tenant ERPs, and PDF invoices run inside the request cycle (up to 4 s tail).
- **Observability**: request logs and CPU graphs only. No p95-by-endpoint, no slow-query log review, no error budget.

## 2. Forcing function

**Month-end reporting concurrency doubles every quarter and now locks checkout.** The measured
limit: >40 concurrent report queries pushes checkout write p95 past 1 s (SLO: 300 ms). That is
the one problem the evolution must remove. Everything else (deploy speed, inline side-effects)
is real friction but not the trigger — it gets fixed only where it lies on the same path.

## 3. Target state

The same monolith, with the load split by kind rather than the app split by team:

- Reads that tolerate lag (reports, dashboards, exports) go to a **read replica**.
- Side-effects leave the request path via an **outbox table + worker queue**.
- Report rendering runs as its own **deployable worker** (first strangler-fig slice) so its releases and failures stop coupling to checkout.
- Postgres stays the only source of truth. No sharding, no microservice rewrite, no new database — nothing else has hit a limit.

## 4. Migration path (ordered, reversible, gated)

Each step ships alone, has a rollback, and a metric that gates the next step.

| # | Change | Rollback | Gate to proceed |
|---|--------|----------|-----------------|
| 0 | **Instrument first**: p95 by endpoint, slow-query log, replica-lag and queue-depth dashboards, checkout SLO alert | remove dashboards | metrics visible for 1 week; baseline recorded |
| 1 | **Provision a read replica** (async, same AZ class); route nothing yet | drop replica | replication lag p99 < 5 s over 3 days |
| 2 | **Route report/dashboard reads to the replica** behind a per-query router flag (`USING_REPLICA` allowlist, not a code fork) | flip the flag: all reads back to primary | checkout write p95 < 300 ms *during* a month-end run |
| 3 | **Outbox + worker queue** for emails, webhooks, PDFs: write the event in the order transaction, workers consume; idempotency keys on webhook delivery | stop workers, re-enable inline sends (kept behind the same flag for one release) | request p99 drops below 800 ms; zero lost events across a deploy (outbox drained) |
| 4 | **Extract report rendering** as a worker deployment (same codebase, separate process + rollout), reading only the replica | route rendering back into the monolith image | month-end report load causes **no** checkout SLO alert; report deploys no longer roll the web tier |
| 5 | **Retire month-end ritual**: delete the "reporting freeze" runbook, cap replica query timeout, document the new steady state | n/a (docs) | one full month-end with error budget intact |

Strangler order matters: replica before outbox (it removes the forcing function fastest), outbox
before extraction (the worker needs the queue), extraction last (it is the most invasive and by
then the pressure is already off).

## 5. What each step gives up

- **Replica routing**: reports see seconds-stale data. Acceptable — stated in the interview; checkout still reads the primary.
- **Outbox/queue**: emails and webhooks become eventually-delivered (seconds). Buys back 4 s request tails; webhook consumers already retry.
- **Report worker**: two deployables to operate instead of one. The team of 6 accepts one extra rollout in exchange for decoupled failure domains.
- **Not sharding, not splitting services**: write volume (~30/s) is nowhere near Postgres limits; a service split would add network hops and distributed failure modes with no forcing function behind them.

## 6. Non-negotiables through the migration

Validation at the API boundary, no lost order events (outbox is transactional with the order
write), auth untouched, and the new dashboards stay after the migration — they are the gates for
the *next* evolution too.

## 7. Risks and what would change this plan

| Watch this | Current call | Flip to |
|------------|--------------|---------|
| Write QPS approaches ~5–10× today | single primary | partition hottest tables, then shard by tenant |
| Replica lag p99 > 30 s under report load | one replica | second replica dedicated to exports, or aggregate tables |
| Queue backlog grows across a whole day | shared worker pool | per-event-type pools; rate-limit webhook fan-out |
| A second team forms around reports | strangler slice stays in-repo | promote the report worker to a real service with its own store |

Source convention: a real run writes this as `.sysdesign-orderhub/EVOLUTION.md`, with the locked
answers in `requirements.md` beside it.
