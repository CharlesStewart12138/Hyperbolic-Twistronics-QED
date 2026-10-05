"""Regression tests for MC-004."""

from __future__ import annotations

import unittest

from production_code.contract_rules.mc_004 import check
from production_code.model_contract import ContractViolation


def valid_quotient_config() -> dict:
    return {
        "quotient": {
            "identifier": "unit-test-normal-quotient",
            "provenance": "production_parameter_freeze",
            "normal_subgroup_verified": True,
            "generator_images_archived": True,
            "multiplication_table_archived": True,
            "surface_relation_verified": True,
            "right_regular_action_verified": True,
            "injectivity_radius_certified": True,
            "order": 8,
            "injectivity_radius": 3.0,
            "c8_compatible": False,
            "bipartite": False,
        },
        "kernel": {"cutoff_distance": 2.0},
        "claims": {"c8_exact": False, "bipartite_benchmark": False},
        "guards": {"validation_quotient_reused": False, "graph_only_quotient": False},
    }


class ModelContractMC004Tests(unittest.TestCase):
    def test_certified_quotient_passes(self) -> None:
        check(valid_quotient_config())

    def test_validation_reuse_is_fatal(self) -> None:
        config = valid_quotient_config()
        config["guards"]["validation_quotient_reused"] = True
        with self.assertRaisesRegex(ContractViolation, "validation quotient"):
            check(config)

    def test_cutoff_beyond_injectivity_is_fatal(self) -> None:
        config = valid_quotient_config()
        config["kernel"]["cutoff_distance"] = 3.0
        with self.assertRaisesRegex(ContractViolation, "D_c < r_inj"):
            check(config)

    def test_unverified_c8_claim_is_fatal(self) -> None:
        config = valid_quotient_config()
        config["claims"]["c8_exact"] = True
        with self.assertRaisesRegex(ContractViolation, "C8"):
            check(config)


if __name__ == "__main__":
    unittest.main()

