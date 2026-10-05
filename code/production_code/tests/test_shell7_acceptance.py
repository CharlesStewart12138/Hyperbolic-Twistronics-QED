from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "geometric_ball"


def tsv(path: Path) -> dict[str, str]:
    return dict(
        line.split("\t", 1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if "\t" in line
    )


def manifest() -> dict[str, object]:
    return json.loads((DATA / "geo_shell_6_7_manifest.json").read_text(encoding="utf-8"))


def test_shell7_t01_exact_b7_minus_b6_count_identity() -> None:
    value = manifest()
    assert value["element_count"] == 468_775_728
    assert value["exact_count_identity"]["expression"] == "23129593 + 468775728 = 491905321"
    assert value["exact_count_identity"]["pass"] is True


def test_shell7_t02_no_duplicate_exact_keys() -> None:
    value = manifest()
    replay = tsv(DATA / "geo_shell_6_7_replay.tsv")
    assert value["duplicate_exact_keys"] == 0
    assert replay["duplicate_exact_keys"] == "0"
    assert replay["bucket_strict_order_pass"] == "1"


def test_shell7_t03_shell_inverse_closure() -> None:
    closure = tsv(DATA / "geo_shell_6_7_inverse_closure.tsv")
    assert closure["input_count"] == "468775728"
    assert closure["input_missing_from_transform"] == "0"
    assert closure["transform_missing_from_input"] == "0"
    assert closure["exact_set_equal"] == "1"


def test_shell7_t04_shell_c8_closure() -> None:
    closure = tsv(DATA / "geo_shell_6_7_phi8_closure.tsv")
    assert closure["input_count"] == "468775728"
    assert closure["input_missing_from_transform"] == "0"
    assert closure["transform_missing_from_input"] == "0"
    assert closure["exact_set_equal"] == "1"


def test_shell7_t05_restart_resume_same_hash() -> None:
    value = manifest()
    assert value["restart_replay_hash_identical"] is True
    assert value["registry_sha256"] == value["independent_bucket_replay_sha256"]
    assert value["closure"]["phi8_transform_buckets_complete"] == 256
    assert value["closure"]["phi8_comparison_buckets_complete"] == 256


def test_shell7_t06_r6_plus_shell_equals_r7() -> None:
    replay = tsv(DATA / "geo_shell_6_7_replay.tsv")
    assert int(replay["ball6_count"]) + int(replay["shell_count"]) == int(replay["ball7_count"])
    assert replay["count_identity_pass"] == "1"


def test_shell7_t07_shell_boundary_convention() -> None:
    contract = manifest()["distance_contract"]
    assert contract["B6"] == "d_H(o,g o) <= 6 a_B"
    assert contract["B7"] == "d_H(o,g o) <= 7 a_B"
    assert contract["shell"] == "6 a_B < d_H(o,g o) <= 7 a_B"
    assert contract["epsilon"] is None
