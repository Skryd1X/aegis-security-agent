# Validation record

Prepared on 2026-10-14. This record describes the package, not the security of any user application.

| Check | Result | Evidence boundary |
| --- | --- | --- |
| Bundled skill-creator quick_validate.py | PASS | Skill name/frontmatter validation. The optional compatibility frontmatter field was moved into the body to support this validator's narrower accepted fields. |
| scripts/validate_package.py | PASS | Canonical layout, English Markdown, local references and Claude manifests. Not a full vendor runtime schema validator. |
| Python unittest suite | PASS: 19 tests | Windows, Python 3.12. Installer copy/refusal/rollback/symlink boundaries; ledger state validation and CLI exit codes. Synthetic references are not application evidence. |
| Installation destinations | PASS | Both client directory layouts were exercised in disposable temporary directories. No user client settings or global skills were modified. |
| Standard-library runtime | PASS | Package helpers run without third-party dependencies. PyYAML was used only in an isolated validation environment for the external skill-creator validator. |
| Claude Code runtime/plugin validator | NOT RUN | Claude Code CLI was not available. Marketplace structure was inspected against official documentation. |
| Codex live skill invocation | NOT RUN | No separate application audit was executed through the client using this skill. |
| GPT/API integration | NOT RUN | No API-backed runtime was provisioned or invoked. Requires the host's supported skill-loading and tool access. |
| Behavioral security evaluation | NOT RUN | Forward-test scenarios are included in tests/behavioral-evaluation.md. Real audit quality is not established by helper unit tests. |
| GitHub CI | NOT RUN | Workflow is prepared for Linux/Windows and Python 3.10/3.12. No repository was published and no hosted run was triggered. |
| GitHub publication | Separate delivery step | Local tests do not establish remote publication. Verify the repository commit and hosted CI independently. |

The skill is ready for local installation and review. Advertise verified cross-client audit behavior only after executing the behavioral scenarios in the actual target clients. No test here establishes that an arbitrary application has no vulnerabilities.
