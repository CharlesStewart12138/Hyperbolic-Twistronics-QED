import json
import unittest

from production_code.group.bolza_canonical_engine import (
    BoundedCanonicalIndex,
    EXPECTED_BALLS,
    EXPECTED_SHELLS,
    OUT_JSON,
    build_certificate,
    main,
    matrix_id,
)
from production_code.group.universal_cover import IDENTITY_MATRIX, matrix_from_word


class CanonicalEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = BoundedCanonicalIndex.build(6)

    def test_frozen_counts(self):
        self.assertEqual(self.index.ball.shell_counts, EXPECTED_SHELLS)
        self.assertEqual(self.index.ball.ball_counts, EXPECTED_BALLS)

    def test_identity_is_unique_empty_word(self):
        self.assertEqual(self.index.canonical_word(IDENTITY_MATRIX), ())
        self.assertEqual(sum(m == IDENTITY_MATRIX for m in self.index.word_by_matrix), 1)

    def test_first_discovery_words_reconstruct_exactly(self):
        for element in self.index.ball.elements[::997]:
            self.assertEqual(matrix_from_word(element.representative), element.matrix)
            self.assertEqual(self.index.canonical_word(element.matrix), element.representative)

    def test_content_ids_are_deterministic(self):
        sample = self.index.ball.elements[12345].matrix
        self.assertEqual(matrix_id(sample), matrix_id(sample))
        self.assertEqual(len(matrix_id(sample)), 64)

    def test_scope_guard_rejects_unproved_depth(self):
        with self.assertRaises(ValueError):
            BoundedCanonicalIndex.build(7)

    def test_certificate_closes_all_regressions(self):
        cert = build_certificate()
        self.assertTrue(all(cert["tests"].values()))
        self.assertFalse(cert["next_gate"]["deep_proof_search_released"])

    def test_generated_certificate_round_trip(self):
        main()
        cert = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(cert["classification"], "BOUNDED_CANONICAL_ENGINE_CERTIFIED")
        self.assertEqual(cert["certified_unique_domain"]["elements"], 155577)


if __name__ == "__main__":
    unittest.main()
