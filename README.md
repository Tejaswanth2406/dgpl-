JWT Security Research Report
Introduction

JSON Web Tokens (JWT) are widely adopted for authentication and authorization in modern applications. Their compact structure and stateless nature make them efficient, but insecure implementation or misconfiguration can lead to serious vulnerabilities. This report highlights common JWT weaknesses, real-world attack vectors, and recommended mitigations.

Common JWT Vulnerabilities
1. alg=none (Unsigned Tokens)

Early JWT implementations accepted tokens with the header "alg":"none", effectively skipping signature verification. Attackers could craft arbitrary tokens that would be treated as valid.

Mitigation:
Reject alg=none. Configure libraries to only accept strong algorithms (e.g., HS256 or RS256) and enforce algorithm whitelisting.

2. Weak Secrets

If a symmetric algorithm like HS256 is used with a predictable secret such as "secret", attackers can guess or brute force the key and sign arbitrary tokens (e.g., escalate privileges to admin).

Mitigation:
Use long, random, high-entropy secrets (32+ bytes). Rotate keys periodically. Consider asymmetric signing (RS256) for stronger separation of signing and verification.

3. Key Confusion (Algorithm Switching)

Some implementations incorrectly allow a token signed with an asymmetric algorithm (e.g., RS256) to be verified with symmetric logic, treating the public key as an HMAC secret. This enables attackers to forge valid tokens.

Mitigation:
Strictly enforce algorithm checks and separate code paths for symmetric and asymmetric keys. Always validate the expected algorithm during verification.

4. Replay Attacks and Token Theft

JWTs are bearer tokens: possession equals access. If intercepted (e.g., via insecure transport), an attacker can reuse them until expiration.

Mitigation:
Always use TLS. Configure short token lifetimes and refresh tokens. Implement token revocation lists or track token IDs (jti) for high-value operations.

5. Insufficient Claim Validation

If claims such as exp, nbf, aud, or iss are not validated, tokens may remain valid indefinitely or be accepted in unintended contexts.

Mitigation:
Always enforce claim validation. Validate expiration, audience, and issuer fields using secure library features.

Best Practices

Use strong, random secrets or asymmetric algorithms.

Enforce algorithm whitelists and reject none.

Validate all critical claims (exp, nbf, iss, aud).

Use HTTPS consistently.

Apply key rotation and proper secret management.

Use short-lived tokens combined with refresh mechanisms.

References

OWASP JWT Cheat Sheet

NIST CVE Database
 — real-world JWT-related vulnerabilities

PyJWT Documentation
