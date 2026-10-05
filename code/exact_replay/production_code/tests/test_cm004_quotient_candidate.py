"""CM-004 / T-Q01--T-Q11 and T-Q14 exact quotient tests."""

import tempfile
import unittest
from pathlib import Path

from production_code.group.quotient_candidate import (
    FiniteQuotientCandidate,
    abelian_validation_candidate,
    symmetric_group_3_relation_failure_candidate,
    symmetric_group_3_validation_candidate,
)
from production_code.group.quotient_search import append_inventory_row


class ExactQuotientCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qval = abelian_validation_candidate(4)
        cls.q2 = abelian_validation_candidate(2)
        cls.negative = symmetric_group_3_relation_failure_candidate()
        cls.qval_certificate = cls.qval.q0_certificate

    def test_t_q01_surface_relation_exact(self):
        self.assertTrue(self.qval_certificate["checks"]["surface_relation_exact"])
        self.assertFalse(self.negative.q0_certificate["checks"]["surface_relation_exact"])

    def test_existing_vt003_s3_relation_witness_is_a_quotient_but_not_q0_admissible(self):
        candidate = symmetric_group_3_validation_candidate()
        certificate = candidate.q0_certificate
        self.assertTrue(certificate["checks"]["surface_relation_exact"])
        self.assertTrue(certificate["checks"]["epimorphism_surjective"])
        self.assertFalse(certificate["checks"]["simple_degree_exactly_8"])
        self.assertFalse(certificate["checks"]["phi8_supplied"])
        self.assertEqual(certificate["q0_status"], "REJECT")

    def test_t_q02_inverse_generator_pairing(self):
        self.assertTrue(self.qval_certificate["checks"]["generator_inverse_pairing_exact"])
        for index in range(4):
            self.assertEqual(self.qval.multiply(self.qval.s8_images[index], self.qval.s8_images[index + 4]), self.qval.identity)

    def test_t_q03_connectedness(self):
        self.assertTrue(self.qval_certificate["checks"]["connected"])
        self.assertEqual(self.qval_certificate["checks"]["generated_vertex_count"], 256)
        self.assertTrue(self.qval_certificate["checks"]["epimorphism_surjective"])
        self.assertTrue(self.qval_certificate["checks"]["kernel_normal_by_homomorphism"])

    def test_right_regular_generator_actions_are_exact_permutations(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["right_regular_generator_maps_are_permutations"])
        for token in ("a1", "b1", "a2", "b2"):
            inverse = f"{token}_inv"
            forward = self.qval.right_regular_permutation(token)
            backward = self.qval.right_regular_permutation(inverse)
            self.assertTrue(all(backward[forward[index]] == index for index in range(self.qval.order)))

    def test_t_q04_degree_and_multiplicity_convention(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["weighted_degree_exactly_8"])
        self.assertTrue(checks["simple_degree_exactly_8"])
        q2_checks = self.q2.q0_certificate["checks"]
        self.assertTrue(q2_checks["weighted_degree_exactly_8"])
        self.assertFalse(q2_checks["simple_degree_exactly_8"])
        self.assertEqual(q2_checks["maximum_edge_multiplicity"], 2)

    def test_t_q05_algebraic_parity(self):
        self.assertTrue(self.qval_certificate["checks"]["algebraic_parity_exists"])

    def test_t_q06_graph_bipartiteness(self):
        self.assertTrue(self.qval_certificate["checks"]["graph_bipartite"])
        self.assertTrue(self.qval_certificate["checks"]["parity_and_graph_bipartiteness_agree"])

    def test_t_q07_phi8_descends(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["phi8_group_automorphism"])
        self.assertTrue(checks["phi8_order_exactly_8"])
        self.assertTrue(checks["phi8_preserves_s8_multiset"])

    def test_t_q08_adjacency_c8_covariance(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["adjacency_covariance_exact"])
        self.assertEqual(checks["adjacency_covariance_residual"], 0)

    def test_t_q09_adjacency_hermitian(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["adjacency_hermitian_exact"])
        self.assertEqual(checks["adjacency_hermiticity_residual"], 0)

    def test_t_q10_uniform_mode_plus_eight(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["uniform_mode_eigenvalue_plus_8"])
        self.assertEqual(checks["uniform_mode_residual"], 0)

    def test_t_q11_staggered_mode_minus_eight(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["staggered_mode_applicable"])
        self.assertTrue(checks["staggered_mode_eigenvalue_minus_8"])
        self.assertEqual(checks["staggered_mode_residual"], 0)

    def test_group_table_axioms_are_checked_exactly(self):
        checks = self.qval_certificate["checks"]
        self.assertTrue(checks["identity_exact"])
        self.assertTrue(checks["unique_two_sided_inverses"])
        self.assertTrue(checks["left_rows_are_permutations"])
        self.assertTrue(checks["associativity_exact"])

    def test_t_q14_serialization_round_trip_preserves_exact_group_data(self):
        serialized = self.qval.to_dict()
        restored = FiniteQuotientCandidate.from_dict(serialized)
        self.assertEqual(restored.to_dict(), serialized)
        self.assertEqual(restored.q0_certificate["q0_status"], "PASS")
        self.assertEqual(restored.adjacency_sha256, self.qval.adjacency_sha256)

    def test_inventory_is_append_only_per_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidates.csv"
            row = {"quotient_id": "fixture", "order_N": 1, "q0_status": "REJECT"}
            append_inventory_row(path, row)
            with self.assertRaisesRegex(ValueError, "append-only"):
                append_inventory_row(path, row)


if __name__ == "__main__":
    unittest.main()
