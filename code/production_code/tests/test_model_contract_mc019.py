"""Regression tests for MC-019."""
import unittest
from production_code.contract_rules.mc_019 import ORDERS, PERTURBATIONS, check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"robustness":{"rebuild_full_hamiltonian_each_sample":True,"perturbations":sorted(PERTURBATIONS),"uniform_loss_separate":True,"nonuniform_loss_separate":True,"derivative_checks":sorted(ORDERS)},"guards":{"surrogate_hamiltonian":False,"scalar_noise_only":False,"linewidth_postprocessing":False}}


class ModelContractMC019Tests(unittest.TestCase):
    def test_full_ensemble_passes(self): check(valid_config())
    def test_surrogate_is_fatal(self):
        c=valid_config(); c["guards"]["surrogate_hamiltonian"]=True
        with self.assertRaisesRegex(ContractViolation,"surrogate"): check(c)
    def test_missing_multimode_is_fatal(self):
        c=valid_config(); c["robustness"]["perturbations"].remove("multimode")
        with self.assertRaisesRegex(ContractViolation,"incomplete"): check(c)


if __name__ == "__main__": unittest.main()

