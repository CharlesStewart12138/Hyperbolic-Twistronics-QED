"""Regression tests for MC-002."""

from __future__ import annotations

import copy
import unittest

from production_code.contract_rules.mc_002 import check
from production_code.model_contract import ContractViolation


def valid_geometry_config() -> dict:
    return {
        "geometry": {
            "metric": "poincare_disk_exact",
            "distance": "hyperbolic_geodesic",
            "twist_action": "bolza_isometry_g_theta",
            "paired_cover_rule": "subgroup_lift_minimization",
            "lift_invariance_verified": True,
            "local_uniqueness_certified": True,
        },
        "guards": {
            "graph_shortest_path": False,
            "euclidean_chord": False,
            "euclidean_minimum_image": False,
            "same_label_pairing": False,
            "heuristic_lift_cutoff": False,
        },
    }


class ModelContractMC002Tests(unittest.TestCase):
    def test_exact_geometry_passes(self) -> None:
        check(valid_geometry_config())

    def test_graph_distance_is_fatal(self) -> None:
        config = valid_geometry_config()
        config["guards"]["graph_shortest_path"] = True
        with self.assertRaisesRegex(ContractViolation, "graph_shortest_path"):
            check(config)

    def test_minimum_image_is_fatal(self) -> None:
        config = valid_geometry_config()
        config["geometry"]["paired_cover_rule"] = "euclidean_minimum_image"
        with self.assertRaisesRegex(ContractViolation, "subgroup lifts"):
            check(config)

    def test_uncertified_local_lift_is_fatal(self) -> None:
        config = valid_geometry_config()
        config["geometry"]["local_uniqueness_certified"] = False
        with self.assertRaisesRegex(ContractViolation, "local uniqueness"):
            check(config)

    def test_input_is_not_mutated(self) -> None:
        config = valid_geometry_config()
        before = copy.deepcopy(config)
        check(config)
        self.assertEqual(config, before)


if __name__ == "__main__":
    unittest.main()

