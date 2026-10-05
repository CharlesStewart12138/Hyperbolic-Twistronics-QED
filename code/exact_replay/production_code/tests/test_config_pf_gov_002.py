"""PF-GOV-002 exact model-class freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class ProductionModelClassFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = yaml.safe_load((ROOT / "production_code/config/model.yaml").read_text(encoding="utf-8"))["model_class"]

    def test_hyperbolic_class_is_complete(self):
        hyper = self.model["production_hyperbolic"]
        self.assertEqual((hyper["layers"], hyper["orbitals_per_site"], hyper["intralayer_degree"]), (2, 1, 8))
        self.assertEqual(hyper["hamiltonian"], "full_2N_bilayer_block_matrix")
        self.assertEqual(hyper["representation_scope"], "every_inequivalent_irrep")

    def test_euclidean_class_is_exact(self):
        euclidean = self.model["production_euclidean"]
        self.assertEqual(euclidean["hamiltonian"], "full_2Sigma_bilayer_Bloch_matrix")
        self.assertEqual(euclidean["extrema_domain"], "full_2d_mini_Brillouin_zone")

    def test_reduced_models_are_validation_only(self):
        validation = set(self.model["validation_only"])
        self.assertTrue({"square_five_state", "first_shell_hyperbolic", "zero_interlayer_folding"}.issubset(validation))
        self.assertNotIn("five_state_only", {self.model["production_hyperbolic"]["hamiltonian"], self.model["production_euclidean"]["hamiltonian"]})


if __name__ == "__main__":
    unittest.main()
