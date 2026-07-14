# Data & Storage

## Picking a database

Start with a relational DB (Postgres). Move off it only for a proven reason:

| Signal | Consider |
|--------|----------|
| Rich queries, transactions, relations | Relational (Postgres/MySQL) |
| Huge write throughput, simple access by key | Wide-column (Cassandra) / KV |
| Flexible/nested documents, few relations | Document (MongoDB) |
| Full-text / relevance search | Elasticsearch (as an index, not source of truth) |
| Caching, ephemeral, counters, queues | Redis |
| Time-stamped metrics at scale | Time-series (Prometheus/Influx) |

"Postgres can probably do it" is usually the right first answer.

## Replication

Primary handles writes, replicas serve reads. Async replication = read replicas can lag (stale reads); sync = safer but slower writes. Route reads that tolerate lag to replicas, read-your-writes to primary.

## Sharding

Split data across nodes when one node can't hold it or serve it.
- **Hash sharding**: even spread, hard range queries, resharding is painful → use **consistent hashing** to limit key movement.
- **Range sharding**: good range scans, risks hot shards.
- **Directory/lookup**: flexible, adds a lookup hop + a thing to keep consistent.

Sharding is a one-way door — exhaust vertical scaling and read replicas first.

## Consistency

- **CAP**: under a network partition you choose availability or consistency. Not a menu for normal operation — it's the partition-time behavior.
- **ACID** (relational): atomic, consistent, isolated, durable.
- **Isolation levels**: read uncommitted → read committed → repeatable read → serializable. Higher = fewer anomalies, more locking.
- **Eventual consistency**: replicas converge; design the UX for it (read-your-writes, monotonic reads).

## Messaging & queues

- **Queue** (RabbitMQ, SQS): work distribution, one consumer per message.
- **Log** (Kafka, Pulsar): ordered, replayable, many consumers, retains history.

Kafka is fast because of sequential disk I/O, zero-copy, and batching. Delivery semantics: at-most-once / at-least-once / exactly-once (exactly-once is expensive and usually really "at-least-once + idempotent consumer").

**CDC** (Debezium): stream row changes out of the DB to keep caches/search/warehouses in sync without dual writes.

## Common patterns

Cache-aside, read replica, CQRS (split read/write models), event sourcing (store events, derive state), outbox (atomic DB write + reliable event publish). Reach for these to solve a named problem, not by default.

## Storage engine: B-tree vs LSM-tree

- **B-tree** (Postgres, MySQL/InnoDB): read-optimized, updates in place, great for range scans and mixed workloads. The default.
- **LSM-tree** (Cassandra, RocksDB, Scylla): write-optimized, buffers writes in memory then flushes sorted segments, compacts in the background. Wins on heavy write throughput; pays in read amplification and compaction I/O.

Match the engine to your read/write ratio.
