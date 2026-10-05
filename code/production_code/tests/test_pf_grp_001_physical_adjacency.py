"""REG-SHELL-04/05 tests for explicit physical adjacency."""

from dataclasses import replace
import unittest

from production_code.group.physical_adjacency import (
    presentation_adjacency_matrix_diagnostic,
    quotient_physical_adjacency_certificate,
    quotient_physical_adjacency_matrix,
    quotient_physical_generator_images,
    universal_physical_neighbours,
)
from production_code.group.quotient_candidate import abelian_validation_candidate
from production_code.group.shell_registry import S8_GEOMETRIC, S8_PRESENTATION
from production_code.group.universal_cover import IDENTITY_MATRIX


class PhysicalAdjacencyTests(unittest.TestCase):
    def test_reg_shell_04_universal_degree_eight_from_geometric_shell(self):
        neighbours = universal_physical_neighbours(IDENTITY_MATRIX)
        self.assertEqual(len(neighbours), 8)
        self.assertEqual(len(set(neighbours)), 8)
        self.assertNotEqual(S8_GEOMETRIC, S8_PRESENTATION)

    def test_reg_shell_05_quotient_physical_adjacency(self):
        candidate = replace(
            abelian_validation_candidate(4),
            quotient_id="QVAL4_PHYSICAL_STRUCTURE_ONLY",
            phi8_permutation=None,
        )
        images = quotient_physical_generator_images(candidate)
        self.assertEqual(len(images), 8)
        self.assertEqual(len(set(images)), 8)
        matrix = quotient_physical_adjacency_matrix(candidate)
        self.assertTrue(all(sum(row) == 8 for row in matrix))
        certificate = quotient_physical_adjacency_certificate(candidate)
        self.assertEqual(certificate.shell_name, "S8_GEOMETRIC")
        self.assertTrue(certificate.passed)

    def test_presentation_diagnostic_is_explicit_and_not_physical_default(self):
        candidate = abelian_validation_candidate(4)
        self.assertEqual(presentation_adjacency_matrix_diagnostic(candidate), candidate.adjacency_matrix)
        self.assertNotEqual(quotient_physical_generator_images(candidate), candidate.s8_images)


if __name__ == "__main__":
    unittest.main()
