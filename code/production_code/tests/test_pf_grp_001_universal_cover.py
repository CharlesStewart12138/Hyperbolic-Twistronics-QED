"""UC-01 through UC-04 universal-cover acceptance tests."""

import unittest

import sympy as sp

from production_code.group.bolza_interface import ALPHA as SYMBOLIC_ALPHA, BETA, ZETA8
from production_code.group.universal_cover import (
    GENERATOR_MATRICES,
    GEOMETRIC_RELATOR,
    IDENTITY_MATRIX,
    enumerate_ball,
    field_to_sympy,
    inverse_index,
    matrix_from_word,
    matrix_multiply,
)


class BolzaUniversalCoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ball = enumerate_ball(6)

    def test_uc_01_shell_one_has_exactly_eight_geometric_directions(self):
        self.assertEqual(self.ball.shell_counts[:2], (1, 8))
        self.assertEqual(len(set(GENERATOR_MATRICES)), 8)
        for index, (a, b) in enumerate(GENERATOR_MATRICES):
            self.assertEqual(sp.simplify(field_to_sympy(a) - SYMBOLIC_ALPHA), 0)
            self.assertEqual(sp.simplify(field_to_sympy(b) - BETA * ZETA8**index), 0)

    def test_uc_02_inverse_consistency(self):
        inverse_ids = inverse_index(self.ball)
        self.assertEqual(inverse_ids[0], 0)
        self.assertTrue(all(inverse_ids[inverse_ids[index]] == index for index in range(len(inverse_ids))))
        for index in range(8):
            self.assertEqual(matrix_multiply(GENERATOR_MATRICES[index], GENERATOR_MATRICES[(index + 4) % 8]), IDENTITY_MATRIX)

    def test_uc_03_word_matrix_identity_consistency(self):
        self.assertEqual(matrix_from_word(GEOMETRIC_RELATOR), IDENTITY_MATRIX)
        self.assertEqual(self.ball.shortest_relation_length, 8)
        self.assertEqual(len({element.matrix for element in self.ball.elements}), len(self.ball.elements))

    def test_uc_04_ball_counts_are_deterministic(self):
        self.assertEqual(self.ball.shell_counts, (1, 8, 56, 392, 2736, 19096, 133288))
        self.assertEqual(self.ball.ball_counts, (1, 9, 65, 457, 3193, 22289, 155577))
        repeat = enumerate_ball(4)
        self.assertEqual(repeat.shell_counts, self.ball.shell_counts[:5])
        self.assertEqual(repeat.ball_counts, self.ball.ball_counts[:5])
        self.assertEqual(tuple(element.matrix for element in repeat.elements),
                         tuple(element.matrix for element in self.ball.elements[:len(repeat.elements)]))


if __name__ == "__main__":
    unittest.main()

