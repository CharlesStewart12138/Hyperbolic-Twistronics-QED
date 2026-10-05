"""Regression tests for MC-005."""

import unittest

from production_code.contract_rules.mc_005 import check
from production_code.model_contract import ContractViolation


def valid_config() -> dict:
    return {"scan": {"curvature": {"coordinate": "kappa=-K=1/R^2", "domain": [0, "kappa_B"], "bolza_endpoint_exact": True, "interior_scope": "synthetic_metric_deformation", "grid_frozen_before_results": True}}, "guards": {"every_curvature_exact_bolza": False, "posthoc_curvature_grid": False}}


class ModelContractMC005Tests(unittest.TestCase):
    def test_scope_passes(self) -> None:
        check(valid_config())

    def test_false_exact_bolza_scope_is_fatal(self) -> None:
        config = valid_config(); config["guards"]["every_curvature_exact_bolza"] = True
        with self.assertRaisesRegex(ContractViolation, "exact Bolza"):
            check(config)

    def test_posthoc_grid_is_fatal(self) -> None:
        config = valid_config(); config["scan"]["curvature"]["grid_frozen_before_results"] = False
        with self.assertRaisesRegex(ContractViolation, "frozen before"):
            check(config)


if __name__ == "__main__": unittest.main()

