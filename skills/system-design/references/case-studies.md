# Real-World Case Studies

> **Ask first** (`AskUserQuestion`, options + "Other"): which precedent fits the goal (feed · chat · media · marketplace · geo · payments) and the target scale. That picks which case actually transfers.

Use these as interview talking points and design precedents. What transfers is the *reason* behind each choice, not the specific tech. When you cite one, name the constraint that forced the design.

## Patterns from real systems

- **Netflix**: microservices behind an edge tier, its own CDN (Open Connect) pushing video to ISP-local boxes, and chaos engineering (deliberately killing instances) to prove resilience. Caching sits at every tier as a first-class latency strategy, not an afterthought.
- **Discord**: stores trillions of messages; migrated Cassandra → ScyllaDB when compaction and tail latency became the bottleneck. Lesson: pick the storage engine for your write pattern, and be willing to re-pick.
- **Twitter timeline**: "For You" is precomputed. Fan-out **on write** (push each tweet into follower timelines) gives fast reads but explodes for celebrity accounts; fan-out **on read** (assemble at request time) is cheap to write but slow to read. Real systems do a hybrid: push for most users, pull for mega-accounts.
- **Uber**: geo-indexing (H3 hex grid) for supply/demand matching, dispatch services, and a service mesh to manage thousands of services. Lesson: the domain (geospatial) drives the core data structure.
- **Figma**: scaled Postgres ~100x by horizontal sharding *without leaving Postgres* — proof that "we need a new database" is often really "we haven't sharded yet."
- **Airbnb**: monolith → SOA → microservices, each step driven by team-scaling pain, not fashion. Lesson: architecture follows org structure (Conway's Law).
- **YouTube uploads**: chunked/resumable upload, an async transcode pipeline producing many renditions, then CDN distribution. Lesson: decouple ingest from processing with a queue.
- **Levels.fyi**: scaled to millions on Google Sheets as the backend early on. Lesson: the boring, cheap solution carries you further than you think — optimize when a real limit hits, not before.

## Classic "design X" problems

Pair these with the framework in `interview.md` — clarify, estimate, then design.

- **Google Docs / collaborative editor**: real-time sync via Operational Transform or CRDTs; conflict resolution is the hard part, not storage.
- **Chat (WhatsApp/Messenger/Discord)**: persistent WebSocket connections, presence, message ordering, and delivery guarantees (at-least-once + dedup); fan-out for group chats.
- **Proximity / "nearby" service**: geo-index with a quadtree or geohash; the query is "everything within radius r," which naive lat/long can't index.
- **Search engine**: crawl → build an inverted index → rank; separate the write-heavy indexing path from the read-heavy query path.
- **Notification system**: fan-out to device tokens across channels (push/SMS/email), with retries, rate limits, and user preferences.
- **URL shortener / pastebin / rate limiter**: the warm-ups: unique ID generation, KV storage, cache-first reads, token/leaky bucket.

Source & inspiration: ByteByteGo *System Design 101*.