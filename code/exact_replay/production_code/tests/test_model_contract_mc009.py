"""Regression tests for MC-009."""
import unittest
from production_code.contract_rules.mc_009 import check
from production_code.model_contract import ContractViolation

def valid_config():
    target={"tracking_method":"riesz_projector_ancestry","max_projector_step_norm":0.7,"projector_error_margin":0.05,"on_step_failure":"refine_step"}
    for k in ["anchor_frozen","contour_frozen","rank_frozen","orbital_ancestry_frozen","layer_ancestry_frozen","symmetry_ancestry_frozen","representation_support_frozen"]: target[k]=True
    return {"target":target,"guards":{"eigenvalue_sorting":False,"nearest_energy_tracking":False}}

class ModelContractMC009Tests(unittest.TestCase):
    def test_riesz_tracking_passes(self): check(valid_config())
    def test_step_margin_is_fatal(self):
        c=valid_config(); c["target"]["max_projector_step_norm"]=0.98
        with self.assertRaisesRegex(ContractViolation,"error margin < 1"): check(c)
    def test_eigenvalue_sorting_is_fatal(self):
        c=valid_config(); c["guards"]["eigenvalue_sorting"]=True
        with self.assertRaisesRegex(ContractViolation,"sorting"): check(c)

if __name__ == "__main__": unittest.main()

