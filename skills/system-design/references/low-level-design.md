# Low-Level Design (OOP & Machine Coding)

> **Ask first** (`AskUserQuestion`, options + "Other"): the setting (LLD interview / machine-coding round · designing real production classes), the language (Java · Python · TypeScript · Go — idioms differ), and the problem family (stateful machine · booking/inventory · game · cache/infra component). These pick the patterns and the depth.

## HLD vs LLD

High-level design places boxes (services, stores, queues); low-level design fills one box: the classes, interfaces, and state inside a component. The rest of this skill is HLD; this file is the class-level sibling. The failure mode differs too: HLD fails by picking the wrong component, LLD fails by coupling the right ones so tightly nothing can change.

## SOLID, and the smell each prevents

- **S — Single responsibility**: one reason to change per class. Smell: a `Manager`/`Utils` class that edits for every feature.
- **O — Open/closed**: extend behavior by adding types, not editing switch statements. Smell: the same `switch(type)` growing in five places.
- **L — Liskov substitution**: a subtype must honor the parent's contract. Smell: overrides that throw `NotImplemented` (the square-extends-rectangle trap).
- **I — Interface segregation**: many narrow interfaces over one fat one. Smell: implementers stubbing methods they never use.
- **D — Dependency inversion**: depend on abstractions; inject them. Smell: `new Database()` inside business logic, untestable without a live DB.

Companions: **DRY** (extract the third copy, not the second), **KISS** (the simple design that works beats the flexible one that might), **YAGNI** (no speculative extension points; delete "for later" code).

## Class relationships

- **Association**: A uses B ("driver has a license"). The weakest link; a reference.
- **Aggregation**: A holds Bs that outlive A ("garage holds cars"). Shared lifetime not implied.
- **Composition**: A owns Bs that die with A ("order owns line items"). Strongest; model invariants here.
- **Dependency**: A takes B as a parameter or local. Cheapest to change.

The reflex rule: **composition over inheritance**. Inherit only for a true is-a with a stable contract; otherwise wrap. Deep hierarchies are where LLD interviews go to die.

## Design patterns: the catalog

`architecture-patterns.md` names the reflex ones at architecture level; this is the class-level menu. Reach for a pattern to remove a specific pain, never to decorate.

| Need | Reach for |
|------|-----------|
| Swap an algorithm at runtime (pricing, routing) | Strategy |
| Object changes behavior by mode (order status, elevator) | State |
| Notify many dependents on change | Observer |
| Build a complex object step by step | Builder |
| One place decides which concrete type to create | Factory Method / Abstract Factory |
| Add features in layers (coffee add-ons, IO streams) | Decorator |
| Make an incompatible interface fit | Adapter |
| One shared instance (config, connection pool) | Singleton: use sparingly; prefer injection |
| Treat part and whole uniformly (folders/files) | Composite |
| Queue, undo, or log operations as objects | Command |
| Pass a request along handlers until one takes it | Chain of Responsibility |
| Control or cache access to an expensive object | Proxy / Flyweight |

## The LLD interview method

1. **Clarify and scope**: 3-4 core use cases, in and out of scope. Multi-floor parking? Payments? Say what you skip.
2. **Entities first**: nouns become classes and enums (`Vehicle`, `Spot`, `SpotSize`, `Ticket`). Enums for closed sets; no strings for states.
3. **Relationships and ownership**: who creates, who holds, what dies together (composition), where the invariants live.
4. **Behavior via patterns and state machines**: map each changing requirement to one pattern; draw the state transitions for anything with a lifecycle.
5. **Walk one flow end to end**, then name concurrency and edge cases (two threads grab the last spot: lock or CAS on the spot, not the lot).

Write skeleton code early (class names, method signatures), talk while filling in, and keep the design extendable exactly where the interviewer's follow-up will land (new vehicle type, new pricing rule).

## Classic problems and the key insight

| Problem | The insight that unlocks it |
|---------|------------------------------|
| Parking lot | Enums for spot/vehicle sizes + Strategy for pricing; assignment logic isolated from the lot |
| Vending / coffee machine | State pattern: Idle → HasMoney → Dispensing; illegal transitions become impossible |
| Elevator system | State machine per car + a scheduler queue deciding which car takes the request |
| LRU cache | HashMap + doubly-linked list: O(1) get and evict; the interview is the pointer surgery |
| Tic-tac-toe / chess | Board owns cells; piece polymorphism for moves; separate move-validation from game loop |
| Pub-sub / logging framework | Observer + per-subscriber queues; log levels as ordered enum, handlers as chain |
| Splitwise | Per-pair balance map + debt simplification; it is a small ledger (see payments.md) |
| Booking (hotel/movie/ticket) | Inventory + reservation with a hold-then-confirm state machine; lock the seat, not the theater |
| ATM / wallet | Command-style transactions with idempotency and a balance invariant checked atomically |
| Rate limiter (class-level) | Token bucket as one class: capacity, refill rate, `tryAcquire`; clock injected for tests |

For thread-safety follow-ups (thread-safe singleton, producer-consumer, reader-writer): the primitives and hazards live in `os-concurrency.md`; the LLD twist is knowing where the lock goes — on the smallest invariant, never around the whole system.
