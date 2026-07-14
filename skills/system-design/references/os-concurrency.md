# OS & Concurrency

## Process vs thread

- **Process**: own address space, isolated. A crash or memory corruption stays contained. Communication goes through IPC (pipes, sockets, shared memory) — expensive to set up.
- **Thread**: shares the parent's heap and file descriptors. Cheap to spawn, fast to communicate (just read shared memory), but one bad pointer corrupts the whole process.
- **Context-switch cost**: thread switch is ~1–5 µs; process switch adds TLB/cache flush overhead on top. Both dwarf a function call (~1 ns).

Reach for processes when isolation matters more than speed (a plugin sandbox, a crash-prone worker). Reach for threads when tasks must share state cheaply. Tradeoff: isolation buys fault containment and pays in IPC latency.

## Concurrency vs parallelism

- **Concurrency**: structuring a program to handle many tasks that overlap in time. One core interleaving 10k connections is concurrent, not parallel.
- **Parallelism**: actually executing multiple tasks at the same instant, which needs multiple cores.

Concurrency is a design property; parallelism is a runtime property. A single-threaded event loop is highly concurrent with zero parallelism. You want concurrency to stay responsive under load, parallelism to finish CPU work faster.

## Blocking vs non-blocking, sync vs async

- **Blocking I/O**: the calling thread parks until the read/write completes. Simple to reason about; each in-flight request costs a thread (~1 MB stack + scheduler slot).
- **Non-blocking I/O**: the call returns immediately; readiness arrives via `epoll`/`kqueue`/`io_uring`. One thread multiplexes thousands of sockets.
- **Sync vs async**: whether your code waits for the result inline or registers a callback/future.

| Workload | Reach for |
| --- | --- |
| Many idle connections, little CPU per request (chat, proxy, gateway) | Event loop, one thread per core |
| Heavy CPU per request, moderate concurrency | Thread-per-request + a pool |
| Mixed | Async I/O with a worker pool for the CPU-bound parts |

Event loop wins on memory and connection count: 100k idle sockets on one thread beats 100k blocked threads. The cost is that any blocking call or long CPU burst on the loop thread stalls *every* connection — you must offload CPU work and never call blocking APIs on the loop. Thread-per-request wins on simplicity and isolates a slow request to its own thread; it caps out where thread count exhausts memory or the scheduler (~10k threads).

## Locks and hazards

- **Race condition**: correctness depends on timing between threads touching shared state. The bug that passes 999 runs and fails in production.
- **Mutex**: mutual exclusion around a critical section. Held too long, it serializes everything behind it.
- **Deadlock (four Coffman conditions, all required)**: mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one — global lock ordering kills circular wait cheaply.
- **Lock granularity**: coarse locks are easy and contended; fine-grained locks scale but multiply deadlock and correctness risk. Tradeoff: contention vs complexity.

Prefer designs that avoid locks: immutability (nothing to protect), single-writer ownership (one thread owns the data, others message it), or lock-free structures (CAS-based, hard to get right). Reach for a mutex only when shared mutable state is unavoidable.

## Thread pools and bounded queues

Fix the thread count near core count for CPU-bound work; size it higher for I/O-bound work where threads mostly wait. Feed the pool through a **bounded** queue: an unbounded queue hides overload until it OOMs. When the queue fills, block or reject — that rejection is backpressure (see distributed-systems.md).

## Virtual memory

- **Paging**: address space split into fixed 4 KB pages mapped to physical frames on demand. The dominant model; enables per-page protection and swap.
- **Segmentation**: variable-size logical regions (code, stack, heap). Mostly historical; paging won.
- **Page fault**: accessing an unmapped page traps to the kernel. A minor fault remaps cheaply; a major fault hits disk (~1–10 ms) and can quietly turn a fast function into a slow one under memory pressure.

## Garbage collection

- **Generational GC**: most objects die young, so collect the young generation often and cheaply, the old generation rarely. Cuts total work.
- **Throughput vs pause time**: a throughput collector maximizes app work per second and tolerates longer pauses; a low-latency collector (ZGC, Shenandoah, Go's concurrent GC) keeps pauses sub-millisecond by doing more concurrent work, costing CPU and headroom.
- **Stop-the-world**: phases that freeze all app threads. Fine for a batch job; a 200 ms STW pause blows a p99 latency SLA and looks like a network blip.

GC buys memory safety and no manual `free`; it costs pause latency and CPU. When p99 tail latency is the product, tune for pause time or move hot paths off the heap.

## Memory hierarchy

Register (<1 ns) → L1/L2 cache (~1–10 ns) → RAM (~100 ns) → SSD (~100 µs) → disk seek (~10 ms). Each rung is roughly 10–100× slower and larger. Keep hot data high; a cache miss to RAM costs ~100 instructions of stall (latency numbers — see caching-performance.md).
