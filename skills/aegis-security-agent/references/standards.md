# Standards and research sources

Research baseline checked on 2026-10-14. Refresh current editions and vendor advisories during each audit; this file is a source index, not a frozen vulnerability database. Distinguish stable releases, drafts, development branches and superseded editions. If offline, cite the available edition and label freshness unverified.

| Source | Purpose |
| --- | --- |
| [OWASP ASVS](https://owasp.org/projects/asvs) | Versioned web application verification requirements. ASVS 5.0.0 was identified as the stable baseline during preparation; verify the selected requirement IDs against the actual edition. |
| [OWASP WSTG](https://owasp.org/projects/web-security-testing-guide) | Concrete web testing methods; cite a versioned procedure where possible. |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Implementation guidance for individual controls; check compatibility with the framework and library versions. |
| [OWASP API Security](https://owasp.org/www-project-api-security/) | API-specific abuse patterns; supplement full verification rather than using the Top Ten as an exhaustive checklist. |
| [OWASP MASVS/MASTG](https://mas.owasp.org/) | Mobile verification requirements and testing procedures. |
| [NIST SSDF](https://csrc.nist.gov/projects/ssdf) | Secure development lifecycle, provenance and vulnerability-response practices. SP 800-218 version 1.1 is a known published baseline; verify revisions before claiming current conformance. |
| [NIST CSF](https://www.nist.gov/cyberframework) | Organizational risk ownership and operational response; not a replacement for source-level application testing. |
| [MITRE CWE](https://cwe.mitre.org/) | Classify weakness/root cause; verify IDs before mapping findings. |
| [FIRST CVSS v4.0](https://www.first.org/cvss/v4.0/specification-document) | Technical severity scoring when the available facts support a vector. Record the vector and business/context rationale separately. |
| [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | Evidence of exploitation in the wild to inform remediation priority; absence does not establish safety. |
| [OSV](https://osv.dev/) and upstream vendor advisories | Package/version-specific vulnerability evidence. Match the resolved package, platform, affected range and reachable usage. |
| [SLSA](https://slsa.dev/) and [OpenSSF](https://openssf.org/) | Build provenance and software supply-chain practices; do not claim an assurance level without its required evidence. |
| [OWASP GenAI Security](https://genai.owasp.org/) | AI-specific application and agent risks; apply deterministic enforcement and synthetic attack tests. |

Use official framework, language, operating-system, cloud, database and crypto-library documentation for implementation choices. Supplement with original peer-reviewed papers or primary security advisories when the threat model needs deeper research. Assess date, reproducibility, deployment assumptions, and whether an experimental defense has production support. Do not adopt a complex technique merely because it is described as cutting edge.

For each researched decision, record source URL, edition/date, retrieved date, applicable component/control, and how it changes the finding or fix. Avoid copying standards wholesale; link to authoritative requirements and write project-specific evidence. These mappings support review; they do not issue compliance certification.
