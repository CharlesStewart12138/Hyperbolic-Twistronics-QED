from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DATA = ROOT / "data" / "production" / "global_direct_v2"
WORK = ROOT / "data" / "production" / "geometric_ball" / "work" / "global_axis6_exact"
EXE = HERE / "external_geometric_ball_axis6.exe"
CHECKPOINT = WORK / "checkpoint.tsv"
P = 785_672_817
Q = 555_554_576
LABEL = "axis_translation_length_le_6a_B"
RECORD_BYTES = 147
RESERVE_BYTES = 250 * 1024**3
TRANSIENT_ALLOWANCE_BYTES = 2 * 1024**3
HARD_RSS_BYTES = 48 * 1024**3
R7_CHECKPOINT = ROOT / "data" / "production" / "geometric_ball" / "work" / "r7_primary" / "checkpoint.tsv"
R7_REGISTRY = ROOT / "data" / "production" / "geometric_ball" / "geo_ball_r7_exact.bin"
FORECAST = HERE / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_RESOURCE_FORECAST.json"
RUN_STATE = HERE / "PF_GRP_001_GEO_GLOBAL_DIRECT_V2_RUN_STATE.json"
LOG = ROOT / "CODE_WORK_LOG.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_tsv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
            values[key] = value
    return values


def integers(text: str) -> list[int]:
    return [] if not text else [int(value) for value in text.split(",")]


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def tree_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(16 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def measured_peak_disk(checkpoint: dict[str, str]) -> int:
    shells = integers(checkpoint["shell_counts"])
    candidates = integers(checkpoint["candidate_counts_by_depth"])
    visited = 0
    peak = 0
    for depth, candidate_count in enumerate(candidates, start=1):
        visited += shells[depth - 1]
        next_visited = visited + shells[depth]
        peak = max(peak, (visited + next_visited + candidate_count) * RECORD_BYTES)
    return peak


def forecast() -> dict[str, object]:
    r7 = parse_tsv(R7_CHECKPOINT)
    root2 = math.sqrt(2.0)
    a_over_r = 2.0 * math.acosh(1.0 + root2)
    cutoff_cosh = P + Q * root2
    cutoff_over_a = math.acosh(cutoff_cosh) / a_over_r
    cosh_7a = math.cosh(7.0 * a_over_r)
    area_ratio = (cutoff_cosh - 1.0) / (cosh_7a - 1.0)
    r7_count = int(r7["visited_elements"])
    projected_count = round(r7_count * area_ratio)
    projected_registry = 24 + RECORD_BYTES * projected_count
    r7_peak_disk = measured_peak_disk(r7)
    projected_peak_disk = round(r7_peak_disk * area_ratio)
    free = shutil.disk_usage(ROOT).free
    final_duplicate_budget = 2 * projected_registry
    result: dict[str, object] = {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT-V2",
        "forecast_precedes_large_run": True,
        "mathematical_cutoff": {
            "translation_length_hypothesis": "ell(g)<=6a_B",
            "axis_distance_after_conjugation": "r<=r_out",
            "displacement_identity": "sinh(d(o,g o)/(2R))=cosh(r/R)*sinh(ell(g)/(2R))",
            "exact_cosh_cutoff": f"{P}+{Q}*sqrt(2)",
            "exact_q2_coefficients": [P, Q],
            "cutoff_over_a_B_decimal": format(cutoff_over_a, ".17g"),
            "strictly_below_old_triangle_cutoff": cutoff_over_a < 7.60179185438737,
            "derivation": "1+2*(3+2*sqrt(2))^2*((2405+1700*sqrt(2))^2-1)",
        },
        "calibration": {
            "R7_exact_elements": r7_count,
            "R7_candidate_emissions": int(r7["candidate_emissions"]),
            "R7_measured_peak_disk_bytes": r7_peak_disk,
            "R7_peak_rss_bytes": int(r7["peak_rss_bytes"]),
            "R7_registry_bytes": R7_REGISTRY.stat().st_size,
        },
        "projection": {
            "hyperbolic_disk_area_ratio_from_R7": area_ratio,
            "element_count_estimate": projected_count,
            "registry_bytes_estimate": projected_registry,
            "measured_shape_peak_disk_bytes_estimate": projected_peak_disk,
            "terminal_work_plus_registry_bytes_estimate": final_duplicate_budget,
            "runtime_seconds_estimate": float(r7["elapsed_seconds"]) * area_ratio,
        },
        "hard_operational_gates": {
            "per_step_additional_disk_upper_bound": "147*(visited+16*frontier)+2GiB; candidates<=8*frontier and next_visited<=visited+8*frontier",
            "minimum_post_step_free_reserve_bytes": RESERVE_BYTES,
            "hard_rss_ceiling_bytes": HARD_RSS_BYTES,
            "atomic_unit": "one flood depth in one fresh subprocess",
            "checkpoint_commit": "state/depth-N is atomically renamed before checkpoint.tsv; transient candidates and old state are then removed",
            "finalization_gate": "free >= exact registry bytes + reserve",
        },
        "host_at_forecast": {
            "free_disk_bytes": free,
            "total_disk_bytes": shutil.disk_usage(ROOT).total,
        },
        "authorization": {
            "projection_leaves_reserve": free - projected_peak_disk >= RESERVE_BYTES,
            "terminal_duplicate_leaves_reserve": free - final_duplicate_budget >= RESERVE_BYTES,
            "run_authorized": free - max(projected_peak_disk, final_duplicate_budget) >= RESERVE_BYTES,
        },
        "generated_utc": utc_now(),
    }
    atomic_json(FORECAST, result)
    return result


def update_log(checkpoint: dict[str, str], gate: dict[str, int]) -> None:
    start = "<!-- PF-GRP-001-GEO-GLOBAL-DIRECT-V2 LIVE START -->"
    end = "<!-- PF-GRP-001-GEO-GLOBAL-DIRECT-V2 LIVE END -->"
    block = (
        f"{start}\n"
        "## PF-GRP-001-GEO-GLOBAL-DIRECT-V2 live checkpoint\n\n"
        f"- cutoff: exact cosh(D*/R) = {P}+{Q} sqrt(2)\n"
        f"- completed depth: {checkpoint['completed_depth']}\n"
        f"- visited/frontier: {checkpoint['visited_elements']} / {checkpoint['frontier_elements']}\n"
        f"- complete: {checkpoint['complete']}\n"
        f"- peak RSS bytes: {checkpoint['peak_rss_bytes']}\n"
        f"- current free bytes: {gate['free_bytes']}\n"
        f"- worst-case additional bytes for next atomic step: {gate['additional_upper_bytes']}\n"
        f"- updated UTC: {utc_now()}\n"
        f"{end}"
    )
    text = LOG.read_text(encoding="utf-8") if LOG.exists() else ""
    if start in text and end in text:
        before = text.split(start, 1)[0]
        after = text.split(end, 1)[1]
        text = before + block + after
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    temporary = LOG.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(LOG)


def gate(checkpoint: dict[str, str]) -> dict[str, int]:
    visited = int(checkpoint["visited_elements"])
    frontier = int(checkpoint["frontier_elements"])
    additional = (visited + 16 * frontier) * RECORD_BYTES + TRANSIENT_ALLOWANCE_BYTES
    free = shutil.disk_usage(ROOT).free
    return {
        "free_bytes": free,
        "additional_upper_bytes": additional,
        "required_free_bytes": additional + RESERVE_BYTES,
        "reserve_bytes": RESERVE_BYTES,
    }


def save_run_state(checkpoint: dict[str, str], current_gate: dict[str, int]) -> None:
    atomic_json(RUN_STATE, {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT-V2",
        "checkpoint": checkpoint,
        "disk_gate": current_gate,
        "work_tree_bytes": tree_bytes(WORK),
        "updated_utc": utc_now(),
    })
    update_log(checkpoint, current_gate)


def run_to_fixed_point() -> None:
    if not FORECAST.exists() or not json.loads(FORECAST.read_text(encoding="utf-8"))["authorization"]["run_authorized"]:
        raise RuntimeError("accepted resource forecast is absent")
    if not CHECKPOINT.exists():
        WORK.parent.mkdir(parents=True, exist_ok=True)
        command = [str(EXE), "init-exact-q2", str(P), str(Q), LABEL, str(WORK)]
        subprocess.run(command, cwd=ROOT, check=True)
    while True:
        checkpoint = parse_tsv(CHECKPOINT)
        current_gate = gate(checkpoint)
        save_run_state(checkpoint, current_gate)
        if checkpoint["complete"] == "1":
            return
        if current_gate["free_bytes"] < current_gate["required_free_bytes"]:
            raise RuntimeError(f"disk gate failed before depth {int(checkpoint['completed_depth']) + 1}: {current_gate}")
        if int(checkpoint["peak_rss_bytes"]) > HARD_RSS_BYTES:
            raise RuntimeError("hard RSS ceiling exceeded")
        started = time.perf_counter()
        completed = subprocess.run([str(EXE), "step", str(WORK)], cwd=ROOT, text=True, capture_output=True)
        if completed.stdout:
            print(completed.stdout, end="", flush=True)
        if completed.stderr:
            print(completed.stderr, end="", flush=True)
        if completed.returncode:
            raise RuntimeError(f"flood step failed with {completed.returncode}")
        print(f"atomic_depth_wall_seconds={time.perf_counter()-started:.6f}", flush=True)


def finalize() -> None:
    checkpoint = parse_tsv(CHECKPOINT)
    if checkpoint["complete"] != "1" or checkpoint["frontier_elements"] != "0":
        raise RuntimeError("cannot finalize incomplete exact flood")
    registry = DATA / "axis6_exact_ball.bin"
    summary = DATA / "axis6_exact_ball_summary.tsv"
    registry_bytes = 24 + int(checkpoint["visited_elements"]) * RECORD_BYTES
    free = shutil.disk_usage(ROOT).free
    if free < registry_bytes + RESERVE_BYTES:
        raise RuntimeError("final registry disk gate failed")
    DATA.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(EXE), "finalize", str(WORK), str(registry), str(summary)], cwd=ROOT, check=True)
    atomic_json(DATA / "axis6_exact_ball_manifest.json", {
        "schema_version": "1.0",
        "task_id": "PF-GRP-001-GEO-GLOBAL-DIRECT-V2",
        "cutoff_q2": [P, Q],
        "cutoff_label": LABEL,
        "checkpoint": checkpoint,
        "registry": str(registry.relative_to(ROOT)).replace("\\", "/"),
        "registry_bytes": registry.stat().st_size,
        "registry_sha256": sha256(registry),
        "summary_sha256": sha256(summary),
        "complete": True,
        "finished_utc": utc_now(),
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("forecast", "run", "finalize"))
    args = parser.parse_args()
    if args.phase == "forecast":
        print(json.dumps(forecast(), indent=2, sort_keys=True))
    elif args.phase == "run":
        run_to_fixed_point()
    else:
        finalize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
