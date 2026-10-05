"""Proof-completeness and global-rejection tests for the class-two p=5 family."""

import gzip
import json
from pathlib import Path

import numpy as np

from production_code.group.class2_p5_c8_family import (
    PHYSICAL_RELATOR,
    b3_survivors,
    invariant_relator_quotients,
    physical_vectors,
    rotation_matrix,
)


ROOT = Path(__file__).resolve().parents[2]


def words_b3():
    path = ROOT / "data" / "production" / "universal_cover" / "ball_radius_6_exact.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [tuple(int(x[1:]) for x in r["representative"]) for r in map(json.loads, stream) if r["minimum_geometric_word_length"] <= 3]


def test_rotation_has_exact_order_eight_and_inverse_shell() -> None:
    rotation = rotation_matrix()
    identity = np.eye(4, dtype=np.int64)
    assert np.array_equal(np.linalg.matrix_power(rotation, 8) % 5, identity)
    assert not any(np.array_equal(np.linalg.matrix_power(rotation, k) % 5, identity) for k in range(1, 8))
    vectors = physical_vectors()
    assert all(np.array_equal(vectors[j + 4], -vectors[j] % 5) for j in range(4))


def test_parameterization_is_complete_and_relator_exact() -> None:
    family = invariant_relator_quotients()
    assert len(family) == 22
    assert all(candidate.order == 31_250 for candidate in family)
    assert all(candidate.image(PHYSICAL_RELATOR) == (0, 0, 0, 0, 0, 0, 0) for candidate in family)


def test_exact_B3_has_sixteen_survivors() -> None:
    words = words_b3()
    assert len(words) == 457
    assert len(b3_survivors(words)) == 16


def test_final_certificate_rejects_every_survivor_globally() -> None:
    path = ROOT / "production_code" / "group" / "CLASS2_P5_C8_FAMILY_CERTIFICATE.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["classification"] == "PROOF_COMPLETE_FAMILY_EXHAUSTED_NO_GLOBAL_SURVIVOR"
    assert record["proof_complete_parameterization"]["C8_stable_and_relator_killing_subspaces"] == 22
    results = record["global_scan"]["candidate_results"]
    assert len(results) == 16
    assert all(item["dangerous_kernel_hits_le_6a_B"] > 0 for item in results)
    assert max(item["minimum_translation_length_over_a_B_in_registry"] for item in results) < 4.72
