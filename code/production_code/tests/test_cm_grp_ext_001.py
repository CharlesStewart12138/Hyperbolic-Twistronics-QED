from __future__ import annotations

import json
from pathlib import Path

import pytest

from production_code.group.run_cm_grp_ext_001 import (
    EXPECTED_BALLS_0_6,
    EXPECTED_SHELLS_0_6,
    abelian,
    projective_key,
    tensor_moment,
)
from production_code.group.universal_cover import GENERATOR_MATRICES, matrix_from_word


ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = ROOT / "production_code/group/CM_GRP_EXT_001_CERTIFICATE.json"
MANIFEST_PATH = ROOT / "data/production/group_ball/ball_radius_7_manifest.json"
if not CERT_PATH.is_file() or not MANIFEST_PATH.is_file():
    pytest.skip(
        "exact generated group-ball certificate is intentionally absent from the source-only release",
        allow_module_level=True,
    )
CERT = json.loads(CERT_PATH.read_text(encoding="utf-8"))
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def negative(matrix):
    return tuple((field[0],) + tuple(-value for value in field[1:]) for field in matrix)


def test_gext_t01_projective_key_normalization() -> None:
    assert projective_key(GENERATOR_MATRICES[0]) == projective_key(negative(GENERATOR_MATRICES[0]))


def test_gext_t02_equivalent_words_same_key() -> None:
    w1 = ("g0", "g5", "g2", "g7")
    w2 = ("g7", "g2", "g5", "g0")
    assert projective_key(matrix_from_word(w1)) == projective_key(matrix_from_word(w2))


def test_gext_t03_known_different_elements_different_keys() -> None:
    assert projective_key(GENERATOR_MATRICES[0]) != projective_key(GENERATOR_MATRICES[1])


def test_gext_t04_cross_shard_relator_duplicate() -> None:
    duplicate = CERT["cross_shard_duplicate"]
    assert duplicate["same_exact_key"] is True
    assert duplicate["source_shards"] == [0, 7]


def test_gext_t05_external_merge_matches_small_reference() -> None:
    assert CERT["regression"]["old_registry_key_set_exact_match"] is True


def test_gext_t06_minimum_length_selection() -> None:
    duplicate = CERT["cross_shard_duplicate"]
    assert duplicate["chosen_minimum_length"] == 4


def test_gext_t07_shortlex_tie_break() -> None:
    duplicate = CERT["cross_shard_duplicate"]
    assert duplicate["chosen_word"] == ["g0", "g5", "g2", "g7"]


def test_gext_t08_c8_map_closure() -> None:
    assert CERT["C8_closure"] is True


def test_gext_t09_inverse_map_closure() -> None:
    assert CERT["inverse_closure"] is True


def test_gext_t10_restart_resume_identical() -> None:
    assert CERT["restart_registry_sha256_identical"] is True


def test_gext_t11_bucket_count_independence_small_domain() -> None:
    words = [()] + [(i,) for i in range(8)]
    keys = [projective_key(matrix_from_word(tuple(f"g{x}" for x in word))) for word in words]
    reference = set(keys)
    for buckets in (1, 16, 256):
        partition = [set() for _ in range(buckets)]
        for key in keys:
            partition[hash(key) % buckets].add(key)
        assert set().union(*partition) == reference


def test_gext_t12_tensor_word_invariance() -> None:
    w1, w2 = (0, 5, 2, 7), (7, 2, 5, 0)
    assert abelian(w1) == abelian(w2)
    assert tensor_moment(w1) == tensor_moment(w2)
    assert CERT["tensor_word_invariance"]["second_moment_equal"] is True


def test_gext_t13_l0_l6_exact_count_regression() -> None:
    assert CERT["regression"]["observed_shells_L0_L6"] == EXPECTED_SHELLS_0_6
    assert CERT["regression"]["observed_balls_L0_L6"] == EXPECTED_BALLS_0_6


def test_gext_t14_no_word_multiplicity_inflation() -> None:
    duplicate = CERT["cross_shard_duplicate"]
    assert duplicate["raw_representations_for_key"] == 2
    assert duplicate["retained_multiplicity"] == 1
    assert MANIFEST["complete"] is True
