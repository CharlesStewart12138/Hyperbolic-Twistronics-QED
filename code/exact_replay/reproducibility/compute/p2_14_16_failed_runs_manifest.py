"""Run P2-14-16 failed-run capture and provenance-manifest validation fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from provenance.run_manifest import compile_manifest, execute_registered_run


def successful_fixture(scale: float, count: int) -> dict[str, object]:
    values = [scale * index * index for index in range(count)]
    return {"count": count, "scale": scale, "sum": sum(values), "values": values}


def failed_fixture(message: str) -> dict[str, object]:
    raise ValueError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "provenance" / "p2_14_16_runs.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_16_failed_runs_manifest",
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    observed = []
    for specification in config["runs"]:
        parameters = dict(specification["parameters"])
        if specification["fixture"] == "success":
            function = lambda parameters=parameters: successful_fixture(
                float(parameters["scale"]), int(parameters["count"])
            )
        elif specification["fixture"] == "failure":
            function = lambda parameters=parameters: failed_fixture(str(parameters["message"]))
        else:
            raise ValueError(f"unknown fixture {specification['fixture']}")
        record = execute_registered_run(
            function,
            run_root=args.output_dir,
            run_id=str(specification["run_id"]),
            task_id="P2-14-16",
            command_label=str(specification["command_label"]),
            parameters=parameters,
        )
        observed.append({
            "run_id": specification["run_id"],
            "expected_status": specification["expected_status"],
            "observed_status": record["status"],
            "status_match": bool(record["status"] == specification["expected_status"]),
        })
    manifest = compile_manifest(args.output_dir, task_id="P2-14-16")
    checks = {
        "all_expected_statuses_match": bool(all(item["status_match"] for item in observed)),
        "success_run_preserved": bool(manifest["status_counts"]["success"] >= 1),
        "failed_run_preserved": bool(manifest["status_counts"]["failed"] >= 1),
        "all_artifact_hashes_verified": bool(manifest["all_artifact_hashes_verified"]),
        "manifest_run_count_matches": bool(manifest["run_count"] == len(config["runs"])),
    }
    failed_checks = sorted(name for name, passed in checks.items() if not passed)
    summary = {
        "task_id": "P2-14-16",
        "status": "PASS" if not failed_checks else "FAIL",
        "scientific_scope": "Failure/provenance harness validated; manuscript production runs are pending.",
        "checks": checks,
        "failed_checks": failed_checks,
        "observed_runs": observed,
        "manifest_file": "manifest.json",
        "manifest_csv_file": "manifest.csv",
        "manifest_status_counts": manifest["status_counts"],
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
