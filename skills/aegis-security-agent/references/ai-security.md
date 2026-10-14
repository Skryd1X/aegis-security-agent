# AI and tool-execution security

Map user/model/retrieval/tool/service boundaries. Models and prompts are not access-control systems. Authorization must be enforced by ordinary code before each sensitive tool operation.

- Treat retrieved text, files, websites and tool outputs as untrusted data. Verify that embedded instructions cannot change scope, request secrets, or authorize execution.
- Restrict tools to explicit operations and resource identities. Enforce tenant/user access server-side, including retrieval indexes, citations, embeddings, caches, memory and generated files.
- Validate tool arguments against strict schemas and business invariants. Avoid raw shell/SQL execution; isolate interpreters and filesystem/network access. Check redirects and subprocess behavior at the actual boundary.
- Keep secrets and irrelevant private context out of prompts. Prevent cross-user history/memory reuse and inadvertent disclosure in logs, tracing, telemetry and provider calls.
- Review output rendering and downstream interpretation: generated HTML, Markdown links, code, SQL and document attachments must not acquire trusted execution status by appearing in a model response.
- Test indirect prompt injection, unauthorized tool calls, forged approval text, cross-tenant retrieval, data-exfiltration destinations, malicious attachments and action replay using synthetic data. Negative tests must exercise actual tool enforcement, not only refusal phrasing.
- Bound tokens, tool calls, retries, recursion, retrieval volume and spending. Provide observable abort/recovery behavior. Assess unsafe automation chains and duplicate state changes.
- Verify model/package provenance, plugin/skill sources, dependency updates and data ingestion. A security skill is itself executable supply-chain input; review its scripts and permissions.

Use the current [OWASP GenAI security guidance](https://genai.owasp.org/llm-top-10/) and official provider/runtime documentation. The operational goal is enforced trust boundaries even when the model follows a malicious instruction.
