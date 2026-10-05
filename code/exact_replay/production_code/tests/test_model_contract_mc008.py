"""Regression tests for MC-008."""
import unittest
from production_code.contract_rules.mc_008 import check
from production_code.model_contract import ContractViolation

def valid_config():
    return {"projectors":{"construction":"explicit_matrix_riesz","idempotence_verified":True,"hermiticity_verified":True,"rank_verified":True,"contour_isolated":True,"representation_resolution_verified":True,"observables":["coherence","hodge","ldos","ancestry"]},"guards":{"character_only_observables":False,"power_sum_eigenvectors":False}}

class ModelContractMC008Tests(unittest.TestCase):
    def test_explicit_projectors_pass(self): check(valid_config())
    def test_character_only_is_fatal(self):
        c=valid_config(); c["guards"]["character_only_observables"]=True
        with self.assertRaisesRegex(ContractViolation,"characters"): check(c)
    def test_rank_check_is_required(self):
        c=valid_config(); c["projectors"]["rank_verified"]=False
        with self.assertRaisesRegex(ContractViolation,"rank_verified"): check(c)

if __name__ == "__main__": unittest.main()

