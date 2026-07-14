# AI/ML Systems

## Data pipeline

The path is ingest → clean/transform → feature store → train → serve. The feature store is the seam that matters: it holds computed features once so training and serving read the same definition. Skip it and training-serving skew creeps in — the model learns on features computed differently from how they're computed live, and offline accuracy lies.

- **Batch pipeline**: recompute features on a schedule (hourly/nightly). Simple, cheap, replayable. Cost: features are stale between runs.
- **Streaming pipeline**: compute features on events as they arrive (Kafka/Flink). Fresh to the second. Cost: harder to reason about, no easy replay, more ops.

Reach for batch by default; add a streaming path only for features where freshness changes the prediction (fraud, ranking, live recommendations).

## Training vs inference

Two different systems that happen to share a model artifact. Training is throughput-bound, runs offline, tolerates hours of latency, and wants big GPUs saturated. Inference is latency-bound, runs online, and is measured in milliseconds per request. Don't co-locate them: training will starve your serving GPUs of memory at the worst time.

- **Online inference**: real-time, one request → one prediction, tight latency budget (10–200 ms). Powers user-facing features.
- **Batch inference**: score millions of rows on a schedule, latency irrelevant, maximize GPU utilization. Powers precomputed recommendations, nightly scoring.

## Request batching on GPUs

A GPU idles waiting on one request and saturates on many. Batch concurrent requests into one forward pass: throughput climbs 5–20x, per-request latency rises by the wait window. Dynamic batching (wait up to N ms or until B requests, whichever first) is the standard knob. The tradeoff is explicit: a larger batch window buys throughput and cheaper tokens, and spends tail latency. Size the window against your p99 budget, not your average.

## Serving

- **Autoscaling**: GPU instances are 10–40x the cost of CPU boxes and slow to start (model load + warmup = tens of seconds). Scale on queue depth or batch-fill, not CPU%. Keep a warm floor so a cold start never sits in a user's request path.
- **Caching**: cache full responses for repeated prompts, and cache embeddings — recomputing an embedding for the same text is wasted GPU. A semantic cache (match on embedding similarity) catches near-duplicate queries at the risk of a wrong-but-close hit.
- **Latency budget**: set it per request and subtract downstream: retrieval + prompt assembly + model + validation must sum under it. LLM generation dominates and scales with output tokens, so cap max tokens.
- **Cost**: a first-class constraint, not an afterthought. GPU-seconds and per-token spend belong in the design next to latency. Bigger model = better quality and more cost and more latency; the smallest model that passes eval wins.

## Vector search

Embed text/images into vectors, store them in a vector DB, and query by nearest neighbor to find semantically similar items. Exact nearest neighbor is O(n) per query and dies past a few hundred thousand vectors. Approximate nearest neighbor (ANN) trades exactness for speed.

- **HNSW**: a navigable graph index, the default ANN. Sub-millisecond search over millions of vectors. Cost: high memory (the graph lives in RAM) and slow rebuilds on heavy writes.

The core tradeoff is recall vs latency: tuning the index toward higher recall (finding the true top-k) costs more search time and memory. Pick a recall target (say 0.95) and tune to the latency floor that holds it — 100% recall means you shouldn't be using ANN.

## LLM application architecture

The model is one component; the system around it does the work.

- **Orchestration layer**: assembles the prompt, calls the model, parses output, chains steps or tools. Own the prompt as versioned config, not a hardcoded string.
- **RAG (retrieval-augmented generation)**: retrieve relevant context (usually via vector search) and inject it into the prompt so the model answers from grounded facts, not memory. Cuts hallucination and lets you cite sources. Cost: retrieval quality caps answer quality — bad chunks in, bad answer out — and every retrieved token is latency and money.
- **Guardrails/validation**: check inputs (injection, PII) and outputs (schema, safety, groundedness) before anything reaches the user. Untrusted model output is untrusted input to the next system.
- **Evaluation**: an eval set with graded outputs is the only way to know a prompt or model change helped. Ship the eval harness before the feature; a change with no eval is a guess.

The budget is tokens: every retrieved chunk, instruction, and generated word costs latency and money. Trim context to what earns its place.

## RAG vs fine-tuning

| Need | Reach for |
| --- | --- |
| Factual freshness, changing data | RAG (swap the index, no retrain) |
| Citations / provenance | RAG (you control the sources) |
| Consistent format, tone, or task behavior | Fine-tune (bake it into weights) |
| Narrow domain skill, no context room to spare | Fine-tune (shorter prompts, lower per-call cost) |
| Cheap high-volume classification | Small fine-tuned or classic model, not an LLM call |
| Fast iteration, small team | RAG (edit data, not training runs) |

RAG changes what the model knows; fine-tuning changes how it behaves. They compose: fine-tune for format, RAG for facts. Fine-tuning's cost is a training pipeline, versioned datasets, and a stale model the day your data changes.

## MLOps

- **Versioning**: version the model, the training data, and the code together. A prediction you can't reproduce is a bug you can't fix. Data version + code version + config = one reproducible run.
- **Model registry**: the promotion path (staging → prod) with lineage, metrics, and one-click rollback. Deploy from the registry, never from a laptop.
- **Monitoring**: watch data drift (input distribution moves from training), model drift/decay (quality falls as the world changes), and quality regressions (a new version scores worse on eval). Models rot silently: accuracy degrades with no error in the logs, so alert on prediction distributions and eval scores, not just 500s.

## Tradeoffs to always name

RAG (fresh, citable) vs fine-tune (consistent behavior, cheaper per call); batch throughput vs real-time latency; bigger model quality vs cost and latency; ANN recall vs speed and memory; caching freshness vs GPU spend. An ML design that names no cost is a demo, not a system.
