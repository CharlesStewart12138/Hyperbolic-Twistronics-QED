"""Regression tests for MC-001."""

from __future__ import annotations

import copy
import unittest

from production_code.model_contract import (
    EXACT_HYPERBOLIC_BLOCK_FORM,
    ContractViolation,
    check_mc_001,
)


def valid_config() -> dict:
    return {
        "run_type": "production",
        "model": {
            "kind": "exact_finite_quotient_hyperbolic_bilayer",
            "layers": 2,
            "orbitals_per_site": 1,
        },
        "quotient": {"order": 7},
        "hamiltonian": {
            "dimension": 14,
            "intralayer_block_shape": [7, 7],
            "interlayer_block_shape": [7, 7],
            "block_form": EXACT_HYPERBOLIC_BLOCK_FORM,
            "hermiticity_verified": True,
        },
        "guards": {
            "validation_fixture": False,
            "first_shell_only": False,
            "toy_2x2": False,
            "scalar_self_energy": False,
        },
    }


class ModelContractMC001Tests(unittest.TestCase):
    def test_exact_contract_passes(self) -> None:
        check_mc_001(valid_config())

    def test_dimension_mismatch_is_fatal(self) -> None:
        config = valid_config()
        config["hamiltonian"]["dimension"] = 12
        with self.assertRaisesRegex(ContractViolation, "dimension must equal"):
            check_mc_001(config)

    def test_validation_fixture_is_fatal(self) -> None:
        config = valid_config()
        config["guards"]["validation_fixture"] = True
        with self.assertRaisesRegex(ContractViolation, "validation_fixture"):
            check_mc_001(config)

    def test_first_shell_is_fatal(self) -> None:
        config = valid_config()
        config["guards"]["first_shell_only"] = True
        with self.assertRaisesRegex(ContractViolation, "first_shell_only"):
            check_mc_001(config)

    def test_wrong_block_form_is_fatal(self) -> None:
        config = valid_config()
        config["hamiltonian"]["block_form"] = "effective_2x2"
        with self.assertRaisesRegex(ContractViolation, "block form"):
            check_mc_001(config)

    def test_input_is_not_mutated(self) -> None:
        config = valid_config()
        before = copy.deepcopy(config)
        check_mc_001(config)
        self.assertEqual(config, before)


if __name__ == "__main__":
    unittest.main()
