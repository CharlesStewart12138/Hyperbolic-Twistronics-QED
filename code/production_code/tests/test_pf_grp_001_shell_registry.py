"""Acceptance tests for the two-shell generator registry."""

from pathlib import Path
import unittest

from production_code.group.shell_registry import (
    S8_GEOMETRIC,
    S8_PRESENTATION,
    geometric_entry,
    presentation_entry,
    registry,
    validate_registry,
)


class ShellRegistryTests(unittest.TestCase):
    def test_reg_shell_01_names_and_distinction(self):
        self.assertEqual(S8_GEOMETRIC, tuple(f"g{i}" for i in range(8)))
        self.assertNotEqual(S8_GEOMETRIC, S8_PRESENTATION)

    def test_reg_shell_02_every_geometric_field(self):
        required = {
            "exact_matrix", "inverse", "standard_word", "phi8_image", "parity",
            "use_in_physical_nearest_neighbour_hamiltonian",
            "presentation_letter_is_physical_nearest_neighbour",
            "presentation_word_length", "geometric_word_length",
        }
        for index in range(8):
            entry = geometric_entry(index)
            self.assertTrue(required.issubset(entry))
            self.assertEqual(entry["parity"], 1)
            self.assertEqual(entry["geometric_word_length"], 1)
            self.assertTrue(entry["use_in_physical_nearest_neighbour_hamiltonian"])

    def test_reg_shell_03_presentation_is_algebraic_only(self):
        entries = [presentation_entry(token) for token in S8_PRESENTATION]
        self.assertFalse(any(entry["use_in_physical_nearest_neighbour_hamiltonian"] for entry in entries))
        lengths = {entry["id"]: entry["geometric_word_length"] for entry in entries}
        self.assertEqual(lengths["a2"], 3)
        self.assertEqual(lengths["b2"], 3)

    def test_registry_artifacts_and_validation(self):
        self.assertTrue(validate_registry())
        self.assertEqual(len(registry()["S8_GEOMETRIC"]), 8)
        root = Path(__file__).resolve().parents[1] / "group"
        self.assertTrue((root / "BOLZA_GENERATOR_SHELL_REGISTRY.yaml").is_file())
        self.assertTrue((root / "BOLZA_GENERATOR_SHELL_REGISTRY.md").is_file())


if __name__ == "__main__":
    unittest.main()
