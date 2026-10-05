"""Regression tests for MC-003."""

from __future__ import annotations

import unittest

from production_code.contract_rules.mc_003 import EXACT_KERNEL_FORM, check
from production_code.model_contract import ContractViolation


def valid_kernel_config() -> dict:
    return {
        "kernel": {
            "family": "exponential_full_distance",
            "formula": EXACT_KERNEL_FORM,
            "pair_policy": "all_frozen_support_pairs",
            "support_policy_frozen": True,
            "theta_derivative_orders": [0, 1, 2],
            "tail_certificate_orders": [0, 1, 2],
            "parameters_from_frozen_config": True,
        },
        "guards": {
            "first_shell_only": False,
            "nearest_interlayer_only": False,
            "same_label_pairing": False,
            "constant_interlayer_coupling": False,
        },
    }


class ModelContractMC003Tests(unittest.TestCase):
    def test_exact_full_kernel_passes(self) -> None:
        check(valid_kernel_config())

    def test_first_shell_is_fatal(self) -> None:
        config = valid_kernel_config()
        config["guards"]["first_shell_only"] = True
        with self.assertRaisesRegex(ContractViolation, "first_shell_only"):
            check(config)

    def test_missing_c2_tail_is_fatal(self) -> None:
        config = valid_kernel_config()
        config["kernel"]["tail_certificate_orders"] = [0, 1]
        with self.assertRaisesRegex(ContractViolation, "C0/C1/C2"):
            check(config)

    def test_same_label_pairing_is_fatal(self) -> None:
        config = valid_kernel_config()
        config["kernel"]["pair_policy"] = "same_label_only"
        with self.assertRaisesRegex(ContractViolation, "all allowed"):
            check(config)


if __name__ == "__main__":
    unittest.main()

