from __future__ import annotations

from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / "data" / "production" / "local_full_kernel"
GEO = ROOT / "data" / "production" / "geometric_ball"
HODGE = ROOT / "production_code" / "hodge"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_m7_t01_all_bucket_hashes_and_exact_shell_count() -> None:
    manifest = load(LOCAL / "M7_TENSOR_BUCKET_MANIFEST.json")
    assert manifest["status"] == "COMPLETE"
    assert manifest["buckets_complete"] == 256
    assert manifest["elements_consumed_complete"] == 468_775_728
    assert [entry["bucket"] for entry in manifest["entries"]] == list(range(256))
    for entry in manifest["entries"]:
        bucket = entry["bucket"]
        assert digest(LOCAL / "m7_tensor_buckets" / f"bucket-{bucket:03d}.json") == entry["tensor_json_sha256"]
        assert digest(LOCAL / "m7_tensor_buckets" / f"bucket-{bucket:03d}.acc.tsv") == entry["accumulator_sha256"]


def test_m7_t02_independent_accumulator_expansion_matches_bucket_json() -> None:
    raw = dict(
        line.split("\t", 1)
        for line in (LOCAL / "m7_tensor_buckets" / "bucket-000.acc.tsv").read_text(encoding="utf-8").splitlines()
        if "\t" in line
    )
    bucket = load(LOCAL / "m7_tensor_buckets" / "bucket-000.json")
    mapping = ((0, 1, 2, 3), (1, 4, 5, 6), (2, 5, 7, 8), (3, 6, 8, 9))
    for i in range(4):
        for j in range(4):
            slot = mapping[i][j]
            assert bucket["partial_tensor_entrywise_lower"][i][j] == raw[f"lower_{slot}"]
            assert bucket["partial_tensor_entrywise_upper"][i][j] == raw[f"upper_{slot}"]


def test_m7_t03_exact_word_invariance() -> None:
    word = load(GEO / "geo7_tensor_word_invariance.json")
    assert word["pairs_checked"] == 8
    assert word["all_complete_downstream_contributions_equal"] is True
    assert all(pair["full_weighted_contribution_equal"] for pair in word["pairs"])


def test_m7_t04_bucket_load_order_independence() -> None:
    merge = load(LOCAL / "M7_TENSOR_MERGE_MANIFEST.json")
    assert merge["acceptance"]["reverse_load_outputs_byte_identical"] is True
    assert merge["output_hashes"] == merge["reverse_load_output_hashes"]
    assert merge["merge_tree"]["levels"] == list(range(1, 9))
    assert merge["merge_tree"]["nodes"] == 255


def test_m7_t05_restart_checkpoint_is_complete_and_nonduplicating() -> None:
    manifest = load(LOCAL / "M7_TENSOR_BUCKET_MANIFEST.json")
    merge = load(LOCAL / "M7_TENSOR_MERGE_MANIFEST.json")
    assert manifest["restart_events"] == 1
    assert merge["bucket_hash_validation"] == {
        "bad_buckets": [],
        "files_checked": 512,
        "records_checked": 256,
    }
    assert merge["acceptance"]["no_duplicate_bucket"] is True
    assert merge["acceptance"]["no_omitted_bucket"] is True


def test_m7_t06_directed_serializer_and_full_tensor_intervals() -> None:
    full = load(LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.json")
    assert full["mpfr_precision_bits"] == 192
    assert "RNDD" in full["directed_rounding_contract"]
    assert "RNDU" in full["directed_rounding_contract"]
    for matrix in (full["partial_tensor_entrywise_lower"], full["partial_tensor_entrywise_upper"]):
        for row in matrix:
            for value in row:
                digits = re.sub(r"[^0-9]", "", value.lower().split("e", 1)[0]).lstrip("0")
                assert len(digits) >= 70
    for i in range(4):
        for j in range(4):
            assert Decimal(full["partial_tensor_entrywise_lower"][i][j]) <= Decimal(full["partial_tensor_entrywise_upper"][i][j])


def test_m7_t07_integer_count_and_trace_identities() -> None:
    shell = load(GEO / "geo_shell_r6_r7_tensor.json")
    m6 = load(LOCAL / "EXACT_BALL6_TENSOR_PARTIAL.json")
    m7 = load(LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.json")
    assert shell["elements_consumed"] + m6["dangerous_nonidentity_elements"] + 1 == m7["elements_consumed"] == 491_905_321
    assert shell["unweighted_integer_trace_sum"] + m6["unweighted_integer_trace_sum"] == m7["unweighted_integer_trace_sum"] == 8_424_123_008


def test_m7_t08_exact_symmetry_and_closure_contracts() -> None:
    shell = load(GEO / "geo_shell_6_7_manifest.json")
    full = load(LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.json")
    assert shell["duplicate_exact_keys"] == 0
    assert shell["closure"]["inverse_full_scan_missing"] == 0
    assert shell["closure"]["phi8_full_scan_missing"] == 0
    for key in ("partial_tensor_entrywise_lower", "partial_tensor_entrywise_upper"):
        matrix = full[key]
        assert all(matrix[i][j] == matrix[j][i] for i in range(4) for j in range(4))


def test_m7_t09_frozen_m6_regression_hash() -> None:
    assert digest(LOCAL / "EXACT_BALL6_TENSOR_PARTIAL.json") == "9fc3ca5d207d36dfea3e5714609421447ad8d3fed30b0ad3c60276feed658819"
    status = load(LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.status.json")
    assert status["m6_overwritten"] is False
    assert (LOCAL / "EXACT_BALL7_TENSOR_PARTIAL.pre_stream.status.json").exists()


def test_m7_t10_tail_scope_classification_and_post_decision() -> None:
    tail = load(LOCAL / "EXACT_BALL7_TENSOR_TAIL.json")
    result = load(HODGE / "CM_047_NP_M7_STREAM_RESULT.json")
    decision = load(HODGE / "CM_047_NP_POST_M7_DECISION.json")
    assert tail["first_omitted_shell"] == 7
    assert "d>7a_B" in tail["bound"].replace(" ", "")
    assert result["classification"] in {
        "TENSOR-NO-ROOT-CERTIFIED",
        "TENSOR-ROOT-CANDIDATE",
        "TENSOR-ROOT-CERTIFIED",
        "TENSOR-UNRESOLVED",
    }
    assert result["classification"] == "TENSOR-UNRESOLVED"
    lo, hi = map(Decimal, result["common_root_necessary_interval"])
    assert lo <= hi
    assert result["existence_isolation_transversality_certified"] is False
    assert decision["automatic_case"] == "CASE_C_ANALYTIC_TAIL_DOMINATES"
    assert decision["m8_released"] is False
    assert decision["next_task"]["task_id"] == "CM-047-NP-M7-ANALYTIC-TAIL"
