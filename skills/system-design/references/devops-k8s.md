# DevOps & Kubernetes

## Kubernetes service types

- **ClusterIP**: internal-only, default. Service-to-service.
- **NodePort**: opens a port on every node. Rarely used directly; debugging/on-prem.
- **LoadBalancer**: provisions a cloud LB. One external entry per service (costly if many).
- **Ingress** (not a Service type, but the answer): L7 routing, TLS, host/path rules — the normal edge for HTTP. Gateway API is the successor.

## Deployment strategies

- **Rolling** (default): replace pods gradually. Zero-downtime, slow rollback.
- **Blue-green**: two full environments, flip traffic. Instant rollback, double the resources.
- **Canary**: send a small % to the new version, watch metrics, ramp. Best risk control, needs good observability + traffic splitting.
- **Recreate**: kill all, start new. Downtime; only for things that can't run two versions.

## Core K8s patterns

Sidecar (helper container: proxy, log shipper), init container (setup before main), operator (encode ops knowledge as a controller), and health probes: **liveness** (restart if dead), **readiness** (pull from LB until ready), **startup** (grace for slow boots). Set resource requests/limits or the scheduler and OOM killer will surprise you.

## Docker best practices

Small base (distroless/Alpine/Wolfi), multi-stage builds, non-root user, pinned versions, `.dockerignore`, one process per container, layer caching (copy deps manifest before source). Scan images for CVEs in CI and fail the build on criticals. Don't bake secrets into layers.

## CI/CD

CI: build → test → scan → sign → push artifact. CD: deploy via GitOps (ArgoCD/Flux) — Git is the source of truth, the cluster reconciles to it. Separate app repos from infra/Helm repos; branch- or overlay-per-environment. Keep pipelines fast and deterministic; artifacts immutable and promoted, not rebuilt per env.

## Observability

Three pillars: **metrics** (Prometheus/Grafana — rates, saturation, errors), **logs** (structured, shipped to a store — ELK/Loki), **traces** (OpenTelemetry — follow a request across services). Alert on symptoms users feel (latency, error rate, saturation — the RED/USE methods), not on every internal blip. SLOs and error budgets keep alerting honest.

## DevOps vs SRE vs Platform Engineering

DevOps = culture/practice bridging dev and ops. SRE = ops as an engineering discipline with SLOs and error budgets. Platform engineering = build the internal platform/paved road so product teams self-serve. Overlapping, not competing.
