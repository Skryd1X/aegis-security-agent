#!/usr/bin/env python3
"""Check declared audit ledger consistency; never claim to certify application security."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(text(item) for item in value)


def evaluate(data: Any) -> tuple[list[str], list[str]]:
    """Return schema errors separately from unfulfilled closure requirements."""
    errors: list[str] = []
    blockers: list[str] = []
    if not isinstance(data, dict):
        return ["Ledger must be a JSON object"], []
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be integer 1")
    for field in ("scope", "revision", "environment"):
        if not text(data.get(field)):
            errors.append(f"{field} must be a nonempty string")
    groups: dict[str, list[dict[str, Any]]] = {}
    for group in ("coverage", "findings", "checks", "passes"):
        items = data.get(group)
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            errors.append(f"{group} must be an array of objects")
            groups[group] = []
            continue
        groups[group] = items
        identifiers: set[str] = set()
        for index, item in enumerate(items):
            identifier = item.get("id")
            if not text(identifier):
                errors.append(f"{group}[{index}] needs a nonempty id")
            elif identifier in identifiers:
                errors.append(f"Duplicate {group} id: {identifier}")
            else:
                identifiers.add(identifier)

    for group, permitted in (
        ("coverage", {"reviewed", "blocked", "not-applicable"}),
        ("checks", {"passed", "failed", "blocked"}),
        ("findings", {"open", "fixed-unverified", "verified", "residual", "false-positive"}),
    ):
        for item in groups[group]:
            label = f"{group}:{item.get('id', '?')}"
            status = item.get("status")
            if not isinstance(status, str) or status not in permitted:
                errors.append(f"{label} has an invalid status")
                continue
            needs_evidence = group == "findings" or status in {"reviewed", "passed"}
            if needs_evidence and not strings(item.get("evidence")):
                errors.append(f"{label} needs nonempty evidence references")
            if status in {"blocked", "not-applicable", "residual", "false-positive"}:
                if not text(item.get("reason")):
                    errors.append(f"{label} needs a reason")
            if group == "checks":
                if item.get("kind") not in ("functional", "security"):
                    errors.append(f"{label} kind must be functional or security")
                if status != "passed":
                    blockers.append(f"{label} is {status}")
            elif group == "coverage" and status == "blocked":
                blockers.append(f"{label} is blocked")
            elif group == "findings":
                severity = item.get("severity")
                if severity not in ("critical", "high", "medium", "low", "informational"):
                    errors.append(f"{label} has an invalid severity")
                if item.get("confidence") not in ("confirmed", "suspected"):
                    errors.append(f"{label} has an invalid confidence")
                if status == "verified" and not strings(item.get("validation")):
                    errors.append(f"{label} needs validation references")
                if status == "verified" and item.get("confidence") != "confirmed":
                    errors.append(f"{label} cannot be verified while its confidence is suspected")
                if status == "residual" and not text(item.get("owner")):
                    errors.append(f"{label} needs a residual risk owner")
                if status in {"open", "fixed-unverified"}:
                    blockers.append(f"{label} is {status}")
                elif status == "residual" and severity in {"critical", "high"}:
                    blockers.append(f"{label} retains a {severity} risk")

    if not groups["coverage"]:
        blockers.append("Coverage matrix is empty")
    if not any(item.get("status") == "reviewed" for item in groups["coverage"]):
        blockers.append("No applicable coverage has been reviewed")
    for kind in ("functional", "security"):
        if not any(item.get("kind") == kind for item in groups["checks"]):
            blockers.append(f"No {kind} check recorded")
    if len(groups["passes"]) < 2:
        blockers.append("Initial audit and fresh re-audit must both be recorded")
    for item in groups["passes"]:
        if not text(item.get("method")) or not strings(item.get("evidence")):
            errors.append(f"passes:{item.get('id', '?')} needs a method and evidence")
    return errors, blockers


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        if args.ledger.stat().st_size > 10 * 1024 * 1024:
            raise ValueError("Ledger exceeds the 10 MiB input limit")
        data = json.loads(args.ledger.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_object)
        errors, blockers = evaluate(data)
    except (OSError, ValueError, RecursionError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 2
    if errors:
        print("INVALID LEDGER")
        for error in errors:
            print(f"- {error}")
        return 2
    if blockers:
        print("INCOMPLETE")
        for blocker in blockers:
            print(f"- {blocker}")
        return 1
    print("DECLARED CLOSURE GATE PASSED; evidence truth and sufficiency remain unverified by this helper.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
