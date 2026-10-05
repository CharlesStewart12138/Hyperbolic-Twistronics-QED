from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GROUP = ROOT / "production_code" / "group"
DATA = ROOT / "data" / "production" / "global_direct_v2"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_tsv(path: Path):
    return dict(line.split("\t", 1) for line in path.read_text(encoding="utf-8").splitlines() if "\t" in line)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def test_axis_cutoff_exact_coefficients():
    # 1+2(3+2s)^2((2405+1700s)^2-1), s^2=2.
    def mul(x, y):
        return x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]
    r2 = mul((3, 2), (3, 2))
    c2 = mul((2405, 1700), (2405, 1700))
    product = mul(r2, (c2[0] - 1, c2[1]))
    assert (1 + 2 * product[0], 2 * product[1]) == (785_672_817, 555_554_576)


def test_exact_ball_empty_frontier_and_count():
    manifest = load_json(DATA / "axis6_exact_ball_manifest.json")
    assert manifest["complete"] is True
    assert manifest["checkpoint"]["frontier_elements"] == "0"
    assert manifest["checkpoint"]["visited_elements"] == "785639753"


def test_exact_ball_registry_size_contract():
    manifest = load_json(DATA / "axis6_exact_ball_manifest.json")
    assert manifest["registry_bytes"] == 24 + 147 * 785_639_753
    assert (DATA / "axis6_exact_ball.bin").stat().st_size == manifest["registry_bytes"]


def test_kernel_scan_complete():
    scan = parse_tsv(DATA / "product_kernel_scan_checkpoint.tsv")
    assert scan["complete"] == "1"
    assert scan["scanned_records"] == scan["total_records"] == "785639753"
    assert scan["kernel_elements"] == "736"
    assert scan["dangerous_elements"] == "0"


def test_kernel_candidate_archive_count_and_classification():
    with (DATA / "product_kernel_candidates.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 736
    assert {row["dangerous_le_6a_B"] for row in rows} == {"0"}
    assert min(float(row["translation_length_over_a_B"]) for row in rows) > 6.0


def test_independent_audit_passes():
    audit = load_json(GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_INDEPENDENT_AUDIT.json")
    assert audit["all_candidate_words_recompute_to_identity"] is True
    assert audit["all_candidate_trace_margins_strictly_positive_by_integer_radical_sign"] is True
    assert audit["classification"] == "GLOBAL-SYSTOLE-GT-6a_B-CERTIFIED"


def test_final_certificate_global_not_based_only():
    cert = load_json(GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.json")
    assert cert["classification"] == "GLOBAL-SYSTOLE-GT-6a_B-CERTIFIED"
    assert cert["scope"]["global_not_based_only"] is True
    assert cert["systole"]["proved_lower_bound"] == "sys(ker rho)>6a_B"


def test_pq14_pq16_promoted_only_after_global_scan():
    cert = load_json(GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.json")
    assert cert["quotient_gates"]["PQ_14_all_global_dangerous_classes_separated"] == "PASS"
    assert cert["quotient_gates"]["PQ_16_global_geometric_injectivity"] == "PASS_r_inj_global_gt_3a_B"
    assert cert["quotient_gates"]["numerical_matrix_free_feasibility"] == "NEXT_TASK_NOT_ASSUMED"


def test_certificate_output_hashes_are_current():
    cert = load_json(GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.json")
    paths = {
        "axis_ball_manifest": DATA / "axis6_exact_ball_manifest.json",
        "axis_ball_summary": DATA / "axis6_exact_ball_summary.tsv",
        "scan_checkpoint": DATA / "product_kernel_scan_checkpoint.tsv",
        "kernel_candidates": DATA / "product_kernel_candidates.tsv",
        "independent_audit": GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_INDEPENDENT_AUDIT.json",
    }
    assert cert["sha256"]["outputs"] == {name: sha256(path) for name, path in paths.items()}


def test_previous_resource_stop_preserved():
    old = load_json(GROUP / "GLOBAL_SYSTOLE_DIRECT_CERTIFICATE.json")
    cert = load_json(GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.json")
    assert old["classification"] == "GLOBAL-UNRESOLVED"
    assert "remains" in cert["prior_negative_result_preserved"]
