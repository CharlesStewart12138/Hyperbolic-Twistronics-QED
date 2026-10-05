"""RUN-002 integrated validation-package tests."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from validation_code.cleanroom_512.run002_validation_package import package_validation


ROOT = Path(__file__).resolve().parents[2]


class Run002ValidationPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = ROOT / "data/validation/cleanroom_512/dos_audit.json"
        if not fixture.is_file():
            raise unittest.SkipTest(
                "generated RUN-002 validation fixtures are absent from the source-only release"
            )
        cls.temporary = TemporaryDirectory()
        cls.summary = package_validation(
            ROOT,
            ROOT / "data/validation/cleanroom_512",
            Path(cls.temporary.name) / "RUN-002",
        )

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "temporary"):
            cls.temporary.cleanup()

    def test_all_three_fixtures_pass(self):
        self.assertEqual(self.summary["status"], "PASS")
        self.assertTrue(all(item["status"] == "PASS" for item in self.summary["fixtures"].values()))

    def test_cleanroom_registered_dimensions_and_rows(self):
        clean = self.summary["fixtures"]["cleanroom_512"]
        self.assertEqual(clean["dimension"], 512)
        self.assertEqual(clean["cdf_rows"], 2001)
        self.assertEqual(clean["broadening_rows"], 7203)

    def test_estimators_are_independently_registered(self):
        clean = self.summary["fixtures"]["cleanroom_512"]
        self.assertEqual((clean["kpm_moment_count"], clean["kpm_batches"], clean["kpm_probes_per_batch"]), (160, 4, 32))
        self.assertEqual((clean["slq_depth"], clean["slq_batches"], clean["slq_probes_per_batch"]), (64, 4, 32))

    def test_package_is_never_production_eligible(self):
        self.assertEqual(self.summary["run_type"], "validation")
        self.assertFalse(self.summary["production_eligible"])


if __name__ == "__main__":
    unittest.main()
