# Findings, evidence, and closure

Create a local report directory appropriate to the project (for example security-audit/). Do not commit private findings/evidence without authorization. Reports should be understandable to both developers and owners.

## Required report content

1. Scope: project root/revision, environments, authorized remote targets and methods, dates, exclusions and access limits.
2. Architecture: detected components, assets, identities, data flows, trust boundaries, integrations and threat assumptions.
3. Coverage: concrete controls and standards versions, reviewed components and evidence, blocked checks and justified exclusions.
4. Findings: stable ID, title, affected location, confidence, evidence layer, preconditions, impact, severity rationale, root cause, affected variants, remediation and regression evidence.
5. Changes: files/configuration changed, compatibility effects, migrations, operational prerequisites and rollback/recovery steps.
6. Validation: baseline versus final results, exact commands/context, redacted logs, security and functional tests, each repeat pass and remaining gaps.
7. Outcome: verified within scope or incomplete, unresolved risks, owners/next actions, and explicit local/staging/production distinction.

## Finding states

Confidence: confirmed or suspected. Remediation: open, fixed-unverified, verified, residual, or false-positive. Verified means evidence addresses the stated flaw at the stated layer. False-positive needs a reason and evidence; deleting a scanner alert is insufficient. Residual means a known unresolved risk with rationale and owner, not a fixed finding. Critical/high residual risk prevents the strict closure gate from passing. A user's explicit risk acceptance may close the work assignment while the security gate still fails.

Severity: critical, high, medium, low, or informational. Base priority on exploitability, exposure, data sensitivity, blast radius and business impact; use a verified CVSS vector when appropriate. Confidence is separate from severity. Potential high-impact suspected findings must be investigated or explicitly retained as blocked uncertainty.

## Machine-readable ledger

Use the optional check_closure.py helper with this shape. This fictional example deliberately fails closure; it is not audit evidence:

```json
{
  "schema_version": 1,
  "scope": "Synthetic local example",
  "revision": "example-revision",
  "environment": "local",
  "coverage": [
    {"id": "AUTHZ-01", "status": "reviewed", "evidence": ["tests/authz.txt"]},
    {"id": "DEPLOY-01", "status": "blocked", "reason": "No deployment access"}
  ],
  "findings": [
    {"id": "SEC-001", "severity": "high", "confidence": "confirmed", "status": "fixed-unverified", "evidence": ["source-review.txt"], "validation": []}
  ],
  "checks": [
    {"id": "unit", "kind": "functional", "status": "passed", "evidence": ["tests/unit.txt"]},
    {"id": "security-retest", "kind": "security", "status": "blocked", "reason": "Retest pending"}
  ],
  "passes": [
    {"id": "pass-1", "method": "Source and boundary review", "evidence": ["source-review.txt"]}
  ]
}
```

Coverage statuses: reviewed, blocked, not-applicable. Check statuses: passed, failed, blocked; check kinds: functional, security. Findings require evidence; verified findings additionally need validation. Blocked/not-applicable items require a reason. Residual findings require a reason and owner. False-positive findings require a reason. Evidence paths are references, not automatically opened or executed by the helper.

The helper requires nonempty scope/revision/environment, coverage, at least one functional and one security check, at least two documented passes, no blocked coverage/checks, and no unresolved findings except explicitly documented medium/low/informational residual risks. All suspected findings must be resolved or such residual risks; a suspected critical/high residual also fails. These are structural closure rules. Humans and the agent must still inspect whether the declared evidence is real, current, and sufficient. Exit code 0: declared gate passes; 1: incomplete; 2: invalid input. The helper cannot certify the product.
