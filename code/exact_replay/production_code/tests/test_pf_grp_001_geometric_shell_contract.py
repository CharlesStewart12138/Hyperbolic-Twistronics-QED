"""GSC01--GSC07 acceptance tests for the physical geometric shell."""

from pathlib import Path
import unittest

from production_code.group.geometric_shell_contract import (
    GEOMETRIC_SHELL,
    GEOMETRIC_TO_STANDARD_WORD,
    acceptance_rows,
    certificate,
)


class GeometricShellContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = certificate()

    def test_gsc01_side_sharing_nearest_neighbours(self):
        self.assertTrue(self.cert.gsc01_side_sharing_nearest_neighbours)

    def test_gsc02_eight_distinct_neighbours(self):
        self.assertEqual(GEOMETRIC_SHELL, tuple(f"g{i}" for i in range(8)))
        self.assertTrue(self.cert.gsc02_eight_distinct_neighbours)

    def test_gsc03_inverse_closed(self):
        self.assertTrue(self.cert.gsc03_inverse_closed)

    def test_gsc04_universal_centre_orbit_degree_eight(self):
        self.assertTrue(self.cert.gsc04_universal_centre_orbit_degree_eight)

    def test_gsc05_c8_cyclic_action(self):
        self.assertTrue(self.cert.gsc05_c8_cyclic_action)

    def test_gsc06_physical_88_resonator_graph(self):
        self.assertTrue(self.cert.gsc06_physical_88_resonator_graph)
        manuscript = (Path(__file__).resolve().parents[2] / "source_current_195" / "main.tex").read_text(encoding="utf-8")
        self.assertIn("\\label{eq:platform-eight-neighbour-maps}", manuscript)
        self.assertIn("universal \\(\\{8,8\\}\\) tessellation", manuscript)

    def test_gsc07_exact_nielsen_words(self):
        self.assertTrue(self.cert.gsc07_exact_nielsen_words)
        self.assertEqual(GEOMETRIC_TO_STANDARD_WORD[0], ("a1",))
        self.assertEqual(GEOMETRIC_TO_STANDARD_WORD[1], ("b1_inv",))
        self.assertEqual(GEOMETRIC_TO_STANDARD_WORD[2], ("a1_inv", "b1_inv", "a2"))
        self.assertEqual(GEOMETRIC_TO_STANDARD_WORD[7], ("b2", "b1", "a1"))

    def test_all_rows_pass(self):
        self.assertEqual([row["test_id"] for row in acceptance_rows()],
                         [f"GSC{i:02d}" for i in range(1, 8)])
        self.assertTrue(all(row["passed"] for row in acceptance_rows()))
        self.assertTrue(self.cert.passed)


if __name__ == "__main__":
    unittest.main()
