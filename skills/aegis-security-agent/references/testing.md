# Evidence-driven testing and remediation

## Execution planning

Choose tools after detecting the stack and inspecting the build/run instructions. Record tool/version, rules/configuration, exact command, working directory, revision, environment, timestamp, exit status, and a redacted evidence path. Scan generated/deployed artifacts where they differ from source. Record excluded paths and failed/incomplete scans.

| Evidence path | Candidate tools and decision criteria |
| --- | --- |
| Manual source/data-flow review | Follow attacker-controlled input to the sink and enforcement point. Check alternate routes, service calls, jobs, admin paths and config overrides. Essential for business logic and authorization. |
| Static analysis | Semgrep, CodeQL or language-native analyzers using maintained relevant rules. Check support/licensing/runtime and inspect alerts. No single ruleset covers the system. |
| Dependencies | Ecosystem audit tools, OSV-Scanner, container scanners such as Trivy/Grype. Include lockfiles and resolved images; verify advisories with upstream sources. Some tools transmit dependency metadata: check behavior before use. |
| Secrets | Gitleaks or another maintained local scanner. Review current tree, relevant history and build artifacts within scope; keep raw secrets out of evidence. Revocation is a separate operational task. |
| Config/IaC | Framework checks, IaC/container analyzers and provider policy inspection. Distinguish intended configuration from observed runtime state. |
| Runtime web/API | Targeted integration tests, browser/API clients and a properly scoped ZAP deployment where useful. Authenticated coverage needs synthetic roles and tenants. Review scanner rate and state-changing behavior first. |
| Native/mobile | Platform analyzers, MASTG procedures, sanitizers and scoped fuzzing of parsers in isolation. Hardware and physical effects require separate scope. |

Tool names are options, not bundled dependencies or promises of availability. Resolve official installation instructions and pin/review versions when adding tools. Never run remote install text through a shell blindly. Do not automatically use SaaS scanners on private source or data.

## Vulnerability verification

Build a minimal reproduction with synthetic data. Record preconditions and expected versus actual behavior. Test absence/presence of authentication, changed roles, alternate encodings, identifiers, method variants, boundary sizes and concurrent execution where relevant. Availability and expensive fuzz/load tests belong in authorized isolated environments.

For authorization, verify attacker denial and owner success on the same object; then vary tenant, endpoint and background path. For injection, demonstrate control reaching the relevant interpreter without destructive payloads. For payments, verify signed server-side state, idempotency and replay handling using sandbox integrations. For SSRF, use controlled test destinations and check redirect/DNS handling without contacting unapproved internal endpoints.

Inspect assertion strength: a test returning 403 is inadequate if the forbidden side effect still happened. Verify database/object state, emitted messages and audit logs where relevant. When a reproduction is impractical, preserve source evidence and explicitly describe the runtime gap.

## Fix validation

Prefer a regression test that fails on the original code, plus ordinary successful behavior and adjacent failure cases. Run supported lint/type/build checks and functional tests proportional to the changes. Retest with final configuration, not a patched test-only configuration. Keep lockfiles consistent; do not blindly run force upgrades.

Security fixes must address the root cause at all affected enforcement points. Investigate unrelated baseline failures without falsely attributing them to the patch. If a deployed environment is inaccessible, finish local verification and retain the deployment check as a blocker.

## Fresh re-audit

Revisit the trust-boundary map and coverage matrix after fixes. Review the final diff for weakened validation, overbroad privileges, swallowed failures, plaintext fallbacks and disabled controls. Retest equivalent sinks using a different input path or evidence method. Repeat until the declared closure gate passes or a specific boundary blocks further progress. Record every pass and its new findings; repeated green output from the same scanner is not an independent audit.
