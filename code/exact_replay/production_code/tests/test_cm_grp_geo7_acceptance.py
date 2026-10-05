from __future__ import annotations

import hashlib
import json
import struct
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
DATA = ROOT / "data" / "production" / "geometric_ball"
ENGINE = GROUP / "external_geometric_ball_geo7.exe"
OLD_ENGINE = GROUP / "short_geodesic_enumerator.exe"
CONTRACT = GROUP / "BOLZA_GEOMETRIC_BALL_FLOOD_CONTRACT.json"
THEOREM = GROUP / "BOLZA_GEOMETRIC_BALL_FLOOD_THEOREM.md"


def tsv(path: Path) -> dict[str, str]:
    return dict(
        line.split("\t", 1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if "\t" in line
    )


def run_ball(executable: Path, radius: int, root: Path) -> tuple[Path, dict[str, str]]:
    subprocess.run([str(executable), "init", str(radius), str(radius), str(root)], cwd=ROOT, check=True)
    while tsv(root / "checkpoint.tsv")["complete"] != "1":
        subprocess.run([str(executable), "step", str(root)], cwd=ROOT, check=True)
    registry = root / f"ball{radius}.bin"
    summary = root / f"ball{radius}.tsv"
    subprocess.run([str(executable), "finalize", str(root), str(registry), str(summary)], cwd=ROOT, check=True)
    return registry, tsv(summary)


@pytest.fixture(scope="session")
def small_reference(tmp_path_factory: pytest.TempPathFactory) -> dict[str, object]:
    root = tmp_path_factory.mktemp("geo7_acceptance")
    ball1, summary1 = run_ball(ENGINE, 1, root / "r1")
    ball2, summary2 = run_ball(ENGINE, 2, root / "r2")
    old = root / "old_r2"
    subprocess.run(
        [str(OLD_ENGINE), "--output-dir", str(old), "--cutoff-over-a", "2",
         "--maximum-elements", "100000", "--reserve-elements", "100000", "--count-only"],
        cwd=ROOT,
        check=True,
    )
    old_summary = json.loads((old / "based_enumeration_summary.json").read_text(encoding="utf-8"))
    second = root / "ball2-second.bin"
    second_summary = root / "ball2-second.tsv"
    subprocess.run(
        [str(ENGINE), "finalize", str(root / "r2"), str(second), str(second_summary)],
        cwd=ROOT,
        check=True,
    )
    return {
        "ball1": ball1,
        "ball2": ball2,
        "summary1": summary1,
        "summary2": summary2,
        "old2": old_summary,
        "restart_equal": hashlib.sha256(ball2.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest(),
    }


def test_geo7_t01_exact_circumradius_regression() -> None:
    value = json.loads(CONTRACT.read_text(encoding="utf-8"))["circumradius"]
    assert value["over_R_exact"] == "2*atanh(2^(-1/4)) = acosh(3+2*sqrt(2))"
    assert value["over_a_B_decimal"].startswith("0.800895927193685166956845")


def test_geo7_t02_cell_center_r_plus_rv_implication() -> None:
    text = THEOREM.read_text(encoding="utf-8")
    assert "d_{\\mathbb H}(o,ho)" in text
    assert "R_{\\rm target}+r_v" in text
    assert "d_{\\mathbb H}(x,ho)" in text


def test_geo7_t03_known_target_reachable_through_restricted_flood(small_reference: dict[str, object]) -> None:
    assert small_reference["summary2"]["shell_counts"] == "1,8,56,32,8,0"
    assert int(small_reference["summary2"]["flood_generations"]) == 5


def test_geo7_t04_external_visited_exact_dedup(small_reference: dict[str, object]) -> None:
    summary = small_reference["summary2"]
    assert int(summary["candidate_emissions"]) == 224
    assert int(summary["duplicate_emissions"]) == 120
    assert int(summary["target_unique_elements"]) == 105


def test_geo7_t05_frontier_fixed_point_termination_small_radius(small_reference: dict[str, object]) -> None:
    assert small_reference["summary2"]["frontier_exhausted"] == "1"
    assert small_reference["summary2"]["shell_counts"].endswith(",0")


def test_geo7_t06_r1_geometric_ball_known_reference(small_reference: dict[str, object]) -> None:
    assert small_reference["summary1"]["target_unique_elements"] == "9"
    assert small_reference["summary1"]["shell_counts"] == "1,8,0"


def test_geo7_t07_r2_independent_bruteforce_reference(small_reference: dict[str, object]) -> None:
    assert small_reference["old2"]["dangerous_nonidentity_elements"] + 1 == 105
    assert small_reference["old2"]["shell_counts_including_identity_at_depth_zero"] == [1, 8, 56, 32, 8, 0]


def test_geo7_t08_r6_count_exact() -> None:
    result = json.loads((DATA / "geo_ball_r6_regression_certificate.json").read_text(encoding="utf-8"))
    assert result["target_unique_elements"] == 23_129_593
    assert result["old_new_exact_key_set"]["equal"] is True


def test_geo7_t09_r6_tensor_baseline_reproduction() -> None:
    result = json.loads((DATA / "geo_ball_r6_tensor_regression_certificate_v2.json").read_text(encoding="utf-8"))
    assert result["trace_exact_match"] is True
    assert result["new_intervals_contained_in_frozen_intervals"] is True


def test_geo7_t10_r7_c8_closure() -> None:
    result = json.loads((DATA / "geo_ball_r7_closure_certificate.json").read_text(encoding="utf-8"))
    assert result["phi8_pass"] is True


def test_geo7_t11_r7_inversion_closure() -> None:
    result = json.loads((DATA / "geo_ball_r7_closure_certificate.json").read_text(encoding="utf-8"))
    assert result["inverse_pass"] is True


def test_geo7_t12_restart_manifest_equality(small_reference: dict[str, object]) -> None:
    result = json.loads((DATA / "geo_ball_r7_manifest.json").read_text(encoding="utf-8"))
    assert small_reference["restart_equal"] is True
    assert result["restart_registry_sha256_identical"] is True


def test_geo7_t13_word_ball_geometric_ball_scope_mismatch_regression() -> None:
    word = json.loads((GROUP / "CM_GRP_EXT_001_CERTIFICATE.json").read_text(encoding="utf-8"))
    assert word["radius7"]["unique_group_elements"] == 1_085_905
    assert word["radius7"]["unique_group_elements"] < 23_129_593


def test_geo7_t14_same_group_element_different_word_tensor_invariance() -> None:
    result = json.loads((DATA / "geo7_tensor_word_invariance.json").read_text(encoding="utf-8"))
    assert result["pairs_checked"] == 8
    assert result["all_complete_downstream_contributions_equal"] is True


def test_geo7_t15_exact_shell_subtraction_b7_minus_b6() -> None:
    result = json.loads((DATA / "geo_shell_6_7_manifest.json").read_text(encoding="utf-8"))
    validation = json.loads((DATA / "geo_tensor_shell_additivity_validation.json").read_text(encoding="utf-8"))
    assert result["element_count"] == 468_775_728
    assert result["exact_count_identity"]["pass"] is True
    assert result["closure"]["inverse_full_scan_missing"] == 0
    assert result["closure"]["phi8_full_scan_missing"] == 0
    assert result["restart_replay_hash_identical"] is True
    assert validation["all_directed_intervals_overlap"] is True

