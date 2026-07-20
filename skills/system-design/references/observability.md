# Observability

> **Ask first** (`AskUserQuestion`, options + "Other"): the stack (managed SaaS · self-hosted Prometheus/Grafana + Loki/Tempo · cloud-native), the availability target the SLOs must encode, and on-call maturity (who gets paged, is there a rotation). These set how much observability to build and where.

## SLOs, SLIs, error budgets

- **SLI**: the measurement (p95 latency, error rate, availability of a specific endpoint).
- **SLO**: the target on that measurement, over a window ("99.95% of checkout requests succeed, 30 days").
- **Error budget**: 100% minus the SLO. It is permission to ship: budget left means deploy; budget burned means freeze features and fix reliability. Without the budget, "be more reliable" and "ship faster" argue forever.

| Target | Downtime budget / month | What it buys |
|--------|------------------------|--------------|
| 99.9% | ~43.8 min | single region, restart-and-retry ops |
| 99.95% | ~21.9 min | needs automated failover, on-call that reacts in minutes |
| 99.99% | ~4.4 min | multi-zone/region, no human in the recovery path |

Pick the loosest target the business tolerates: each nine multiplies cost and ops maturity, and a public 99.99% with a 15-minute manual failover is fiction.

## The three pillars and what they cost

- **Metrics** (Prometheus, Cloud Monitoring): cheap to query, the alerting backbone. The cost is **cardinality**: a label like `user_id` explodes one series into millions. Label by dimension you would actually alert on (service, endpoint, region), never by entity.
- **Logs** (Loki, ELK, cloud logging): the forensic record. Cost scales with volume × retention: structured JSON, sampled debug logs, and tiered retention (hot 7–30 days, archive after) keep the bill sane.
- **Traces** (OpenTelemetry): the only pillar that follows one request across services: where the 800 ms actually went. Cost control is **sampling**: keep 1–10% of normal traffic, 100% of errors and slow requests (tail-based sampling).

Observability commonly runs 10–30% of the infra bill. Decide what you will pay for before the first incident, not during it.

## RED and USE

- **RED** (request-side, per service): **R**ate, **E**rrors, **D**uration. The dashboard for anything that serves requests.
- **USE** (resource-side, per node/pool): **U**tilization, **S**aturation, **E**rrors. The dashboard for CPUs, disks, queues, connection pools.

Instrument RED first: users feel requests, not CPUs.

## Alerting philosophy

- **Page on symptoms users feel**: SLO burn rate, error rate, p95 latency, saturation about to hit a limit. A page means "a human must act now."
- **Ticket the causes**: disk 70% full, certificate expiring, replica lag creeping. Real, not urgent.
- Every page links a **runbook**: what the alert means, the first three checks, the rollback. A page without a runbook at 3am is just fear.
- **Alert fatigue is an outage risk**: every ignored page trains on-call to ignore the real one. Delete or demote any alert that fires without action twice.

## Dashboards and runbooks

One overview dashboard per service (RED + saturation + deploy markers), one per critical flow (checkout, signup). Runbooks live next to the code, reviewed when the alert changes. Test the pager path: a silent integration fails exactly once, during the incident.

See `devops-k8s.md` for the CI/CD and platform context these attach to, and `distributed-systems.md` for the failure patterns the alerts are watching for.
