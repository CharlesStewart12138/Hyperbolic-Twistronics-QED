"""Regression tests for MC-012."""
import unittest
from production_code.contract_rules.mc_012 import check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"euclidean":{"Sigma":7,"hilbert_dimension":14,"interlayer_Tk":"full_radial_nonzero","extrema_domain":"full_2d_mbz"},"guards":{"five_state_in_production":False,"zero_interlayer_in_production":False},"validation":{"namespace_separate":True}}


class ModelContractMC012Tests(unittest.TestCase):
    def test_exact_supercell_passes(self): check(valid_config())
    def test_wrong_dimension_is_fatal(self):
        c=valid_config(); c["euclidean"]["hilbert_dimension"]=5
        with self.assertRaisesRegex(ContractViolation,"2\*Sigma"): check(c)
    def test_five_state_production_is_fatal(self):
        c=valid_config(); c["guards"]["five_state_in_production"]=True
        with self.assertRaisesRegex(ContractViolation,"validation-only"): check(c)


if __name__ == "__main__": unittest.main()

