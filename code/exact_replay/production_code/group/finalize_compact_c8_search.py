"""Finalize the completed direct-equivariant compact quotient search classes."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production" / "compact_quotient_search"
GROUP = ROOT / "production_code" / "group"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    csv_path = DATA / "candidates.csv"
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames
    if fieldnames is None or len(rows) != 133_920:
        raise AssertionError(f"candidate table drift: {len(rows)}")

    s8_results = read_tsv(DATA / "s8_based_results.tsv")
    pgl23_results = read_tsv(DATA / "pgl2_23_based_results.tsv")
    based_fail: dict[str, dict[str, str]] = {}
    s8_member_to_result: dict[str, dict[str, str]] = {}
    for result in s8_results:
        if result["based_pass"] != "FAIL":
            raise AssertionError("unexpected S8 based survivor")
        for member in result["member_seed_indices"].split(","):
            candidate_id = f"DIRECT_S8_C8_{int(member):05d}"
            s8_member_to_result[candidate_id] = result
            based_fail[candidate_id] = result
    for result in pgl23_results:
        if result["based_pass"] != "FAIL":
            raise AssertionError("unexpected PGL(2,23) based survivor")
        based_fail[result["candidate_id"]] = result
    if len(s8_member_to_result) != 48 or len(pgl23_results) != 48 or len(based_fail) != 96:
        raise AssertionError("based-failure coverage drift")

    for row in rows:
        result = based_fail.get(row["candidate_id"])
        if result is None:
            continue
        if row["accept_reject"] != "CHEAP_SURVIVOR":
            raise AssertionError("based result targets a non-survivor")
        row["CQ-09_based_dangerous_separation"] = "FAIL"
        row["CQ-10_based_geometric_admissibility"] = "FAIL"
        row["first_failed_gate"] = "CQ-09_BASED_DANGEROUS_SEPARATION"
        row["accept_reject"] = "REJECT"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summaries = {
        prime: json.loads((DATA / f"pgl2_{prime}_search_summary.json").read_text(encoding="utf-8"))
        for prime in (17, 23, 31)
    }
    family_rows = {
        family: sum(row["family"] == family for row in rows)
        for family in ("S8_natural_inner_C8", "PGL2_17_inner_C8", "PGL2_23_inner_C8", "PGL2_31_inner_C8")
    }
    report = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-Q-C8-COMPACT",
        "strategy": "direct rho o phi8 = alpha o rho; no eight-kernel core blowup",
        "based_lower_bound_N": 2338,
        "candidate_families_attempted": [
            {"family": "S7 natural symmetric target", "order": 5040, "seeds_examined": 0, "classification": "EMPTY_BY_THEOREM", "reason": "Aut(S7)=Inn(S7) and S7 has no element of order 8."},
            {"family": "S8 natural symmetric target", "order": 40320, "seeds_examined": family_rows["S8_natural_inner_C8"], "classification": "COMPLETE_UP_TO_SIMULTANEOUS_CONJUGACY", "cheap_survivors": 48, "based_survivors": 0},
            {"family": "PGL(2,17)", "order": 4896, "seeds_examined": family_rows["PGL2_17_inner_C8"], "classification": "ALL_ORDER_8_AUTOMORPHISM_CLASSES_COMPLETE", "cheap_survivors": summaries[17]["counters"]["cheap_survivors"], "based_survivors": 0},
            {"family": "PGL(2,19)", "order": 6840, "seeds_examined": 0, "classification": "EMPTY_BY_THEOREM", "reason": "Element orders in split/nonsplit tori divide 18 or 20; no order-8 inner automorphism."},
            {"family": "PGL(2,23)", "order": 12144, "seeds_examined": family_rows["PGL2_23_inner_C8"], "classification": "ALL_ORDER_8_AUTOMORPHISM_CLASSES_COMPLETE", "cheap_survivors": summaries[23]["counters"]["cheap_survivors"], "based_survivors": 0},
            {"family": "PGL(2,29)", "order": 24360, "seeds_examined": 0, "classification": "EMPTY_BY_THEOREM", "reason": "Element orders in split/nonsplit tori divide 28 or 30; no order-8 inner automorphism."},
            {"family": "PGL(2,31)", "order": 29760, "seeds_examined": family_rows["PGL2_31_inner_C8"], "classification": "ALL_ORDER_8_AUTOMORPHISM_CLASSES_COMPLETE", "cheap_survivors": summaries[31]["counters"]["cheap_survivors"], "based_survivors": 0},
        ],
        "order_windows_completed": {
            "Q1_2338_to_10000": {"completed_classes": ["S7", "PGL(2,17)", "PGL(2,19)"], "entire_window_exhausted": False},
            "Q2_10000_to_50000": {"completed_classes": ["S8", "PGL(2,23)", "PGL(2,29)", "PGL(2,31)"], "entire_window_exhausted": False},
            "Q3_50000_to_100000": {"completed_classes": [], "entire_window_exhausted": False},
        },
        "number_candidates_examined": len(rows),
        "number_passing_cheap_exact_gates": 96,
        "number_passing_based_dangerous_certificate": 0,
        "number_global_certified": 0,
        "smallest_global_certified_quotient": None,
        "smallest_tractable_global_certified_quotient": None,
        "C8_equivariance_direct": True,
        "parity": "PASS for all 96 cheap-gate survivors",
        "based_query": {
            "immutable_tree": "data/production/quotient_separator/based_tree_meta.bin",
            "exact_elements_including_identity": 23_129_593,
            "dangerous_set_recomputed": False,
            "S8_kernel_orbit_representatives": len(s8_results),
            "S8_maps_covered": len(s8_member_to_result),
            "PGL2_23_maps_evaluated": len(pgl23_results),
            "all_based_fail": True,
            "witnesses": [
                {"scope": "S8 kernel orbit", "id": item["kernel_orbit_id"], "members": item["member_seed_indices"], "element_id": int(item["first_kernel_element_id"]), "depth": int(item["first_kernel_depth"]), "word": item["first_kernel_word"]}
                for item in s8_results
            ] + [
                {"scope": "PGL(2,23) map", "id": item["candidate_id"], "element_id": int(item["first_kernel_element_id"]), "depth": int(item["first_kernel_depth"]), "word": item["first_kernel_word"]}
                for item in pgl23_results
            ],
        },
        "numerical_feasibility": {"evaluated_candidates": 0, "reason": "No candidate passed CQ-09/CQ-10, so no candidate was eligible for global geometry or the tractability gate."},
        "production_quotient_found": False,
        "production_yaml_created": False,
        "smoke_released": False,
        "terminal_classification": "NO_COMPACT_QUOTIENT_IN_COMPLETED_SEARCH_CLASSES",
        "task_status": "Deferred",
        "exact_primary_stop_condition": "The completed S7/S8 and prime-field PGL(2,p), p=17,19,23,29,31, direct-equivariant classes contain no based-admissible quotient; the current environment has no low-index-normal-subgroup or finite-group automorphism enumerator that proves exhaustion of all remaining groups in Q1/Q2.",
        "required_to_resume": "A concrete non-symmetric/non-prime-PGL finite group family in 2338<=N<=50000 with an explicit order-eight automorphism and a proof-complete homomorphism parameterization, or GAP/Sage/libgap low-index infrastructure.",
        "main_tex_modified": False,
    }
    json_path = GROUP / "COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.json"
    md_path = GROUP / "COMPACT_C8_EQUIVARIANT_QUOTIENT_SEARCH_REPORT.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(
        "# Compact direct C8-equivariant quotient search\n\n"
        "## Terminal result\n\n"
        "**No compact quotient exists in the completed search classes.** This is an exact null result for those classes, "
        "not an exhaustion theorem for every group in Q1/Q2.\n\n"
        "The search used `rho(g_i)=alpha^i(x)` from the outset. It completed the natural symmetric targets `S7` and `S8`, "
        "and every order-eight inner-automorphism class of the prime-field groups `PGL(2,p)` for all relevant primes "
        "`p=17,19,23,29,31` with order in 2,338--50,000. `PGL(2,19)` and `PGL(2,29)` have no order-eight element and "
        "are empty classes.\n\n"
        f"The machine-readable table contains {len(rows):,} evaluated seeds. Exactly 96 pass CQ-01--CQ-08: 48 in `S8` "
        "and 48 in `PGL(2,23)`. The 48 S8 maps collapse to six centralizer kernel orbits; every orbit has a frozen-ball "
        "kernel witness at depth 4 or 6. Every PGL(2,23) survivor likewise has a depth-6 witness. Therefore all 96 fail "
        "CQ-09 and CQ-10.\n\n"
        "The immutable 23,129,592-element dangerous set was not recomputed. Its certified BFS tree was queried directly, "
        "and each evaluation stopped at an explicit exact permutation/projective-matrix identity. With no based survivor, "
        "global systole, numerical feasibility, production YAML, and smoke were not released.\n\n"
        "The exact remaining blocker is a proof-complete enumerable family outside the completed classes, or low-index/finite-"
        "automorphism infrastructure such as GAP, SageMath, or libgap. `main.tex` remains unchanged.\n",
        encoding="utf-8",
    )
    print(json.dumps({"candidates": len(rows), "cheap": 96, "based_pass": 0, "classification": report["terminal_classification"]}, indent=2))


if __name__ == "__main__":
    main()
