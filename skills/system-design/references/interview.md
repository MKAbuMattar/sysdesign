# System Design Interview

## Answer framework (don't skip step 1)

1. **Clarify & scope** (5 min). Functional requirements, non-functional (scale, latency, consistency, availability), and what's out of scope. Get the interviewer to agree before designing.
2. **Estimate** (back-of-envelope). QPS, storage/day, bandwidth, read:write ratio. Round hard. This drives every later choice.
3. **API + data model.** Define the handful of endpoints and the core entities/schema.
4. **High-level design.** Boxes and arrows: clients → LB/gateway → services → data + cache + queue. Get a working baseline before optimizing.
5. **Deep dive.** Interviewer picks (or you propose) 1-2 components to detail: the DB choice, the hot path, the tricky consistency point.
6. **Scale & harden.** Now bring in caching, sharding, replication, CDN, async, failure handling — each tied to a number from step 2.
7. **Tradeoffs & wrap.** State what you optimized for and what you'd revisit.

Talk continuously, drive the session, treat it as collaboration.

## Numbers worth memorizing

1 day ≈ 86,400 s (~10^5). 1M writes/day ≈ 12/s avg, but peak is multiples. 1 char ≈ 1 byte, 1 KB row × 1M/day ≈ 1 GB/day ≈ ~365 GB/yr. Memory ns, SSD µs, same-DC ms, cross-continent ~150 ms.

## Building blocks to have ready

Load balancer, reverse proxy/gateway, cache (aside + CDN), SQL vs NoSQL choice + sharding + replication, message queue vs log, rate limiter, unique ID generator, blob storage + CDN for media, search index, pub/sub for fan-out.

## Algorithms/structures that come up

Consistent hashing (sharding, LB), quadtree/geohash (proximity/maps), bloom filter (dedup/penetration), trie (autocomplete), leaky/token bucket (rate limiting), merkle tree (sync/anti-entropy), LSM-tree vs B-tree (write-heavy vs read-heavy storage), HLL (approx counting).

## Classic problems

URL shortener, pastebin, rate limiter, news feed, chat (WhatsApp), typeahead, YouTube/Netflix (upload + CDN + transcode), Uber/maps (geo-index), Twitter timeline (fan-out on write vs read), notification system, distributed job scheduler, key-value store, payment system (idempotency + reconciliation).

## Tradeoff checklist to voice

Consistency vs availability · strong vs eventual · SQL vs NoSQL · normalization vs denormalization · sync vs async · fan-out on write vs read · latency vs throughput · cost vs redundancy · build vs buy. Naming the tradeoff is the signal they're grading.

## Common failures

Designing before clarifying, skipping estimates, jumping to microservices, ignoring failure/edge cases, no bottleneck analysis, going silent. A simple correct design beats a clever hand-wavy one.
