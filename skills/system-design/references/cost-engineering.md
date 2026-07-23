# Cost Engineering

> **Ask first** (`AskUserQuestion`, options + "Other"): pricing posture (on-demand · committed/reserved · spot · self-hosted), what the budget looks like (hard monthly cap vs unit-economics target), and what you suspect dominates the bill (compute · egress · storage · managed premiums). These decide which levers matter.

## The dominant-line-item method

Cloud bills follow a power law: one or two lines dominate, the rest is noise. Rank the bill, name the dominant line, and aim every optimization at it; a 10% cut there beats deleting everything else. A media-heavy marketplace's bill is CDN egress; an ML platform's is GPU-hours; a log-happy SaaS's is often the logging vendor. Optimizing a non-dominant line is effort spent on noise.

## Unit economics

Absolute spend is meaningless without a denominator. Divide the bill by the thing the business sells:

- **Cost per request**: infra $ / requests served. A 10M-request/day API at $30k/mo runs ~$0.0001/request; know your number.
- **Cost per active user**: the SaaS survival metric; it must sit far below revenue per user.
- **Cost per GB delivered/stored**: the metric for media and data platforms.

Watch the trend, not the total: spend growing linearly with users is healthy; spend growing faster than users is a design problem surfacing in finance.

## Egress: the silent dominant

Data into a cloud is free; data out is not, and it hides in three places:

| Path | Order of magnitude | Trap |
|------|--------------------|------|
| Internet egress | ~$0.05-0.12/GB | media/video sites: this is the bill |
| Cross-region | ~$0.02-0.08/GB | replication and multi-region chatter |
| Cross-AZ | ~$0.01-0.02/GB, both directions | chatty microservices pay it twice per hop |

Levers: CDN offload (>90% hit ratio moves the bill to cheaper CDN rates), compress and resize before the wire (AVIF/WebP cut image egress 30-70%), keep chatty service pairs in one AZ and accept the blast-radius tradeoff knowingly.

## Storage tiers

Object storage prices by access pattern: hot ~$0.02/GB-mo, infrequent ~$0.01, archive ~$0.001-0.004. The trap is the **retrieval cost**: archive tiers charge per GB restored and per request, so archiving data you re-read monthly costs more than leaving it hot. Lifecycle rules (hot → infrequent at 30 days, archive at 90+) are one config block and routinely cut storage bills 50%+ for append-mostly data.

## Commitment discounts

- **Committed use / savings plans / reserved**: 30-60% off for a 1-3 year spend promise. Commit the baseline you're certain of, never the peak.
- **Spot / preemptible**: 60-90% off, reclaimable at minutes' notice. For stateless, checkpointable work (CI, batch, transcode) only; the discount is payment for interruption tolerance.
- **The cost**: flexibility. A committed instance family you migrate off is money burned; commit late, after the architecture settles.

## The managed premium

Managed services (managed Postgres, K8s control planes, hosted search) run 20-50%+ over self-hosting the same hardware. On a small team the premium is usually the cheap option: it buys patching, failover, backups, and on-call sleep, and one engineer's month costs more than a year of the premium. Self-host when the service is your core competence or the scale makes the premium exceed a headcount.

## Cost as a design input

Treat cost like latency: budget it per component in the plan (the plan template's cost table), tag every resource to a service/team, alert on spend anomalies the way you alert on error rates. Design choices that flip on cost alone: single-AZ vs multi-AZ chatter, fan-out breadth, log verbosity and retention, image quality tiers, per-tenant quotas. A design that ignores its bill gets redesigned by the CFO; see `observability.md` for the telemetry that catches the trend early.
