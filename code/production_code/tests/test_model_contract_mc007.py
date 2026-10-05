"""Regression tests for MC-007."""

import unittest

from production_code.contract_rules.mc_007 import check
from production_code.model_contract import ContractViolation


def valid_config() -> dict:
    return {"quotient": {"order": 6}, "representation": {"irrep_dimensions": [1, 1, 2], "every_inequivalent_irrep": True, "explicit_matrices": True, "regular_multiplicity_rule": "d_rho", "normalized_weight_rule": "d_rho^2/|Q_N|", "character_gram_verified": True, "direct_block_spectrum_verified": True}, "guards": {"abelian_only_as_full": False, "character_only_projectors": False, "selected_irreps_only": False, "equal_irrep_weighting": False}}


class ModelContractMC007Tests(unittest.TestCase):
    def test_complete_registry_passes(self) -> None: check(valid_config())
    def test_degree_square_failure_is_fatal(self) -> None:
        config = valid_config(); config["representation"]["irrep_dimensions"] = [1, 1]
        with self.assertRaisesRegex(ContractViolation, "sum d_rho"):
            check(config)
    def test_abelian_only_is_fatal(self) -> None:
        config = valid_config(); config["guards"]["abelian_only_as_full"] = True
        with self.assertRaisesRegex(ContractViolation, "abelian_only"):
            check(config)
    def test_equal_weights_are_fatal(self) -> None:
        config = valid_config(); config["representation"]["normalized_weight_rule"] = "equal_by_irrep"
        with self.assertRaisesRegex(ContractViolation, "d_rho"):
            check(config)


if __name__ == "__main__": unittest.main()

