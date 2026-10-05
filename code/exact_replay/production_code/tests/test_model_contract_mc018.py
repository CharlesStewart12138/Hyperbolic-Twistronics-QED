"""Regression tests for MC-018."""
import unittest
from production_code.contract_rules.mc_018 import check
from production_code.model_contract import ContractViolation


def valid_config():
    fold={"outcome":"certified_fold","same_point_F_zero":True,"same_point_dtheta_F_zero":True,"nonzero_dkappa_F":True,"nonzero_dtheta2_F":True,"interval_newton_unique":True,"branch_ancestry_verified":True,"interior_margins_verified":True,"square_root_law_verified":True}
    return {"fold":fold,"guards":{"grid_minimum_as_fold":False,"endpoint_as_fold":False}}


class ModelContractMC018Tests(unittest.TestCase):
    def test_certified_fold_passes(self): check(valid_config())
    def test_certified_absence_passes(self):
        c={"fold":{"outcome":"no_certified_fold","failure_certificate":"interval boxes exhausted"},"guards":{"grid_minimum_as_fold":False,"endpoint_as_fold":False}}
        check(c)
    def test_grid_minimum_is_fatal(self):
        c=valid_config(); c["guards"]["grid_minimum_as_fold"]=True
        with self.assertRaisesRegex(ContractViolation,"grid minimum"): check(c)


if __name__ == "__main__": unittest.main()

