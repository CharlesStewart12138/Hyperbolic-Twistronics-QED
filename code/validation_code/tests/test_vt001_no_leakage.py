"""VT-001 production/validation isolation tests."""

from pathlib import Path
import unittest

from validation_code.governance.no_leakage import run_validation


ROOT = Path(__file__).resolve().parents[2]


class NoLeakageValidationTests(unittest.TestCase):
    def test_every_registered_fixture_is_rejected(self):
        report = run_validation(ROOT)
        self.assertTrue(report["passed"])
        self.assertEqual(report["rejected_cases"], report["forbidden_cases"])

    def test_validation_run_is_explicitly_namespaced(self):
        report = run_validation(ROOT)
        self.assertEqual(report["test_id"], "VT-001")
        self.assertEqual(report["criterion"], "Exact")


if __name__ == "__main__":
    unittest.main()
