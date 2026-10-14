"""Exercise installation isolation and closure states with synthetic evidence."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("installer", ROOT / "scripts" / "install.py")
closure = load("closure", ROOT / "skills" / "aegis-security-agent" / "scripts" / "check_closure.py")
validator = load("validator", ROOT / "scripts" / "validate_package.py")


def ledger():
    return {
        "schema_version": 1, "scope": "Synthetic fixture", "revision": "fixture-v1",
        "environment": "local",
        "coverage": [{"id": "AUTHZ", "status": "reviewed", "evidence": ["fixture-review"]}],
        "findings": [{"id": "SEC-1", "severity": "high", "confidence": "confirmed",
                      "status": "verified", "evidence": ["fixture-before"], "validation": ["fixture-after"]}],
        "checks": [{"id": kind, "kind": kind, "status": "passed", "evidence": ["fixture-check"]}
                   for kind in ("functional", "security")],
        "passes": [{"id": str(i), "method": method, "evidence": ["fixture-pass"]}
                   for i, method in enumerate(("Source review", "Runtime boundary review"))],
    }


class ClosureTests(unittest.TestCase):
    def test_complete_declared_ledger(self):
        self.assertEqual(closure.evaluate(ledger()), ([], []))

    def test_unresolved_findings_fail(self):
        for status in ("open", "fixed-unverified"):
            with self.subTest(status=status):
                data = ledger()
                data["findings"][0]["status"] = status
                errors, blockers = closure.evaluate(data)
                self.assertFalse(errors)
                self.assertTrue(blockers)

    def test_high_residual_fails(self):
        data = ledger()
        data["findings"][0].update(status="residual", reason="Pending rotation", owner="Operator")
        self.assertTrue(closure.evaluate(data)[1])

    def test_low_residual_is_explicit(self):
        data = ledger()
        data["findings"][0].update(severity="low", status="residual", reason="Documented tradeoff", owner="Owner")
        self.assertEqual(closure.evaluate(data), ([], []))
        del data["findings"][0]["owner"]
        self.assertTrue(closure.evaluate(data)[0])

    def test_suspected_open_high_fails(self):
        data = ledger()
        data["findings"][0].update(confidence="suspected", status="open")
        self.assertTrue(closure.evaluate(data)[1])

    def test_suspected_finding_cannot_be_verified(self):
        data = ledger()
        data["findings"][0]["confidence"] = "suspected"
        self.assertTrue(closure.evaluate(data)[0])

    def test_false_positive_needs_reason(self):
        data = ledger()
        data["findings"][0]["status"] = "false-positive"
        self.assertTrue(closure.evaluate(data)[0])
        data["findings"][0]["reason"] = "Input never reaches the suspected sink"
        self.assertEqual(closure.evaluate(data), ([], []))

    def test_missing_verification_invalid(self):
        data = ledger()
        data["findings"][0]["validation"] = []
        self.assertTrue(closure.evaluate(data)[0])

    def test_blocked_coverage_or_checks_fail(self):
        for group in ("coverage", "checks"):
            data = ledger()
            data[group][0].update(status="blocked", reason="Access unavailable")
            self.assertTrue(closure.evaluate(data)[1])

    def test_missing_reaudit_or_functional_check_fails(self):
        data = ledger()
        data["passes"].pop()
        self.assertTrue(closure.evaluate(data)[1])
        data = ledger()
        data["checks"] = [data["checks"][1]]
        self.assertTrue(closure.evaluate(data)[1])

    def test_duplicate_ids_and_boolean_schema_invalid(self):
        data = ledger()
        data["schema_version"] = True
        data["findings"].append(copy.deepcopy(data["findings"][0]))
        self.assertGreaterEqual(len(closure.evaluate(data)[0]), 2)

    def test_wrong_types_never_crash(self):
        for data in (None, [], {}, {"findings": "wrong"}):
            self.assertTrue(closure.evaluate(data)[0])
        data = ledger()
        data["findings"][0]["status"] = []
        self.assertTrue(closure.evaluate(data)[0])

    def test_cli_exit_codes_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            for state, expected in (("verified", 0), ("open", 1)):
                data = ledger()
                data["findings"][0]["status"] = state
                path.write_text(json.dumps(data), encoding="utf-8")
                result = subprocess.run([sys.executable, closure.__file__, str(path)], capture_output=True)
                self.assertEqual(result.returncode, expected)
            path.write_text('{"schema_version": 1, "schema_version": 2}', encoding="utf-8")
            result = subprocess.run([sys.executable, closure.__file__, str(path)], capture_output=True)
            self.assertEqual(result.returncode, 2)


class InstallerTests(unittest.TestCase):
    def test_both_installations_contain_canonical_files(self):
        with tempfile.TemporaryDirectory() as directory:
            destinations = installer.install("both", Path(directory))
            for destination in destinations:
                for source in installer.SOURCE.rglob("*"):
                    if source.is_file() and "__pycache__" not in source.parts:
                        self.assertEqual(source.read_bytes(), (destination / source.relative_to(installer.SOURCE)).read_bytes())

    def test_preflight_preserves_existing_and_creates_no_other_install(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            original = installer.install("claude", base)[0]
            marker = original / "keep.txt"
            marker.write_text("User data")
            with self.assertRaises(FileExistsError):
                installer.install("both", base)
            self.assertEqual(marker.read_text(), "User data")
            self.assertFalse((base / ".agents").exists())

    def test_invalid_root_and_agent(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                installer.install("unknown", Path(directory))
            with self.assertRaises(FileNotFoundError):
                installer.install("codex", Path(directory) / "missing")

    def test_partial_copy_rolls_back_only_new_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / "unrelated.txt").write_text("keep")
            with patch.object(installer.shutil, "copytree", side_effect=OSError("Synthetic copy error")):
                with self.assertRaises(OSError):
                    installer.install("both", base)
            self.assertFalse((base / ".agents" / "skills" / installer.NAME).exists())
            self.assertEqual((base / "unrelated.txt").read_text(), "keep")

    def test_symlinked_destination_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            base = Path(directory)
            try:
                (base / ".agents").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("OS does not grant symlink creation privileges")
            with self.assertRaises(ValueError):
                installer.install("codex", base)
            self.assertFalse((Path(outside) / "skills").exists())


class PackageTests(unittest.TestCase):
    def test_package_references_and_manifests(self):
        self.assertEqual(validator.validate(), [])


if __name__ == "__main__":
    unittest.main()
