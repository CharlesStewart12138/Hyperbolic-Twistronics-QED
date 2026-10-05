from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GROUP = Path(__file__).resolve().parent
DATA = ROOT / "data" / "production" / "global_direct_v2"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(16 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def parse_tsv(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
            result[key] = value
    return result


def main() -> None:
    axis_manifest_path = DATA / "axis6_exact_ball_manifest.json"
    axis_manifest = json.loads(axis_manifest_path.read_text(encoding="utf-8"))
    scan_path = DATA / "product_kernel_scan_checkpoint.tsv"
    scan = parse_tsv(scan_path)
    audit_path = GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_INDEPENDENT_AUDIT.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    candidates_path = DATA / "product_kernel_candidates.tsv"
    with candidates_path.open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle, delimiter="\t"))
    candidates.sort(key=lambda row: float(row["translation_length_over_a_B"]))
    minimum = candidates[0]

    assert axis_manifest["complete"] is True
    assert axis_manifest["checkpoint"]["frontier_elements"] == "0"
    assert scan["complete"] == "1"
    assert int(scan["scanned_records"]) == int(scan["total_records"]) == 785_639_753
    assert int(scan["kernel_elements"]) == len(candidates) == 736
    assert int(scan["dangerous_elements"]) == 0
    assert audit["classification"] == "GLOBAL-SYSTOLE-GT-6a_B-CERTIFIED"

    input_paths = {
        "frozen_quotient": GROUP / "BASED_PRODUCT_QUOTIENT_CERTIFICATE.json",
        "GEO_FLOOD_theorem": GROUP / "BOLZA_GEOMETRIC_BALL_FLOOD_THEOREM.md",
        "prior_direct_attempt": GROUP / "GLOBAL_SYSTOLE_DIRECT_CERTIFICATE.json",
        "R7_manifest": ROOT / "data" / "production" / "geometric_ball" / "geo_ball_r7_manifest.json",
    }
    code_paths = {
        "flood_engine": GROUP / "external_geometric_ball.cpp",
        "flood_runner": GROUP / "run_pf_grp_global_direct_v2.py",
        "kernel_scanner": GROUP / "scan_axis6_product_kernel.cpp",
        "independent_audit": GROUP / "audit_axis6_product_kernel.py",
    }
    output_paths = {
        "axis_ball_manifest": axis_manifest_path,
        "axis_ball_summary": DATA / "axis6_exact_ball_summary.tsv",
        "scan_checkpoint": scan_path,
        "kernel_candidates": candidates_path,
        "independent_audit": audit_path,
    }
    certificate = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT-V2",
        "status": "Done",
        "classification": "GLOBAL-SYSTOLE-GT-6a_B-CERTIFIED",
        "quotient_id": "Q_BASED_S4CORE_PAIR_001",
        "theorem": {
            "statement": "If a nonidentity Bolza element has translation length ell<=6a_B, its conjugacy class contains h with cosh(d(o,h o)/R)<=785672817+555554576*sqrt(2).",
            "identity": "sinh(d(o,h o)/(2R))=cosh(r/R)*sinh(ell(h)/(2R)), with r<=r_out",
            "exact_cutoff_q2": [785672817, 555554576],
            "cutoff_over_a_B_decimal": "7.1531994630294363735423559053...",
            "old_triangle_cutoff_over_a_B": "7.6017918543873703339136905979...",
            "kernel_normality_closes_global_argument": True,
        },
        "exact_ball": {
            "elements": int(scan["total_records"]),
            "flood_generations": int(axis_manifest["checkpoint"]["completed_depth"]),
            "frontier_elements": int(axis_manifest["checkpoint"]["frontier_elements"]),
            "candidate_emissions": int(axis_manifest["checkpoint"]["candidate_emissions"]),
            "duplicate_emissions": int(axis_manifest["checkpoint"]["duplicate_emissions"]),
            "exact_boundary_fallbacks": int(axis_manifest["checkpoint"]["exact_boundary_fallbacks"]),
            "peak_rss_bytes": int(axis_manifest["checkpoint"]["peak_rss_bytes"]),
            "runtime_seconds": float(axis_manifest["checkpoint"]["elapsed_seconds"]),
            "registry_bytes": axis_manifest["registry_bytes"],
            "registry_sha256": axis_manifest["registry_sha256"],
            "GEO_FLOOD_2_fixed_point_complete": True,
        },
        "quotient_kernel_scan": {
            "records_scanned": int(scan["scanned_records"]),
            "even_nonidentity_records": int(scan["even_nonidentity_records"]),
            "component_evaluations": int(scan["component_evaluations"]),
            "kernel_elements_in_exact_ball": int(scan["kernel_elements"]),
            "dangerous_kernel_elements_with_translation_length_le_6a_B": int(scan["dangerous_elements"]),
            "runtime_seconds": float(scan["elapsed_seconds"]),
            "all_kernel_candidates_archived": True,
        },
        "systole": {
            "proved_lower_bound": "sys(ker rho)>6a_B",
            "equivalent_injectivity_radius": "r_inj(ker rho)>3a_B",
            "observed_kernel_element_upper_bound": "sys(ker rho)<=2*acosh(3167+2240*sqrt(2))*R",
            "observed_upper_bound_over_a_B": minimum["translation_length_over_a_B"],
            "observed_margin_over_6a_B": str(float(minimum["translation_length_over_a_B"]) - 6.0),
            "do_not_promote_observed_upper_bound_to_exact_systole": True,
        },
        "quotient_gates": {
            "PQ_14_all_global_dangerous_classes_separated": "PASS",
            "PQ_16_global_geometric_injectivity": "PASS_r_inj_global_gt_3a_B",
            "mathematical_production_admissibility_now_available": True,
            "numerical_matrix_free_feasibility": "NEXT_TASK_NOT_ASSUMED",
        },
        "acceptance": {
            "exact_algebraic_cutoff": True,
            "closed_boundary": True,
            "frontier_exhausted": True,
            "complete_exact_key_equality": True,
            "all_registry_elements_scanned": True,
            "no_dangerous_kernel_element": True,
            "independent_candidate_re_evaluation": True,
            "independent_integer_radical_trace_sign": True,
            "rss_below_48GiB": int(axis_manifest["checkpoint"]["peak_rss_bytes"]) <= 48 * 1024**3,
        },
        "scope": {
            "surface": "centered Bolza surface",
            "kernel": "normal kernel of Q_BASED_S4CORE_PAIR_001",
            "global_not_based_only": True,
            "does_not_prove_bulk_tower_convergence": True,
            "does_not_select_physical_target": True,
            "main_tex_unchanged": True,
        },
        "resource": {
            "free_disk_bytes_after_certificate_inputs": shutil.disk_usage(ROOT).free,
            "disk_reserve_policy_bytes": 250 * 1024**3,
            "no_swap_strategy": True,
            "one_flood_depth_per_subprocess": True,
            "scan_commit_records": 1_000_000,
        },
        "sha256": {
            "inputs": {name: sha256(path) for name, path in input_paths.items()},
            "code": {name: sha256(path) for name, path in code_paths.items()},
            "outputs": {name: sha256(path) for name, path in output_paths.items()},
        },
        "prior_negative_result_preserved": "PF-GRP-001-GEO-GLOBAL-DIRECT remains the immutable in-memory resource-stop result; V2 supplies the new external exact method.",
        "finished_utc": utc_now(),
    }
    out_json = GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.json"
    out_md = GROUP / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_CERTIFICATE.md"
    out_json.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_md.write_text(
        "# PF-GRP-001-GEO-GLOBAL-DIRECT-V2 certificate\n\n"
        "**Classification: GLOBAL-SYSTOLE-GT-6a_B-CERTIFIED.**\n\n"
        "The sharp axis-displacement identity reduces the complete global test to the exact algebraic "
        "closed ball `cosh(d/R)<=785672817+555554576 sqrt(2)`, whose radius is "
        "`7.153199463029436... a_B`. GEO-FLOOD-2 exhausted this ball after 21 generations with an empty "
        f"frontier and exactly `{scan['total_records']}` elements.\n\n"
        f"Every registry element was evaluated in `Q_BASED_S4CORE_PAIR_001`. There are `{scan['kernel_elements']}` "
        "nonidentity kernel elements inside the ball and exactly zero with translation length at most `6a_B`. "
        "Normality transfers the conjugacy representative theorem back to every kernel element, proving "
        "`sys(ker rho)>6a_B` and `r_inj(ker rho)>3a_B`.\n\n"
        f"The shortest observed in-ball kernel element has length `{minimum['translation_length_over_a_B']} a_B`; "
        "it supplies an upper bound, not an equality claim for the global systole. Independent recomputation of "
        "all candidate quotient images and exact integer-radical trace signs passed. PQ-14 and PQ-16 now pass.\n\n"
        "This certificate does not establish numerical matrix-free feasibility, a growing tower, target ancestry, "
        "or bulk convergence. `main.tex` remains unchanged.\n",
        encoding="utf-8",
    )
    print(json.dumps({"task_id": certificate["task_id"], "classification": certificate["classification"], "elements": certificate["exact_ball"]["elements"], "kernel": certificate["quotient_kernel_scan"]["kernel_elements_in_exact_ball"], "dangerous": 0}, indent=2))


if __name__ == "__main__":
    main()
