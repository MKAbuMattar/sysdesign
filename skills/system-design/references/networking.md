# Networking

## OSI model, and where you actually reason

Seven layers, top to bottom: Application, Presentation, Session, Transport, Network, Data Link, Physical. Memorize the names for interviews; in practice you design at three. **L3 (IP)**: addressing and routing between hosts. **L4 (TCP/UDP)**: ports, reliability, flow control. **L7 (HTTP/gRPC)**: the payload your service speaks. A load balancer is "L4" or "L7" depending on whether it routes by IP:port or by URL path — that one distinction decides whether it can do content-based routing.

## TCP vs UDP

TCP is a reliable, ordered, connection-oriented byte stream: 3-way handshake (SYN → SYN-ACK → ACK) sets up state, then acks and retransmits guarantee delivery. UDP is fire-and-forget datagrams: no handshake, no ordering, no retransmit.

| Need | Reach for |
| --- | --- |
| Correctness, ordering, most request/response | TCP |
| Lowest latency, loss-tolerant (video, games, DNS) | UDP |
| Custom reliability without TCP's cost | UDP + app-level acks (QUIC does this) |

The tradeoff is reliability vs latency: TCP's ordering guarantee causes **head-of-line blocking** — one lost segment stalls every byte behind it until the retransmit lands. UDP never blocks because it never promises order; you pay by rebuilding whatever reliability you need yourself.

## IP, IPv4 vs IPv6, NAT

An IP address identifies a host on L3. IPv4 is 32-bit: ~4.3 billion addresses, exhausted years ago. IPv6 is 128-bit: address space stops being the constraint, and it drops NAT and broadcast for cleaner routing. The tradeoff is adoption cost: dual-stack operation and legacy gear keep IPv4 alive, so you run both. **NAT** exists to stretch IPv4 — many private addresses (`10.x`, `192.168.x`) share one public address, the router rewriting ports on the way out. It bought a decade but breaks inbound connections and end-to-end addressing, which is part of why IPv6 wants it gone.

## DNS

Resolution walks a hierarchy: your **recursive resolver** asks a **root** server (points to the TLD), then the **TLD** server for `.com` (points to the authoritative), then the **authoritative** server returns the record. Results cache at every hop, keyed by **TTL**.

- **A / AAAA**: name → IPv4 / IPv6 address.
- **CNAME**: name → another name (alias). Can't coexist with other records at the same node.
- **MX**: mail servers for the domain.
- **TXT**: arbitrary text — SPF, domain verification.

TTL is the freshness-vs-load tradeoff: a 24h TTL slashes resolver traffic but means a changed record (a failover, a new IP) is stale for up to a day across the internet. Drop TTL to 60s before a planned cutover, raise it after. The stale-record trap: resolvers and OS caches often ignore your TTL and hold longer, so never treat DNS as an instant switch.

## Protocol map

- **HTTP/1.1**: text, one request per connection at a time (pipelining unused). Runs over TCP.
- **HTTP/2**: binary framing, **multiplexing** many streams on one TCP connection — but a lost packet still head-of-line-blocks all streams (it's one TCP flow).
- **HTTP/3 / QUIC**: runs over UDP, moves reliability and ordering per-stream into userspace, so loss on one stream no longer stalls the others. Also 0-RTT reconnects.
- **WebSocket**: upgrades an HTTP connection to full-duplex; use for push/live, not for request/response you could cache.
- **gRPC**: HTTP/2 + protobuf, typed contracts and streaming — strong for internal service-to-service, weak where you need browser or human-readable calls.

Delivery scope: **unicast** (one-to-one, the default), **multicast** (one-to-many on a subnet), **anycast** (one address, many locations, routed to the nearest). Anycast is why a single CDN or public DNS IP resolves to the closest edge. HTTP version details live in api-web.md — don't duplicate them here.

## Ports worth knowing

| Port | Service |
| --- | --- |
| 80 / 443 | HTTP / HTTPS |
| 22 | SSH |
| 53 | DNS |
| 5432 | Postgres |
| 6379 | Redis |
| 27017 | MongoDB |

## Latency and geography

Speed of light sets the floor. Same-DC round trips run ~0.5 ms; same-region ~1-5 ms; cross-continent 100-300 ms no matter how fast your servers are. A chatty flow that makes 10 sequential calls cross-continent spends 1-3 seconds in transit alone — collapse round trips or move compute to the data. To serve users near their geography, push static and cacheable content to the edge: CDN — see caching-performance.md.
