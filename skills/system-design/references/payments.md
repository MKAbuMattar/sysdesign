# Payments & Fintech

## Players & flow

A card charge crosses five parties before money moves. Know each hop and where it can fail.

- **Cardholder**: presents a card (or token) to pay.
- **Merchant**: your system, initiating the charge.
- **PSP/gateway**: the API you integrate (Stripe, Adyen, Braintree). Handles tokenization, routing, retries.
- **Acquirer**: the merchant's bank; owns the merchant account and takes on card-network risk.
- **Card network**: Visa/Mastercard rails that route the message to the issuer.
- **Issuer**: the cardholder's bank; approves or declines against balance and fraud rules.

The lifecycle splits into distinct phases, and conflating them is the classic bug:

- **Authorization**: issuer places a hold, confirms funds. No money moves. Holds expire (5–7 days).
- **Capture**: merchant claims the authorized amount. Often deferred until fulfillment (ship-then-capture). Can capture less than authorized, rarely more.
- **Clearing**: network exchanges transaction records between acquirer and issuer, computes net positions.
- **Settlement**: actual funds transfer, T+1 to T+2. This is when you truly have the money.

Tradeoff: **auth-and-capture together** is one API call and simplest, but you charge before you can fulfill. **Auth-then-capture** matches money to delivery and cuts refund volume, at the cost of expiring holds and a second failure point.

## Money representation

- **Integer minor units**: store `1050` cents, never `10.50` dollars. Floats can't represent `0.10` exactly: `0.1 + 0.2 != 0.3`, and rounding drift compounds across a ledger.
- **Currency + scale**: an amount is meaningless without its currency. Store `{ amount: 1050, currency: "USD" }`. Scale differs: USD has 2 decimals, JPY has 0, BHD has 3. Encode the scale per currency, don't hardcode 100.
- **Rounding**: define the rule once (banker's rounding / round-half-even avoids upward bias). Round only at the boundary where you must emit a real charge; keep full precision internally for splits, fees, and FX.
- **Big decimals for FX/interest**: multiplication and division (currency conversion, APR) need arbitrary precision, then round to minor units at the end.

## Idempotency

At-least-once delivery is the network's promise; exactly-once is what you build on top with dedup.

- **Idempotency key** on every charge, refund, and transfer: a client-generated unique ID (UUIDv7). The server stores key → result. A retry with the same key returns the stored result instead of charging again.
- **Why retries double-charge without it**: the first request succeeds but the response is lost to a timeout. The client retries. Without a key the processor sees two distinct charges. With a key it recognizes the replay.
- **Scope and TTL**: key is unique per operation, not per session. Persist the key before calling the processor (write-ahead), so a crash mid-call still dedups. Keep keys 24h+ to outlast retry windows.

Tradeoff: idempotency needs a durable dedup store on the hot path, adding a write and a read to every payment. Cheap next to reconciling a double-charge with an angry customer.

## Ledger & reconciliation

- **Double-entry, append-only**: every movement is balanced entries where debits equal credits. Never UPDATE a balance; INSERT an entry and derive balance as the sum. This makes the ledger immutable and auditable — you can replay history and prove any balance.
- **Corrections are new entries**: a mistake is fixed by a reversing entry, never by editing the past. The audit trail stays intact.
- **Reconciliation**: match your internal ledger against the processor's settlement report daily. Flag entries present in one and not the other (missing capture, unexpected refund, fee drift). Unmatched rows are money leaking or a bug.
- **Idempotent event ingestion**: processor reports and webhooks arrive more than once; dedup on the processor's transaction ID before posting to the ledger.

## Consistency & hot accounts

Money demands strong consistency: no dirty reads, no lost updates. Two transactions must not both spend the same balance. This rules out eventual consistency on the balance itself.

- **Hot-account problem**: a platform's fee account or a popular merchant's row gets updated by thousands of concurrent transactions. Row-level locks serialize them, and throughput collapses to one txn at a time on that row.
- **Mitigations**: shard a hot balance into N sub-accounts and route writes across them (sum for the true balance); batch many small postings into one periodic entry; queue per account so one writer owns each account and processes its stream serially.

Tradeoff: strong consistency vs throughput. Per-account serialization guarantees correctness but caps write rate; sharding a balance restores throughput at the cost of a scatter-gather read to total it.

## Async choreography

Payments span services and external banks, so most steps are async. Coordinate with events, not one giant transaction.

- **Webhooks**: the processor calls you back when an async event settles (payment succeeded, dispute opened). Verify the signature (HMAC) on every callback, return 2xx fast, process off the request thread. Assume redelivery: make handlers idempotent.
- **Saga / compensation**: a multi-step payment (reserve funds → charge → allocate → notify) has no distributed transaction. Model it as a saga: each step has a compensating action (release the reservation, issue a refund) that undoes it on downstream failure.
- **Outbox**: to publish a "payment captured" event exactly when the ledger commits, write the event to an outbox table in the same DB transaction, then relay it. Avoids the dual-write drift of committing the row and separately publishing (outbox/CDC — see data-storage.md).

Tradeoff: sync authorization gives the buyer an instant yes/no at checkout; async settlement is the only honest model for the money actually moving. Present the auth result live, reconcile settlement in the background.

## Security & compliance

- **PCI DSS scope**: touching a raw card number (PAN) puts your systems in scope for costly audits. Minimize scope: never let the PAN reach your servers.
- **Tokenization**: the gateway swaps the PAN for a token you store and reuse for future charges. You keep a durable payment handle; the sensitive number lives in the processor's vault.
- **3-D Secure / SCA**: an issuer-side challenge (biometrics, OTP) that shifts fraud liability to the issuer and satisfies Strong Customer Authentication rules in the EU. Adds a checkout step and some conversion drop.
- **Encryption**: TLS in transit, encryption at rest for any stored token or PII (see security-auth.md).

Tradeoff: storing cards yourself gives control and portability across processors but inherits full PCI scope and breach liability; tokenization offloads both at the cost of coupling to the processor's vault and token format.
