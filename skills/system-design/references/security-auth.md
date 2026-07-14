# Security & Auth

## Session vs token

- **Session + cookie**: server stores session, client holds an opaque cookie. Easy to revoke, stateful, needs shared session store to scale. Set `HttpOnly`, `Secure`, `SameSite`.
- **JWT**: signed, stateless, self-contained claims. Scales without a session store but is hard to revoke before expiry. Keep TTL short, pair with a refresh token, keep a revocation list for logout/compromise.

Default to sessions for classic web apps; use JWT for stateless APIs and service-to-service — and know the revocation cost.

## OAuth 2.0 / OIDC

OAuth 2.0 = delegated **authorization**. OIDC adds an ID token for **authentication** on top.
- **Authorization Code + PKCE**: the correct flow for web and mobile/SPA today.
- **Client Credentials**: service-to-service, no user.
- Avoid Implicit and Password grants — deprecated/insecure.

Access token = short-lived, sent to APIs. Refresh token = long-lived, guarded, exchanged for new access tokens.

## SSO

One identity provider, many apps. SAML (enterprise, XML) or OIDC (modern, JSON/JWT). Central revocation and MFA are the wins.

## Encoding vs encryption vs hashing vs tokenization

- **Encoding** (base64): reversible, not security. Don't confuse with encryption.
- **Encryption**: reversible with a key. Symmetric (AES, fast, shared key) vs asymmetric (RSA/EC, key pair, TLS handshake/signing).
- **Hashing**: one-way. Passwords → slow salted hash (argon2/bcrypt/scrypt), never fast hashes, never plain.
- **Tokenization**: replace sensitive value with a token mapped in a secure vault (PCI).

## Secrets management

Never in code or images. Use a secrets manager (Vault, cloud KMS/CSMS) or an operator like External Secrets. Rotate. Prefer keyless/workload-identity auth (IAM roles, IRSA, agency-based) over long-lived static keys.

## Permission models

RBAC (roles) scales for coarse control; ABAC (attributes) for fine-grained; ReBAC (relationship graph, e.g. Zanzibar) for "can user X access object Y" at scale. Enforce on the server, per request, against server-side identity — never trust client-declared roles or IDs.

## Baseline

TLS everywhere, validate input at trust boundaries, least privilege, defense in depth, log security events, patch dependencies. DevSecOps = shift these left into CI (SAST, dependency/CVE scan, image scan).
