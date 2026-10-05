"""Regression tests for MC-006."""

import unittest

from production_code.contract_rules.mc_006 import check
from production_code.model_contract import ContractViolation


def valid_config() -> dict:
    return {"twist": {"hilbert_space_policy": "fixed_fiber", "dimension_constant": True, "geometry_derivative_orders": [1, 2], "hamiltonian_derivative_orders": [1, 2], "projector_transport": "riesz_fixed_contour_with_refinement", "signed_internal_coordinate": True}, "guards": {"changing_commensurate_dimension": False, "eigenvalue_index_transport": False}}


class ModelContractMC006Tests(unittest.TestCase):
    def test_fixed_fiber_passes(self) -> None: check(valid_config())
    def test_changing_dimension_is_fatal(self) -> None:
        config = valid_config(); config["guards"]["changing_commensurate_dimension"] = True
        with self.assertRaisesRegex(ContractViolation, "changing commensurate"):
            check(config)
    def test_missing_second_derivative_is_fatal(self) -> None:
        config = valid_config(); config["twist"]["hamiltonian_derivative_orders"] = [1]
        with self.assertRaisesRegex(ContractViolation, "second Hamiltonian"):
            check(config)


if __name__ == "__main__": unittest.main()

