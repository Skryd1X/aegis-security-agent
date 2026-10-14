# Security coverage matrix

Use this as a routing checklist, then expand it into concrete versioned requirements for the actual system. It is not a substitute for ASVS/MASVS or a claim that every listed control applies. Each applicable area needs component-level evidence; each exclusion needs a reason.

| Area | Review and verify |
| --- | --- |
| Architecture and threat model | Assets, entry points, trust boundaries, public/admin/internal exposure, privileged actors, sensitive flows, multi-stage attacks, fail-open behavior, assumptions about upstream controls. |
| Identity and authentication | Enrollment, credential checks, enumeration, recovery, MFA/passkeys, federation callbacks, account linking, step-up authentication, lockout abuse, service identities, safe bootstrap/admin defaults. |
| Sessions and tokens | Fixation, rotation, expiry, revocation, logout, cookie flags and scope, CSRF, refresh-token reuse, JWT algorithm allowlist, signature/key selection, issuer/audience/time validation, token leakage. |
| Authorization and tenancy | Server-side ownership, object/property/function authorization, role escalation, tenant scoping on queries/cache/search/exports/files/jobs/WebSockets, mass assignment, impersonation, administrative APIs. |
| Input and interpreter boundaries | SQL/NoSQL/LDAP/template/OS injection, XSS and contextual encoding, unsafe deserialization, regex/resource exhaustion, ambiguous parsing, type confusion, schema validation, path normalization. |
| Files and content processing | Traversal and symlinks, archive extraction, compressed-size limits, MIME and signature checks, image/document converters, execution rights, isolated processing, private downloads, signed URL scope/expiry. |
| Requests and protocols | SSRF through initial URL and redirects, DNS rebinding, scheme restrictions, cloud metadata, proxy trust, host headers, HTTP request smuggling/parser differences, CORS, CSRF, GraphQL depth and field authorization. |
| Business logic | Price/discount/balance authority, payment signatures and backend state, idempotency, replay, order transitions, concurrent updates, transaction isolation, inventory, coupon abuse, bypassed multi-step flows. |
| Data and privacy | Classification, minimization, retention/deletion, logs/traces/analytics/cache/backups, exports, object storage access, database privileges, redaction, recovery, authorization on deletion and portability. |
| Cryptography and keys | Purpose-appropriate encryption/hashing/MAC/signatures, nonce and entropy, key custody/rotation/recovery, authenticated decryption, TLS verification, lifecycle/migration; use cryptography.md. |
| APIs and integrations | Inventory/version retirement, pagination/batch/resource limits, scopes, webhook signatures and replay defense, OAuth redirect/state/PKCE validation, outbound response validation, retry and secret isolation. |
| Availability and abuse | Bounded payloads/timeouts/queues, expensive endpoints, per-identity/tenant budgets, distributed rate limits, backpressure, circuit breaking, safe error handling; load tests only in authorized isolated environments. |
| Dependencies and build | Lockfiles, direct/transitive advisories, reachability, compromised packages, registry ambiguity, install scripts, reproducibility, SBOM/provenance, signing verification, release artifacts. |
| Infrastructure and deployment | IAM, ingress/egress, TLS termination, storage exposure, least privilege, service isolation, container capabilities/users, IaC state secrets, Kubernetes RBAC/admission, config drift, patching. |
| CI/CD and developer systems | Untrusted pull requests, workflow token permissions, injection into shell/templates, secret access, runner persistence, artifact trust, environment protections, action pinning and update ownership. |
| Client and browser | DOM sinks, dangerous rendering, storage of tokens, CSP appropriate to application behavior, framing policy, service-worker caching, source maps and embedded credentials, integrity of external assets. |
| Observability and response | Auditability of privileged events, log injection/redaction, alerting ownership, detection tests, incident containment, backup restore evidence, secret revocation procedure, security-contact handling. |
| Native/mobile/desktop | Platform storage, IPC, deep links, permissions, update signing, webviews, local privilege boundaries, transport security; use platforms.md. |
| AI and agent systems | Prompt injection, tool authorization, retrieval isolation, data disclosure, tool chaining, budget limits, model supply chain; use ai-security.md. |

For each row, create controls with IDs owned by the audit or verified IDs from a named standard. Mark coverage as reviewed, blocked, or not-applicable. "Reviewed" needs evidence even when no finding was identified. Record the separate implementation outcome; reviewed does not mean secure. Sample-based review must name the sample and uncovered variants.
