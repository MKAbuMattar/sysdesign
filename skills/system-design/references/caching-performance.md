# Caching & Performance

## Latency budget (know these orders of magnitude)

Memory read ~100 ns · SSD read ~100 µs · same-DC round trip ~0.5 ms · disk seek ~10 ms · cross-continent round trip ~150 ms. Every hop you remove is worth more than micro-optimizing one.

## Cache strategies

- **Cache-aside (lazy)**: app reads cache, on miss loads DB and populates. Most common. Risk: stale data, thundering herd on cold key.
- **Read-through**: cache library loads on miss. Same shape, hidden behind the cache.
- **Write-through**: write cache + DB together. Consistent, slower writes.
- **Write-behind**: write cache, flush to DB async. Fast, risks loss on crash.

Pick by read/write ratio and staleness tolerance.

## Eviction

LRU (default mental model), LFU (frequency), FIFO, TTL. Always set a TTL — unbounded caches become correctness bugs.

## Failure modes

- **Stampede / thundering herd**: many misses hit DB at once. Fix: request coalescing (single-flight), staggered TTLs, early recompute.
- **Cache penetration**: queries for keys that don't exist bypass cache. Fix: cache negatives, bloom filter.
- **Big keys / hot keys**: one huge or one very hot key stalls the node. Split, replicate, or shard the key.
- **Avalanche**: many keys expire simultaneously. Fix: jittered TTLs.

## CDN

Push static (and cacheable dynamic) content to edge nodes near users. Cuts latency and origin load. Cache-control headers and invalidation strategy matter more than the vendor.

## Redis

Single-threaded event loop, in-memory, so it's fast — but that means one slow command (big `KEYS`, big value) blocks everything. Persistence: RDB snapshots (fast restart, can lose recent writes) vs AOF (durable, larger/slower). Use it for cache, sessions, rate limiting, leaderboards, locks, lightweight queues — not as your primary store unless loss is acceptable.

**Memcached vs Redis**: Memcached is a simpler multithreaded pure KV cache; Redis adds data structures, persistence, pub/sub, and Lua scripting. Reach for Memcached only when you want nothing but a fast cache.

## Order of attack for "it's slow"

Measure first. Then: reduce round trips → add/tune indexes → cache the hot path → read replicas → precompute/denormalize → shard. Don't shard before you've indexed.
