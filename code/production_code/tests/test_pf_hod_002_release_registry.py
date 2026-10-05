"""Serialization and scope-regression tests for PF-HOD-002."""

import json
from pathlib import Path
import unittest

import sympy as sp
import yaml

from production_code.hodge.bolza_hodge_metric import SCOPE, hodge_metric_standard


ROOT = Path(__file__).resolve().parents[2]


def _parse_exact(value: object) -> sp.Expr:
    return sp.sympify(str(value), locals={"sqrt": sp.sqrt})


class HodgeMetricReleaseRegistryTests(unittest.TestCase):
    def test_registry_metric_matches_executable_matrix(self):
        registry = yaml.safe_load((ROOT / "production_code/hodge/BOLZA_HODGE_METRIC.yaml").read_text(encoding="utf-8"))
        serialized = registry["hodge_metric_on_cohomology"]["matrix"]
        matrix = sp.ImmutableMatrix([[_parse_exact(value) for value in row] for row in serialized])
        self.assertEqual(matrix, hodge_metric_standard())
        self.assertEqual(registry["scope"], SCOPE)
        self.assertTrue(registry["hodge_metric_on_cohomology"]["positive_definite"])
        self.assertFalse(registry["hodge_metric_on_cohomology"]["equals_identity"])
        self.assertTrue(registry["acceptance"]["passed"])
        self.assertFalse(registry["claim_boundary"]["main_tex_modified"])

    def test_immutable_release_preserves_claim_boundary(self):
        release = json.loads(
            (ROOT / "production_code/config/freeze_records/PF-HOD-002-LOCAL-RELEASE.json").read_text(encoding="utf-8")
        )
        self.assertTrue(release["immutable_record"])
        self.assertEqual(release["status"], "Fixed")
        self.assertEqual(release["scope"], SCOPE)
        self.assertTrue(release["frozen_value"]["positive_definite"])
        self.assertFalse(release["frozen_value"]["identity_metric"])
        self.assertEqual(release["scope_boundary"]["general_nonabelian_Ad_rho"], "not asserted")
        self.assertFalse(release["scope_boundary"]["main_tex_modified"])

    def test_hodge_config_keeps_root_tail_task_unfrozen(self):
        config = yaml.safe_load((ROOT / "production_code/config/hodge.yaml").read_text(encoding="utf-8"))
        metric = config["parameters"]["PF-HOD-002"]
        self.assertEqual(metric["status"], "fixed")
        self.assertEqual(metric["scope"], SCOPE)
        self.assertTrue(metric["positive_definite"])
        self.assertFalse(metric["identity_metric"])
        self.assertIsNone(config["parameters"]["PF-HOD-004"])


if __name__ == "__main__":
    unittest.main()

