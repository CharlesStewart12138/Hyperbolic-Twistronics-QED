from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "external_geometric_ball.cpp"
EXECUTABLE = HERE / "external_geometric_ball_geo7.exe"
DATA = ROOT / "data" / "production" / "geometric_ball"
WORK = DATA / "work"
OLD_R6_CSV = ROOT / "data" / "production" / "short_geodesics" / "dangerous_based.csv"
OLD_R6_SUMMARY = ROOT / "data" / "production" / "short_geodesics" / "based_enumeration_summary.json"
R6_EXPECTED = 23_129_593
R6_SHELLS = [
    1, 8, 56, 392, 2736, 19096, 133288, 750304, 2394648,
    4550352, 5639552, 4853408, 2980664, 1312496, 402224,
    80448, 9408, 512, 0,
]
HARD_RSS = 48 * 1024**3


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(16 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def tree_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_tsv(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
            result[key] = value
    return result


def integer_list(text: str) -> list[int]:
    return [] if not text else [int(value) for value in text.split(",")]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")
    return completed


def compile_engine() -> None:
    if EXECUTABLE.exists() and EXECUTABLE.stat().st_mtime_ns >= max(
        SOURCE.stat().st_mtime_ns, (HERE / "external_group_ball.cpp").stat().st_mtime_ns
    ):
        return
    temporary = EXECUTABLE.with_suffix(".build.exe")
    run([
        "g++", "-std=c++20", "-O3", "-DNDEBUG", str(SOURCE),
        "-o", str(temporary), "-lgmp", "-lpsapi",
    ])
    if EXECUTABLE.exists():
        EXECUTABLE.unlink()
    temporary.replace(EXECUTABLE)


def run_fixed_point(target: int, flood: int, name: str) -> tuple[Path, dict[str, str]]:
    run_root = WORK / name
    checkpoint = run_root / "checkpoint.tsv"
    if not checkpoint.exists():
        run([str(EXECUTABLE), "init", str(target), str(flood), str(run_root)])
    while True:
        fields = parse_tsv(checkpoint)
        if fields["complete"] == "1":
            break
        run([str(EXECUTABLE), "step", str(run_root)])
    return run_root, parse_tsv(checkpoint)


def finalize_registry(run_root: Path, radius: int) -> tuple[Path, Path, dict[str, str]]:
    registry = DATA / f"geo_ball_r{radius}_exact.bin"
    summary = DATA / f"geo_ball_r{radius}_summary.tsv"
    run([str(EXECUTABLE), "finalize", str(run_root), str(registry), str(summary)])
    return registry, summary, parse_tsv(summary)


def r6_phase() -> dict[str, object]:
    started = time.perf_counter()
    run_root, checkpoint = run_fixed_point(6, 6, "r6_regression")
    registry, summary_path, summary = finalize_registry(run_root, 6)
    comparison_path = DATA / "geo_ball_r6_old_new_key_comparison.tsv"
    run([
        str(EXECUTABLE), "compare-old-csv", str(run_root),
        str(OLD_R6_CSV), str(comparison_path),
    ])
    comparison = parse_tsv(comparison_path)
    observed_shells = integer_list(summary["shell_counts"])
    count_pass = int(summary["target_unique_elements"]) == R6_EXPECTED
    shells_pass = observed_shells == R6_SHELLS
    set_pass = comparison["exact_key_set_equal"] == "1"
    rss = int(summary["peak_rss_bytes"])
    manifest: dict[str, object] = {
        "schema_version": "1.0",
        "task_id": "CM-GRP-GEO7-001",
        "phase": "R6_EXTERNAL_REGRESSION",
        "algorithm": "exact external Dirichlet-Voronoi center flood",
        "target_radius_over_a_B": 6,
        "simple_theorem_expansion_radius_over_a_B": "6.800895927193685166956845298951242796283512166915248265505749950383589236950287",
        "production_flood_radius_over_a_B": 6,
        "production_filter_basis": "GEO-FLOOD-2 exact Voronoi-center strengthening",
        "flood_generations": int(summary["flood_generations"]),
        "candidate_emissions": int(summary["candidate_emissions"]),
        "duplicate_emissions": int(summary["duplicate_emissions"]),
        "shell_counts": observed_shells,
        "candidate_counts_by_depth": integer_list(summary["candidate_counts_by_depth"]),
        "duplicate_counts_by_depth": integer_list(summary["duplicate_counts_by_depth"]),
        "target_unique_elements": int(summary["target_unique_elements"]),
        "expansion_unique_elements": int(summary["target_unique_elements"]),
        "frontier_exhausted": summary["frontier_exhausted"] == "1",
        "exact_boundary_fallbacks": int(summary["exact_boundary_fallbacks"]),
        "old_new_exact_key_set_equal": set_pass,
        "known_maximum_minimum_word_length": len(observed_shells) - 2,
        "registry": str(registry.relative_to(ROOT)).replace("\\", "/"),
        "registry_sha256": sha256(registry),
        "registry_bytes": registry.stat().st_size,
        "summary_sha256": sha256(summary_path),
        "comparison_sha256": sha256(comparison_path),
        "peak_rss_bytes": rss,
        "hard_rss_ceiling_bytes": HARD_RSS,
        "disk_bytes_after_finalization": tree_bytes(run_root) + registry.stat().st_size,
        "runtime_seconds_engine": float(summary["runtime_seconds"]),
        "runtime_seconds_phase": time.perf_counter() - started,
        "restart_semantics_exercised": "each depth is a fresh process resumed from the last atomic checkpoint",
        "acceptance": {
            "count_exact": count_pass,
            "shell_counts_exact": shells_pass,
            "frontier_empty": summary["frontier_exhausted"] == "1",
            "old_new_exact_key_set_equality": set_pass,
            "maximum_minimum_word_length_17": len(observed_shells) - 2 == 17,
            "rss_below_hard_ceiling": rss <= HARD_RSS,
        },
        "complete": count_pass and shells_pass and set_pass and rss <= HARD_RSS,
        "finished_utc": utc_now(),
    }
    write_json(DATA / "geo_ball_r6_manifest.json", manifest)
    return manifest


def forecast_from_r6(r6: dict[str, object]) -> dict[str, object]:
    # The hyperbolic-area ratio is used only for a resource forecast.  It is
    # not a word cutoff and does not participate in completeness.
    area_ratio = 21.266687037624642
    estimated_target = round(int(r6["target_unique_elements"]) * area_ratio)
    edge_ratio = int(r6["candidate_emissions"]) / int(r6["target_unique_elements"])
    estimated_emissions = round(estimated_target * edge_ratio)
    record_bytes = 147
    final_bytes = 24 + estimated_target * record_bytes
    free = shutil.disk_usage(ROOT).free
    forecast = {
        "schema_version": "2.0",
        "task_id": "CM-GRP-GEO7-001",
        "forecast_precedes_R7_run": True,
        "source": "measured exact external R=6 geometric flood plus hyperbolic area growth",
        "R6": {
            "target_count": r6["target_unique_elements"],
            "expansion_superball_count": r6["expansion_unique_elements"],
            "flood_generations": r6["flood_generations"],
            "candidate_emissions": r6["candidate_emissions"],
            "duplicate_emissions": r6["duplicate_emissions"],
            "duplicate_ratio": int(r6["duplicate_emissions"]) / int(r6["candidate_emissions"]),
            "peak_rss_bytes": r6["peak_rss_bytes"],
            "disk_bytes": r6["disk_bytes_after_finalization"],
            "runtime_seconds": r6["runtime_seconds_engine"],
        },
        "R7": {
            "target_count_estimate": estimated_target,
            "expansion_superball_count_estimate": estimated_target,
            "simple_R_plus_r_v_superball_not_used": True,
            "production_filter": "proved exact Voronoi-center criterion dist(o,h o)<=7a_B",
            "candidate_emissions_estimate": estimated_emissions,
            "temporary_disk_bytes_estimate": 450_000_000_000,
            "final_disk_bytes_estimate": final_bytes,
            "peak_rss_bytes_estimate": max(8 * 1024**3, int(r6["peak_rss_bytes"])),
            "runtime_seconds_interval": [14_400, 86_400],
        },
        "record_bytes": record_bytes,
        "normal_rss_target_bytes": 16 * 1024**3,
        "hard_rss_ceiling_bytes": HARD_RSS,
        "free_disk_bytes_before_R7": free,
        "disk_gate_pass": free > 450_000_000_000 + final_bytes,
        "no_swap": True,
        "generated_utc": utc_now(),
    }
    write_json(HERE / "CM_GRP_GEO7_001_RESOURCE_FORECAST.json", forecast)
    write_json(DATA / "CM_GRP_GEO7_001_RESOURCE_FORECAST.json", forecast)
    return forecast


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("r6", "forecast"), required=True)
    args = parser.parse_args()
    compile_engine()
    DATA.mkdir(parents=True, exist_ok=True)
    manifest_path = DATA / "geo_ball_r6_manifest.json"
    if args.phase == "r6":
        r6 = r6_phase()
        forecast = forecast_from_r6(r6)
        print(json.dumps({"r6": r6, "forecast": forecast}, indent=2, sort_keys=True))
        return 0 if r6["complete"] and forecast["disk_gate_pass"] else 1
    if not manifest_path.exists():
        raise SystemExit("R=6 regression manifest is missing")
    r6 = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(json.dumps(forecast_from_r6(r6), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
