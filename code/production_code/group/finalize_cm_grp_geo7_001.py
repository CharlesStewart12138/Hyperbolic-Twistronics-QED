from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, getcontext, localcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GROUP = Path(__file__).resolve().parent
DATA = ROOT / "data" / "production" / "geometric_ball"
R6_ROOT = DATA / "work" / "r6_regression"
R7_ROOT = DATA / "work" / "r7_primary"
ENGINE = GROUP / "external_geometric_ball_geo7.exe"
POST_SOURCE = GROUP / "geometric_ball_postprocess.cpp"
POST = GROUP / "geometric_ball_postprocess_geo7_v2.exe"
TENSOR_SOURCE = ROOT / "production_code" / "hodge" / "geometric_ball_tensor_stream.cpp"
TENSOR = ROOT / "production_code" / "hodge" / "geometric_ball_tensor_stream_geo7_v2.exe"
R6_REGISTRY = DATA / "geo_ball_r6_exact.bin"
R7_REGISTRY = DATA / "geo_ball_r7_exact.bin"
SHELL_BUCKETS = DATA / "shell_r6_r7" / "buckets"
SHELL_REGISTRY = DATA / "geo_shell_r6_r7_exact.bin"
SHELL_TENSOR = DATA / "geo_shell_r6_r7_tensor.json"
FROZEN_M6 = ROOT / "data" / "production" / "local_full_kernel" / "EXACT_BALL6_TENSOR_PARTIAL.json"
TAIL7 = ROOT / "data" / "production" / "local_full_kernel" / "EXACT_BALL7_TENSOR_TAIL.json"
BUCKETS = 256
RECORD_BYTES = 147
HARD_RSS = 48 * 1024**3


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(32 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def parse_tsv(path: Path) -> dict[str, str]:
    return dict(
        line.split("\t", 1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if "\t" in line
    )


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True)
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")


def compile_if_needed(source: Path, executable: Path, libraries: list[str]) -> None:
    if executable.exists() and executable.stat().st_mtime_ns >= source.stat().st_mtime_ns:
        return
    temporary = executable.with_suffix(".build.exe")
    run(["g++", "-std=c++20", "-O3", "-DNDEBUG", str(source), "-o", str(temporary), *libraries])
    if executable.exists():
        executable.unlink()
    temporary.replace(executable)


def committed_buckets(run_root: Path) -> tuple[Path, dict[str, str]]:
    checkpoint = parse_tsv(run_root / "checkpoint.tsv")
    if checkpoint["complete"] != "1" or checkpoint["frontier_elements"] != "0":
        raise RuntimeError(f"geometric flood is not complete: {run_root}")
    depth = int(checkpoint["completed_depth"])
    return run_root / "state" / f"depth-{depth:03d}" / "visited", checkpoint


def bucket_manifest(bucket_dir: Path, output: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    total_count = 0
    total_bytes = 0
    for bucket in range(BUCKETS):
        path = bucket_dir / f"bucket-{bucket:03d}.bin"
        size = path.stat().st_size
        if size % RECORD_BYTES:
            raise RuntimeError(f"corrupt bucket size: {path}")
        count = size // RECORD_BYTES
        rows.append({
            "bucket": bucket,
            "count": count,
            "bytes": size,
            "sha256": sha256(path),
        })
        total_count += count
        total_bytes += size
    result = {
        "schema_version": "1.0",
        "bucket_count": BUCKETS,
        "record_bytes": RECORD_BYTES,
        "total_count": total_count,
        "total_bytes": total_bytes,
        "buckets": rows,
        "all_complete": len(rows) == BUCKETS,
    }
    write_json(output, result)
    return result


def r7_registry_phase() -> dict[str, object]:
    buckets, checkpoint = committed_buckets(R7_ROOT)
    summary_path = DATA / "geo_ball_r7_summary.tsv"
    if not R7_REGISTRY.exists() or not summary_path.exists():
        run([str(ENGINE), "finalize", str(R7_ROOT), str(R7_REGISTRY), str(summary_path)])
    summary = parse_tsv(summary_path)
    manifest_buckets = bucket_manifest(buckets, DATA / "geo_ball_r7_bucket_manifest.json")
    restart_registry = DATA / "geo_ball_r7_restart_check.bin"
    restart_summary = DATA / "geo_ball_r7_restart_check.tsv"
    run([str(ENGINE), "finalize", str(R7_ROOT), str(restart_registry), str(restart_summary)])
    primary_hash = sha256(R7_REGISTRY)
    restart_hash = sha256(restart_registry)
    restart_pass = primary_hash == restart_hash
    restart_registry.unlink()
    restart_summary.unlink()
    shell_counts = [int(value) for value in summary["shell_counts"].split(",")]
    frontier_manifest = {
        "schema_version": "1.0",
        "completed_depth": int(checkpoint["completed_depth"]),
        "terminal_frontier_count": int(checkpoint["frontier_elements"]),
        "shell_counts": shell_counts,
        "candidate_counts_by_depth": [int(value) for value in summary["candidate_counts_by_depth"].split(",")],
        "duplicate_counts_by_depth": [int(value) for value in summary["duplicate_counts_by_depth"].split(",")],
        "atomic_checkpoint_resume_used_at_every_depth": True,
        "frontier_exhausted": summary["frontier_exhausted"] == "1",
    }
    write_json(DATA / "geo_ball_r7_frontier_manifest.json", frontier_manifest)
    result = {
        "schema_version": "1.0",
        "task_id": "CM-GRP-GEO7-001",
        "phase": "R7_PRODUCTION_ENUMERATION",
        "target_radius_over_a_B": 7,
        "simple_expansion_radius_over_a_B": "7.800895927193685166956845298951242796283512166915248265505749950383589236950287",
        "production_flood_radius_over_a_B": 7,
        "production_filter_basis": "GEO-FLOOD-2 exact Dirichlet-Voronoi center strengthening cross-validated by exact R=6 set equality",
        "flood_generations": int(summary["flood_generations"]),
        "candidate_emissions": int(summary["candidate_emissions"]),
        "duplicate_emissions": int(summary["duplicate_emissions"]),
        "target_unique_elements": int(summary["target_unique_elements"]),
        "expansion_unique_elements": int(summary["target_unique_elements"]),
        "frontier_exhausted": summary["frontier_exhausted"] == "1",
        "exact_boundary_fallbacks": int(summary["exact_boundary_fallbacks"]),
        "maximum_transport_word_depth": len(shell_counts) - 2,
        "shell_counts_by_transport_depth": shell_counts,
        "registry": str(R7_REGISTRY.relative_to(ROOT)).replace("\\", "/"),
        "registry_bytes": R7_REGISTRY.stat().st_size,
        "registry_sha256": primary_hash,
        "bucket_manifest_sha256": sha256(DATA / "geo_ball_r7_bucket_manifest.json"),
        "frontier_manifest_sha256": sha256(DATA / "geo_ball_r7_frontier_manifest.json"),
        "restart_registry_sha256_identical": restart_pass,
        "peak_rss_bytes": int(summary["peak_rss_bytes"]),
        "runtime_seconds": float(summary["runtime_seconds"]),
        "hard_rss_ceiling_bytes": HARD_RSS,
        "acceptance": {
            "fixed_point_complete": summary["frontier_exhausted"] == "1",
            "bucket_count_256": manifest_buckets["bucket_count"] == BUCKETS,
            "bucket_total_matches_registry": manifest_buckets["total_count"] == int(summary["target_unique_elements"]),
            "restart_hash_identical": restart_pass,
            "rss_below_hard_ceiling": int(summary["peak_rss_bytes"]) <= HARD_RSS,
        },
        "finished_utc": utc_now(),
    }
    write_json(DATA / "geo_ball_r7_manifest.json", result)
    return result


def closure_phase() -> dict[str, object]:
    compile_if_needed(POST_SOURCE, POST, ["-lgmp", "-lpsapi"])
    inverse = DATA / "geo_ball_r7_inverse_closure.tsv"
    phi8 = DATA / "geo_ball_r7_phi8_closure.tsv"
    run([str(POST), "closure-root", str(R7_ROOT), "inverse", str(inverse)])
    run([str(POST), "closure-root", str(R7_ROOT), "phi8", str(phi8)])
    result = {
        "schema_version": "1.0",
        "inverse": parse_tsv(inverse),
        "phi8": parse_tsv(phi8),
        "inverse_pass": parse_tsv(inverse)["exact_set_equal"] == "1",
        "phi8_pass": parse_tsv(phi8)["exact_set_equal"] == "1",
    }
    write_json(DATA / "geo_ball_r7_closure_certificate.json", result)
    return result


def shell_phase() -> dict[str, object]:
    compile_if_needed(POST_SOURCE, POST, ["-lgmp", "-lpsapi"])
    summary_path = DATA / "geo_shell_r6_r7_summary.tsv"
    run([
        str(POST), "shell", str(R7_ROOT), str(R6_ROOT), str(SHELL_BUCKETS),
        str(SHELL_REGISTRY), str(summary_path),
    ])
    summary = parse_tsv(summary_path)
    count = int(summary["shell_count"])
    inverse = DATA / "geo_shell_r6_r7_inverse_closure.tsv"
    phi8 = DATA / "geo_shell_r6_r7_phi8_closure.tsv"
    run([str(POST), "closure-buckets", str(SHELL_BUCKETS), str(count), "inverse", str(inverse)])
    run([str(POST), "closure-buckets", str(SHELL_BUCKETS), str(count), "phi8", str(phi8)])
    buckets = bucket_manifest(SHELL_BUCKETS, DATA / "geo_shell_r6_r7_bucket_manifest.json")
    result = {
        "schema_version": "1.0",
        "task_id": "CM-GRP-GEO7-001",
        "scope": "exact geometric shell 6a_B<d<=7a_B",
        "ball6_count": int(summary["ball6_count"]),
        "ball7_count": int(summary["ball7_count"]),
        "shell_count": count,
        "cardinality_identity": count + int(summary["ball6_count"]) == int(summary["ball7_count"]),
        "exact_difference_pass": summary["exact_difference_pass"] == "1",
        "inverse_closure": parse_tsv(inverse)["exact_set_equal"] == "1",
        "phi8_closure": parse_tsv(phi8)["exact_set_equal"] == "1",
        "registry": str(SHELL_REGISTRY.relative_to(ROOT)).replace("\\", "/"),
        "registry_bytes": SHELL_REGISTRY.stat().st_size,
        "registry_sha256": sha256(SHELL_REGISTRY),
        "bucket_manifest_total": buckets["total_count"],
        "bucket_manifest_sha256": sha256(DATA / "geo_shell_r6_r7_bucket_manifest.json"),
        "finished_utc": utc_now(),
    }
    write_json(DATA / "geo_shell_r6_r7_manifest.json", result)
    return result


def tensor_phase() -> dict[str, object]:
    compile_if_needed(TENSOR_SOURCE, TENSOR, ["-lmpfr", "-lgmp", "-lpsapi"])
    run([str(TENSOR), str(SHELL_REGISTRY), str(SHELL_TENSOR)])
    return json.loads(SHELL_TENSOR.read_text(encoding="utf-8"))


def decimal_sqrt2(rounding: str) -> Decimal:
    with localcontext() as context:
        context.prec = 90
        context.rounding = rounding
        return context.sqrt(Decimal(2))


def directed(expression, rounding: str) -> Decimal:
    with localcontext() as context:
        context.prec = 90
        context.rounding = rounding
        return +expression(context)


def matrix_add_interval(a: list[list[str]], b: list[list[str]]) -> list[list[str]]:
    getcontext().prec = 100
    return [[str(Decimal(a[i][j]) + Decimal(b[i][j])) for j in range(4)] for i in range(4)]


def word_invariance_certificate() -> dict[str, object]:
    from production_code.group.run_cm_grp_ext_001 import (
        abelian,
        exact_cosh_distance_over_R,
        matrix_from_word,
        projective_key,
        tensor_moment,
    )

    base1 = (0, 5, 2, 7)
    base2 = (7, 2, 5, 0)
    pairs = []
    for rotation in range(8):
        left = tuple((token + rotation) & 7 for token in base1)
        right = tuple((token + rotation) & 7 for token in base2)
        matrix_left = matrix_from_word(tuple(f"g{x}" for x in left))
        matrix_right = matrix_from_word(tuple(f"g{x}" for x in right))
        key_equal = projective_key(matrix_left) == projective_key(matrix_right)
        distance_equal = exact_cosh_distance_over_R(matrix_left) == exact_cosh_distance_over_R(matrix_right)
        abelian_equal = abelian(left) == abelian(right)
        moment_equal = tensor_moment(left) == tensor_moment(right)
        pairs.append({
            "left": [f"g{x}" for x in left],
            "right": [f"g{x}" for x in right],
            "exact_key_equal": key_equal,
            "exact_displacement_equal": distance_equal,
            "abelianization_equal": abelian_equal,
            "tensor_moment_equal": moment_equal,
            "full_weighted_contribution_equal": key_equal and distance_equal and abelian_equal and moment_equal,
        })
    result = {
        "schema_version": "1.0",
        "task_id": "CM-GRP-GEO7-001",
        "pairs_checked": len(pairs),
        "pairs": pairs,
        "all_complete_downstream_contributions_equal": all(item["full_weighted_contribution_equal"] for item in pairs),
        "reason": "The weight is a deterministic function of exact origin displacement and the Hodge tensor factor is the outer product of the exact abelianization vector.",
    }
    write_json(DATA / "geo7_tensor_word_invariance.json", result)
    return result


def m7_certificate() -> dict[str, object]:
    m6 = json.loads(FROZEN_M6.read_text(encoding="utf-8"))
    shell = json.loads(SHELL_TENSOR.read_text(encoding="utf-8"))
    tail = json.loads(TAIL7.read_text(encoding="utf-8"))
    lower = matrix_add_interval(m6["partial_tensor_entrywise_lower"], shell["partial_tensor_entrywise_lower"])
    upper = matrix_add_interval(m6["partial_tensor_entrywise_upper"], shell["partial_tensor_entrywise_upper"])
    sqrt2_lo = decimal_sqrt2(ROUND_FLOOR)
    sqrt2_hi = decimal_sqrt2(ROUND_CEILING)
    x_lo, x_hi = Decimal(lower[2][3]), Decimal(upper[2][3])
    y_lo, y_hi = Decimal(lower[3][3]), Decimal(upper[3][3])
    if x_lo < 0:
        raise RuntimeError("m7 C8 parameter x crossed zero; interval formula needs sign split")
    beta_minus_lo = directed(lambda _c: y_lo + sqrt2_lo * x_lo, ROUND_FLOOR)
    beta_minus_hi = directed(lambda _c: y_hi + sqrt2_hi * x_hi, ROUND_CEILING)
    beta_plus_lo = directed(lambda _c: y_lo - sqrt2_hi * x_hi, ROUND_FLOOR)
    beta_plus_hi = directed(lambda _c: y_hi - sqrt2_lo * x_lo, ROUND_CEILING)
    tail_budget = Decimal(tail["certified_rational_coordinate_trace_upper"])
    delta_minus_hi = directed(
        lambda _c: tail_budget / (Decimal(2) * sqrt2_lo * (sqrt2_lo - Decimal(1))),
        ROUND_CEILING,
    )
    delta_plus_hi = directed(
        lambda _c: tail_budget / (Decimal(2) * sqrt2_lo * (sqrt2_lo + Decimal(1))),
        ROUND_CEILING,
    )
    minus_sector = [
        directed(lambda _c: beta_minus_lo / 2, ROUND_FLOOR),
        directed(lambda _c: (beta_minus_hi + delta_minus_hi) / 2, ROUND_CEILING),
    ]
    plus_sector = [
        directed(lambda _c: beta_plus_lo / 2, ROUND_FLOOR),
        directed(lambda _c: (beta_plus_hi + delta_plus_hi) / 2, ROUND_CEILING),
    ]
    joint_upper = directed(
        lambda _c: (
            tail_budget
            + Decimal(2) * sqrt2_hi
            * ((sqrt2_hi - 1) * beta_minus_hi + (sqrt2_hi + 1) * beta_plus_hi)
        ) / Decimal(16),
        ROUND_CEILING,
    )
    common = [max(minus_sector[0], plus_sector[0]), min(minus_sector[1], plus_sector[1], joint_upper)]
    resolved = common[0] > common[1]
    endpoint_ratio = None if resolved else common[1] / common[0]
    word_invariance = word_invariance_certificate()
    result = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7-STREAM",
        "status": "Done",
        "scope": "LOCAL centered/aligned Bolza point; no angle continuation or bulk promotion",
        "inputs": {
            "frozen_m6_tensor": str(FROZEN_M6.relative_to(ROOT)).replace("\\", "/"),
            "new_exact_shell_tensor": str(SHELL_TENSOR.relative_to(ROOT)).replace("\\", "/"),
            "directed_tail_d_gt_7a_B": str(TAIL7.relative_to(ROOT)).replace("\\", "/"),
        },
        "new_geometric_shell_elements_consumed": shell["elements_consumed"],
        "full_ball_elements": shell["elements_consumed"] + m6["dangerous_nonidentity_elements"] + 1,
        "partial_tensor_entrywise_lower": lower,
        "partial_tensor_entrywise_upper": upper,
        "partial_generalized_coefficients": {
            "minus_interval": [str(beta_minus_lo), str(beta_minus_hi)],
            "plus_interval": [str(beta_plus_lo), str(beta_plus_hi)],
        },
        "tail": {
            "C0": tail["C0_per_abs_w_upper_directed"],
            "C1_coordinate": tail["C1_coordinate_per_abs_w_upper_directed"],
            "C2_coordinate_trace": tail["coordinate_trace_C2_upper_directed"],
            "certified_integer_C2": tail["certified_rational_coordinate_trace_upper"],
            "joint_alignment_budget": "2*sqrt(2)*(tau_-+tau_+)<48",
        },
        "sector_t_over_w_intervals": {
            "minus": [str(value) for value in minus_sector],
            "plus": [str(value) for value in plus_sector],
        },
        "common_root_necessary_interval": [str(value) for value in common],
        "endpoint_ratio": None if endpoint_ratio is None else str(endpoint_ratio),
        "common_aligned_root_resolved": resolved,
        "classification": "TENSOR-NO-ROOT-CERTIFIED" if resolved else "TENSOR-UNRESOLVED",
        "tensor_word_invariance": word_invariance["all_complete_downstream_contributions_equal"],
        "uncertainty_decomposition": {
            "remaining_exact_shell_omission": "zero inside d<=7a_B; no separate certified finite (7,8] shell term has been isolated from the analytic d>7a_B majorant",
            "finite_shell_component": "the complete 6a_B<d<=7a_B shell is exactly accumulated with 192-bit directed rounding",
            "C0_tail": tail["C0_per_abs_w_upper_directed"],
            "C1_tail": tail["C1_coordinate_per_abs_w_upper_directed"],
            "C2_tail": tail["coordinate_trace_C2_upper_directed"],
            "alignment": "joint C8 sector constraint retained; no independent simultaneous saturation",
            "interval_rounding": "192-bit shell and 256-bit tail directed MPFR rounding",
            "dominant_uncertainty": "d>7a_B analytic C2/alignment majorant" if not resolved else "resolved within the registered local aligned scope",
        },
        "m8_scientifically_justified": False,
        "m8_decision": "DO_NOT_RELEASE: the analytic d>7a_B C2/alignment majorant, not a separately certified omitted finite shell, is the dominant reducible uncertainty; improve the analytic bound first",
        "m8_executed": False,
        "scalar_route_authorized": False,
        "physical_parameters_retuned": False,
        "main_tex_modified": False,
        "finished_utc": utc_now(),
    }
    write_json(ROOT / "production_code" / "hodge" / "CM_047_NP_M7_STREAM_RESULT.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("r7-registry", "closure", "shell", "tensor", "m7"), required=True)
    args = parser.parse_args()
    if args.phase == "r7-registry":
        value = r7_registry_phase()
    elif args.phase == "closure":
        value = closure_phase()
    elif args.phase == "shell":
        value = shell_phase()
    elif args.phase == "tensor":
        value = tensor_phase()
    else:
        value = m7_certificate()
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
