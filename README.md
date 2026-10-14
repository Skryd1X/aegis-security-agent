# Aegis Security Agent

Created by **Skryd1X**.

A portable English-language Agent Skill for evidence-driven software security audits and remediation in Claude Code, Codex, and compatible tool-enabled GPT runtimes.

The agent discovers the real architecture, builds a threat model and coverage matrix, investigates vulnerabilities, implements authorized fixes, and repeats security and functional checks. It covers web/API services, mobile and desktop applications, infrastructure, CI/CD, dependencies, sensitive data, cryptography and AI tool boundaries. It preserves the product's architecture and legitimate behavior.

This is an instruction package, not an autonomous daemon, scanner distribution, or guarantee that every vulnerability will be found. It needs the host's actual tools and project access. Automatic selection is enabled, but selection depends on the host; invoke it explicitly when a full audit is required. No hooks, external services or telemetry are installed.

## Install from a cloned repository

Requires Python 3.10+ for the optional installer. No third-party Python packages are needed. Run from this repository root:

```sh
# Install for the current project; pass the application repository explicitly.
python scripts/install.py --agent codex --project /path/to/application
python scripts/install.py --agent claude --project /path/to/application

# Install once for all local projects for either or both clients.
python scripts/install.py --agent both --user
```

The installer copies the skill to `.agents/skills/aegis-security-agent` for Codex and `.claude/skills/aegis-security-agent` for Claude Code. `--user` uses the same paths under your home directory. It refuses to replace an existing installation. For updates, review the new version and rename/move the old installation before copying it. It does not modify client settings or install scanning tools. Restart/reload the client if discovery has not refreshed.

To install without Python, copy the complete `skills/aegis-security-agent/` directory into the appropriate skills location. Review the instructions and scripts before installation. The installer is deliberately local: clone/download a reviewed release rather than executing remote installation text.

## Install from GitHub

Repository: https://github.com/Skryd1X/aegis-security-agent. Created by **Skryd1X**.

```sh
git clone https://github.com/Skryd1X/aegis-security-agent.git
cd aegis-security-agent
python scripts/install.py --agent both --user
```

In Codex with its skill-installer available:

```text
$skill-installer install https://github.com/Skryd1X/aegis-security-agent/tree/main/skills/aegis-security-agent
```

Claude Code marketplace alternative:

```text
/plugin marketplace add Skryd1X/aegis-security-agent
/plugin install aegis-security-agent@aegis-security-agent-marketplace
```

The marketplace points to this repository root, which contains the plugin manifest and the canonical skill. The plugin invocation is `/aegis-security-agent:aegis-security-agent`. A direct folder installation uses `/aegis-security-agent`. Do not install both copies unless you intend both to be available.

## Use

Codex:

```text
Use $aegis-security-agent to audit this repository and fix in-scope vulnerabilities.
Discover the architecture, cover all applicable security areas, preserve intended
behavior, and repeat tests and review until verified closure or explicit blockers.
Use local/staging synthetic data for state-changing tests. Report findings,
changes, coverage, evidence, residual risks, and any deployment checks still needed.
```

Claude Code (direct installation):

```text
/aegis-security-agent Audit and harden this project, fix vulnerabilities, and re-audit with evidence.
```

For an inspection-only task, say "Audit only; do not edit files." For secure development, ask the agent to apply the skill while building the feature. This does not silently trigger live remote testing or deployment.

## GPT/API and hosted chat environments

For a compatible tool-enabled runtime, load the whole skill directory using that runtime's supported Agent Skills mechanism. OpenAI's Responses API supports local/hosted shell skills; Agents API sandboxes discover registered capability directories. Follow current official setup documentation rather than assuming a GitHub URL installs a skill into every GPT product.

A plain chat or custom GPT instruction field does not gain repository, terminal, scanning, deployment, or credential access by reading SKILL.md. In such an environment the instructions can guide analysis of supplied artifacts, but autonomous fixes require connected tools and authorized workspace access. No GPT account setup or API credentials are bundled here.

## Verification and limitations

```sh
python scripts/validate_package.py
python -m unittest discover -s tests -v
python skills/aegis-security-agent/scripts/check_closure.py /path/to/ledger.json
```

Package validation checks portable structure, internal references and manifests. Tests exercise installer safety and declared ledger gates. The ledger helper does not run an application audit or verify the truth of evidence. Cross-client behavior and real-project security effectiveness must be evaluated separately; see `tests/behavioral-evaluation.md` and `VALIDATION.md`.

A completed audit must distinguish source, local, staging and deployed evidence. Missing tools/credentials remain explicit blockers. "Verified within scope" never means zero unknown vulnerabilities. Cryptographic changes use maintained libraries and a key/migration/recovery plan; the agent does not invent encryption protocols or mechanically encrypt all fields.

## Sources and maintenance

See [the source index](skills/aegis-security-agent/references/standards.md) for OWASP, NIST, MITRE, FIRST and upstream research. Refresh current editions/advisories during each audit. The package references standards rather than copying their full texts. Guidance is original project-specific workflow material, not a compliance certificate.

Official format/runtime references: [Agent Skills specification](https://agentskills.io/specification), [Claude Code skills](https://code.claude.com/docs/en/skills), [Claude marketplace distribution](https://code.claude.com/docs/en/plugin-marketplaces), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [OpenAI API skills](https://developers.openai.com/api/docs/guides/tools-skills).

## License

MIT. See [LICENSE](LICENSE). Referenced third-party standards and tools retain their own licenses. Audit artifacts created in a target project follow that project's access and publication rules.
