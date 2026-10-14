# Platform-specific review

Use only the sections matching observed artifacts. Mixed projects may need several sections. Locate the deployed enforcing component before changing policy.

## Web services and APIs

Map routes to middleware and data stores. Verify authorization at the service boundary, safe ORM/raw query use, environment overrides, debug/admin exposure, object access, serialization fields, validation, reverse-proxy trust, and asynchronous copies of HTTP business logic. Test stateless and stateful auth paths independently.

For Python inspect Django/Flask/FastAPI dependency/middleware order, settings overrides, template safety, pickle/YAML loading, subprocess calls and filesystem helpers. For JS/TS inspect Express/Fastify/Nest middleware, prototype pollution sinks, unsafe merge operations, HTML/DOM output, Node child processes, SSR loaders and API actions. For JVM/.NET/PHP/Ruby inspect framework-specific access enforcement, deserialization, template evaluation, binding and production config. For Go/Rust/native services inspect unsafe/FFI code, parser bounds, concurrency, subprocesses, and error handling. Languages are routing hints, not proof of safety.

## Mobile

Use MASVS requirements and MASTG procedures appropriate to Android/iOS. Check Keychain/Keystore usage, backups, cleartext files and logs, exported activities/components, entitlements, deep/universal links, webview bridges, network trust, session management, dependency behavior, debug build leakage, and signed release distribution. Client integrity controls cannot replace backend access control. Root/jailbreak detection and pinning need a threat-model justification and recovery/update plan; do not add them mechanically.

## Desktop, CLI, and local agents

Review local privilege and user boundaries, filesystem permissions, temporary files, executable search paths, command quoting, IPC origins and peer authentication, protocol handlers, embedded browser bridges, plugin trust, and signed update verification. In Electron inspect nodeIntegration/contextIsolation/sandbox and every IPC capability, preload bridge, navigation and window-open policy. In Tauri inspect capability scope and invoke handlers. Avoid storing service credentials in packaged client binaries.

## Cloud, containers, and infrastructure

Match IaC intent to observable deployed configuration if access exists. Review public exposure, network boundaries, IAM conditions and escalation paths, workload identity, service account tokens, storage policies, private secrets, database grants, image provenance, runtime isolation, resource limits, backup recovery and logging. Do not silently apply infrastructure plans; prepare and review destructive/replacement effects first. Managed encryption does not remedy public access permissions.

## CI/CD and supply chain

Follow untrusted inputs from PR metadata, commits, artifacts and fork jobs into shell commands and privileged releases. Review permissions per job, secret availability, environment approvals, runner isolation, dependency confusion, action/image pins, artifact verification and publishing identity. A pin needs an update process. A dependency finding needs resolved package/version and affected usage; lack of known CVEs does not prove a package is trustworthy.

## Embedded, IoT, OT and specialized systems

Inspect provisioning, device identity, firmware/update authenticity and rollback, debug interfaces, secret storage, network exposure, physical threat assumptions and isolation. Avoid active tests that could affect hardware, safety, availability, or physical processes without a dedicated approved test plan. Smart contracts, kernel code, medical/safety systems and cryptographic protocol design need domain-specific verification and specialist review; record that boundary rather than treating the generic checklist as sufficient.
