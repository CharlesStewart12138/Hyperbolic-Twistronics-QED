"""PF-GOV-003 unit-convention freeze regression."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]


class ProductionUnitFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units = yaml.safe_load((ROOT / "production_code/config/model.yaml").read_text(encoding="utf-8"))["units"]

    def test_internal_matrix_quantities_are_angular_frequencies(self):
        for key in ["one_particle_matrix", "omega0", "intralayer_hopping_t", "interlayer_hopping_w"]:
            self.assertEqual(self.units[key], "rad_per_s")

    def test_second_quantized_energy_has_hbar(self):
        self.assertEqual(self.units["second_quantized_energy"], "hbar_times_one_particle_matrix")

    def test_display_conversion_is_explicit(self):
        display = self.units["display_frequency"]
        self.assertEqual(display["conversion_to_internal"], "multiply_by_2pi")
        self.assertIn("implicit_Hz_to_rad_per_s", self.units["forbidden"])


if __name__ == "__main__": unittest.main()

