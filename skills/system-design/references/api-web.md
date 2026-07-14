# API & Web

## Protocol / style choice

| Need | Reach for |
|------|-----------|
| Simple CRUD, cacheable, broad client support | REST |
| Client picks exact fields, many nested resources, one round trip | GraphQL |
| Low-latency service-to-service, streaming, strict contracts | gRPC |
| Fire-and-forget events between services | message queue, not a sync API |

REST is the default. Move off it only when a concrete pain (over-fetching, chatty round trips, streaming) justifies the cost. GraphQL shifts complexity to the server (N+1, query cost limits, caching is harder). gRPC needs HTTP/2 and isn't browser-native without a proxy.

## Middle boxes — don't conflate them

- **Reverse proxy**: terminates TLS, hides backends, serves cache/static. (nginx)
- **Load balancer**: spreads traffic across instances (L4 = transport, L7 = HTTP-aware).
- **API gateway**: L7 entry point that also does auth, rate limiting, routing, request shaping. A gateway usually *contains* LB + reverse-proxy behavior.

Rule: one gateway at the edge, LBs behind it per service tier.

## Client update patterns

- **Short polling**: client asks on a timer. Simple, wasteful, laggy.
- **Long polling**: server holds the request until data or timeout. Better, still one message per cycle.
- **SSE**: server → client stream over one HTTP connection. Great for feeds/notifications; unidirectional.
- **WebSocket**: full-duplex. Use for chat, collab, live cursors. Costs a persistent connection and stateful infra.

Escalate only as far as the use case needs. Most "real-time" needs are SSE, not WebSocket.

## HTTP versions

HTTP/1.1 = one request per connection (head-of-line blocking). HTTP/2 = multiplexed streams over one TCP connection (still TCP HOL blocking). HTTP/3 = QUIC over UDP, removes transport HOL blocking, faster on lossy networks.

## API design essentials

- Version from day one (`/v1`), plan deprecation.
- **Pagination**: cursor-based for large/changing sets, offset only for small stable ones.
- Idempotency keys on POSTs that can be retried (payments especially).
- Consistent error envelope; use real status codes.
- Rate limit and authenticate at the edge.

## Security checklist

Auth (who) vs authz (what they can do) — both. TLS everywhere. Validate/normalize input at the boundary. Never trust client-supplied IDs for access decisions. Scope tokens, short TTLs, rotate secrets. See `security-auth.md`.

## Networking basics (interview-adjacent)

OSI model, top to bottom: application → presentation → session → transport (TCP/UDP) → network (IP) → data link → physical. In practice you reason at L4 and L7. TCP = reliable, ordered, connection-based; UDP = fire-and-forget, lower latency (DNS, gaming, live video). DNS resolves a name to an IP by walking resolver → root → TLD → authoritative, cached at each hop by TTL. Ports worth knowing: 80/443 HTTP(S), 22 SSH, 53 DNS, 5432 Postgres, 6379 Redis, 27017 Mongo.
