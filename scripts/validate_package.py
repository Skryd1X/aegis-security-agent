#!/usr/bin/env python3
"""Validate this package's portable layout and internal references without dependencies."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skill = root / "skills" / "aegis-security-agent"
    required = [skill / "SKILL.md", skill / "agents" / "openai.yaml",
                skill / "LICENSE.txt", root / "LICENSE", root / "README.md"]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing file: {path.relative_to(root)}")
    if errors:
        return errors
    content = (skill / "SKILL.md").read_text(encoding="utf-8")
    header = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not header:
        errors.append("SKILL.md must have YAML frontmatter")
    else:
        fields = dict(re.findall(r"^([a-z-]+): (.+)$", header.group(1), re.M))
        if fields.get("name") != skill.name:
            errors.append("Skill name must match its directory")
        description = fields.get("description", "")
        if not 1 <= len(description) <= 1024:
            errors.append("Description must have 1-1024 characters")
        if len(fields.get("compatibility", "")) > 500:
            errors.append("Compatibility exceeds 500 characters")
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlinks are not distributed: {path.relative_to(root)}")
        if path.is_file() and path.suffix == ".md":
            text = path.read_text(encoding="utf-8")
            if re.search(r"[\u0400-\u04ff]", text):
                errors.append(f"Non-English Cyrillic content: {path.relative_to(root)}")
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                    errors.append(f"Broken local reference in {path.relative_to(root)}: {target}")
    try:
        plugin = json.loads((root / ".claude-plugin" / "plugin.json").read_text())
        marketplace = json.loads((root / ".claude-plugin" / "marketplace.json").read_text())
        if plugin.get("name") != skill.name or plugin.get("version") != "1.0.0":
            errors.append("Plugin identity/version mismatch")
        if marketplace.get("name") != "aegis-security-agent-marketplace":
            errors.append("Marketplace name mismatch")
        if not marketplace.get("owner", {}).get("name"):
            errors.append("Marketplace owner missing")
        entries = marketplace.get("plugins", [])
        if len(entries) != 1 or entries[0].get("source") != "./" or entries[0].get("name") != plugin.get("name"):
            errors.append("Marketplace source/identity mismatch")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        errors.append(f"Manifest validation failed: {error}")
    return errors


if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    print("Package validation passed" if not failures else "Package validation failed")
    raise SystemExit(bool(failures))
