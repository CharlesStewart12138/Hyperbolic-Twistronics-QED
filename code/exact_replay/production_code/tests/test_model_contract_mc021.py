"""Regression tests for MC-021."""
import unittest
from production_code.contract_rules.mc_021 import FROZEN_INPUTS, check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"qubit":{"self_energy_formula":"V_q*G_gamma_R*V_q^dagger","target_projection_after_remainder_bound":True,"frozen_inputs":sorted(FROZEN_INPUTS),"dispersive_margins_verified":True,"gamma_mediated_psd_verified":True},"guards":{"target_only_self_energy":False,"scalar_g":False,"unresolved_poles":False}}


class ModelContractMC021Tests(unittest.TestCase):
    def test_full_qubit_resolvent_passes(self): check(valid_config())
    def test_target_only_is_fatal(self):
        c=valid_config(); c["guards"]["target_only_self_energy"]=True
        with self.assertRaisesRegex(ContractViolation,"target_only"): check(c)
    def test_missing_remainder_bound_is_fatal(self):
        c=valid_config(); c["qubit"]["target_projection_after_remainder_bound"]=False
        with self.assertRaisesRegex(ContractViolation,"remainder bound"): check(c)


if __name__ == "__main__": unittest.main()

