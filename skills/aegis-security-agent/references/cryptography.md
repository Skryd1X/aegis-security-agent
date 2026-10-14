# Cryptography and sensitive-data engineering

Choose protection from the data lifecycle and attacker model. Inventory what must be encrypted, what must be hashed, what needs integrity/authenticity, and who must be able to decrypt it. Prefer avoiding unnecessary sensitive data. Encryption does not replace access control, isolation, retention limits, or incident response.

## Decision rules

- Passwords: use the framework's maintained password API and an adaptive password hash such as Argon2id with unique salts; choose parameters using current guidance and measurements on the deployment hardware. Never store recoverable passwords. A pepper is optional and needs separate key custody and a rotation plan.
- Recoverable data: use a maintained authenticated-encryption API, commonly AES-GCM or ChaCha20-Poly1305 where suitable. Verify platform/regulatory requirements and library guidance. Ensure nonce uniqueness under each key; use the library's supported nonce-generation and envelope format. Never invent a cipher, reuse a nonce, or use unauthenticated encryption as a new design.
- Opaque high-entropy tokens: generate with a cryptographically secure RNG. Consider storing a digest instead of the usable token; choose a keyed MAC when the threat model calls for it. Password hashing requirements and random-token verification are different problems.
- Integrity/authenticity: use supported MAC/signature primitives with explicit domain/purpose separation. Encryption alone is not proof of sender identity. Canonicalize the exact signed payload where the protocol requires it and verify before acting.
- Transport: use supported TLS configuration and certificate/hostname verification, including internal and outbound connections. Follow current vendor recommendations; do not disable verification to fix connectivity. Browser headers are not substitutes for encrypted transport.
- End-to-end encryption: define endpoints, identity verification, device enrollment, key agreement, forward secrecy, recovery, group membership and metadata leakage. Use an established protocol and implementation with appropriate review. Server-side envelope encryption is not automatically end-to-end encryption.

## Key lifecycle

Keep keys outside source, images, logs and plaintext database rows beside the encrypted data. Prefer a managed KMS/HSM or secret manager where justified. Define creation, custody, allowed identities, versioning, rotation, revocation, disaster recovery and deletion. Use envelope encryption when it fits the deployment; constrain decrypt privileges and record audited access. Never embed a shared decrypt key in a public client.

Describe key compromise and rotation behavior before changing storage. A new key must not make historical data unrecoverable. Version ciphertext/envelopes and authenticate relevant context (for example tenant, object and schema identifiers) as associated data to prevent cross-context substitution. Authentication failure must reject the data and avoid side effects.

## Migration and validation

Specify inventory, backups, staging rehearsal, dual-read strategy if needed, batched rewrite, concurrency handling, rollback/recovery, old-key retention and final cleanup. Do not encrypt every field mechanically; query/index behavior and plaintext derived copies must be considered. Live data migration requires explicit authorization.

Verify round trips, wrong-key rejection, tamper detection, truncated/malformed ciphertext, nonce policy, context binding, old/new key coexistence, rotation, recovery and access denials. Check logs, caches, backups and analytics for plaintext copies. Test with synthetic data and redacted evidence. Do not replace a maintained crypto library with a hand-written implementation to satisfy an imagined "highest level" requirement.

## Authoritative guidance

Consult current [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html), [Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [Key Management](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html), [NIST cryptographic standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines), and the selected library/KMS vendor documentation. Record retrieved guidance and supported platform versions. FIPS validation, legal compliance, and protocol assurance require evidence specific to the actual modules and deployment.
