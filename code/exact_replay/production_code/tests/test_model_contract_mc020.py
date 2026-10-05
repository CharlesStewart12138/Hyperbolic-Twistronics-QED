"""Regression tests for MC-020."""
import unittest
from production_code.contract_rules.mc_020 import DIAGNOSTICS, check
from production_code.model_contract import ContractViolation


def valid_config():
    return {"spectroscopy":{"greens_formula":"[Omega*I-H+i*Gamma/2]^-1","scattering_formula":"I-i*K^dagger*G_R*K","ports_calibrated":True,"loss_frozen":True,"frequency_grid_frozen":True,"gamma_psd_verified":True,"diagnostics":sorted(DIAGNOSTICS)},"guards":{"scalar_linewidth":False,"magnitude_only":False,"unspecified_ports":False}}


class ModelContractMC020Tests(unittest.TestCase):
    def test_full_spectroscopy_passes(self): check(valid_config())
    def test_non_psd_loss_is_fatal(self):
        c=valid_config(); c["spectroscopy"]["gamma_psd_verified"]=False
        with self.assertRaisesRegex(ContractViolation,"positive semidefinite"): check(c)
    def test_magnitude_only_is_fatal(self):
        c=valid_config(); c["guards"]["magnitude_only"]=True
        with self.assertRaisesRegex(ContractViolation,"magnitude_only"): check(c)


if __name__ == "__main__": unittest.main()

