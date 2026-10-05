from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "compact_quotient_search"


def rows() -> list[dict[str, str]]:
    with (DATA / "candidates.csv").open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_candidate_table_is_unique_and_complete_for_recorded_seeds() -> None:
    records = rows()
    assert len(records) == 133_920
    assert len({row["candidate_id"] for row in records}) == len(records)


def test_all_cheap_survivors_receive_terminal_based_failure() -> None:
    records = rows()
    based_fail = [row for row in records if row["CQ-09_based_dangerous_separation"] == "FAIL"]
    assert len(based_fail) == 96
    assert all(row["CQ-10_based_geometric_admissibility"] == "FAIL" for row in based_fail)
    assert not any(row["accept_reject"] == "CHEAP_SURVIVOR" for row in records)


def test_s8_kernel_orbit_cover_is_exact() -> None:
    with (DATA / "s8_based_results.tsv").open("r", encoding="utf-8", newline="") as handle:
        results = list(csv.DictReader(handle, delimiter="\t"))
    assert len(results) == 6
    assert sum(len(result["member_seed_indices"].split(",")) for result in results) == 48
    assert all(result["based_pass"] == "FAIL" for result in results)
    assert {int(result["first_kernel_depth"]) for result in results} <= {4, 6}


def test_pgl23_survivors_all_have_depth_six_witnesses() -> None:
    with (DATA / "pgl2_23_based_results.tsv").open("r", encoding="utf-8", newline="") as handle:
        results = list(csv.DictReader(handle, delimiter="\t"))
    assert len(results) == 48
    assert all(result["based_pass"] == "FAIL" for result in results)
    assert {int(result["first_kernel_depth"]) for result in results} == {6}


def test_prime_pgl_family_counts_are_frozen() -> None:
    counts = {}
    for prime in (17, 23, 31):
        summary = json.loads((DATA / f"pgl2_{prime}_search_summary.json").read_text(encoding="utf-8"))
        counts[prime] = summary["counters"]["cheap_survivors"]
        assert summary["counters"]["alpha_classes"] == 2
    assert counts == {17: 0, 23: 48, 31: 0}


def test_report_does_not_release_global_or_production() -> None:
    report = json.loads((ROOT / "production_code/group/COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.json").read_text(encoding="utf-8"))
    assert report["number_candidates_examined"] == 133_920
    assert report["number_passing_cheap_exact_gates"] == 96
    assert report["number_passing_based_dangerous_certificate"] == 0
    assert report["number_global_certified"] == 0
    assert report["production_quotient_found"] is False
    assert report["main_tex_modified"] is False
