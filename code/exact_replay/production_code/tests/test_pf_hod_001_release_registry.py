"""Serialization and scope-regression tests for the PF-HOD-001 release."""

import json
from pathlib import Path
import unittest

import yaml

from production_code.hodge.bolza_harmonic_basis import (
    HARMONIC_BASIS,
    SCOPE,
    nielsen_homology_matrix,
    standard_cohomology_in_geometric_dual,
)


ROOT = Path(__file__).resolve().parents[2]


class HarmonicBasisReleaseRegistryTests(unittest.TestCase):
    def test_registry_matches_executable_exact_data(self):
        registry = yaml.safe_load(
            (ROOT / "production_code/hodge/BOLZA_HARMONIC_TANGENT_BASIS.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(registry["scope"], SCOPE)
        self.assertEqual(tuple(registry["standard_cohomology_basis"]["ordered_basis"]), HARMONIC_BASIS)
        self.assertEqual(
            registry["geometric_homology_marking"]["standard_generators_in_geometric_coordinates"]["matrix"],
            [list(row) for row in nielsen_homology_matrix().tolist()],
        )
        self.assertEqual(
            registry["standard_cohomology_basis"]["geometric_dual_coordinates_M_inverse_transpose"],
            [list(row) for row in standard_cohomology_in_geometric_dual().tolist()],
        )
        self.assertTrue(registry["acceptance"]["passed"])
        self.assertFalse(registry["main_tex_modified"])

    def test_immutable_release_has_restricted_scope(self):
        release = json.loads(
            (ROOT / "production_code/config/freeze_records/PF-HOD-001-LOCAL-RELEASE.json").read_text(encoding="utf-8")
        )
        self.assertTrue(release["immutable_record"])
        self.assertEqual(release["status"], "Fixed")
        self.assertEqual(release["scope"], SCOPE)
        self.assertEqual(release["acceptance"], "PASSED")
        self.assertEqual(release["scope_boundary"]["general_nonabelian_Ad_rho"], "not asserted")
        self.assertFalse(release["scope_boundary"]["main_tex_modified"])

    def test_hodge_config_keeps_basis_release_intact(self):
        config = yaml.safe_load((ROOT / "production_code/config/hodge.yaml").read_text(encoding="utf-8"))
        basis = config["parameters"]["PF-HOD-001"]
        self.assertEqual(basis["status"], "fixed")
        self.assertEqual(basis["scope"], SCOPE)
        self.assertEqual(basis["transport"], "I_4")
        self.assertEqual(tuple(basis["ordered_basis"]), HARMONIC_BASIS)
        self.assertIn("PF-HOD-002", config["parameters"])


if __name__ == "__main__":
    unittest.main()

