"""Verify reconstructed pipeline manifests and preserve success/failure run records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "reproducibility" / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from provenance.run_manifest import compile_manifest, execute_registered_run, file_sha256


PIPELINE_MANIFESTS = (
    ("P2-14-R03", "reproducibility/data/euclidean_topic1_reconstruction/run_manifest.json"),
    ("P2-14-R04", "reproducibility/data/hyperbolic_geometry_reconstruction/run_manifest.json"),
    ("P2-14-R05", "reproducibility/data/hyperbolic_hamiltonian_reconstruction/run_manifest.json"),
    ("P2-14-R06", "reproducibility/data/hyperbolic_spectral_reconstruction/run_manifest.json"),
    ("P2-14-R07", "reproducibility/data/hyperbolic_representation_completion/run_manifest.json"),
    ("P2-14-R08", "reproducibility/data/hyperbolic_dos_reconstruction/run_manifest.json"),
    ("P2-14-R09", "reproducibility/data/hyperbolic_finite_cover_convergence/run_manifest.json"),
)


def verify_file_record(path: Path, record: dict[str, object]) -> dict[str, object]:
    declared_bytes = int(record["bytes"])
    declared_sha256 = str(record["sha256"])
    exists = path.is_file()
    observed_bytes = path.stat().st_size if exists else None
    observed_sha256 = file_sha256(path) if exists else None
    return {
        "path": path.relative_to(PROJECT_ROOT).as_posix() if path.is_relative_to(PROJECT_ROOT) else str(path),
        "exists": exists,
        "declared_bytes": declared_bytes,
        "observed_bytes": observed_bytes,
        "bytes_verified": bool(exists and observed_bytes == declared_bytes),
        "declared_sha256": declared_sha256,
        "observed_sha256": observed_sha256,
        "sha256_verified": bool(exists and observed_sha256 == declared_sha256),
    }


def verify_pipeline_manifest(expected_task_id: str, relative_manifest: str) -> dict[str, object]:
    manifest_path = PROJECT_ROOT / relative_manifest
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing pipeline manifest: {relative_manifest}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("task_id") != expected_task_id:
        raise ValueError(
            f"task identity mismatch for {relative_manifest}: "
            f"expected {expected_task_id}, observed {manifest.get('task_id')}"
        )
    status = str(manifest.get("status", ""))
    if "PASS" not in status:
        raise ValueError(f"pipeline manifest is not passing: {expected_task_id} status={status!r}")

    output_checks = [
        verify_file_record(manifest_path.parent / str(record["relative_path"]), record)
        for record in manifest.get("output_files", [])
    ]
    source_checks = [
        verify_file_record(PROJECT_ROOT / str(record["relative_path"]), record)
        for record in manifest.get("source_files", [])
    ]
    input_checks = [
        verify_file_record(PROJECT_ROOT / str(record["relative_path"]), record)
        for record in manifest.get("registered_inputs", [])
    ]
    all_checks = output_checks + source_checks + input_checks
    failed_files = [
        item["path"]
        for item in all_checks
        if not (item["bytes_verified"] and item["sha256_verified"])
    ]
    if failed_files:
        raise ValueError(f"manifest file verification failed: {failed_files}")
    return {
        "task_id": expected_task_id,
        "pipeline_status": status,
        "manifest_file": relative_manifest,
        "manifest_sha256": file_sha256(manifest_path),
        "declared_output_count": len(output_checks),
        "declared_source_count": len(source_checks),
        "declared_input_count": len(input_checks),
        "all_declared_files_verified": True,
        "output_checks": output_checks,
        "source_checks": source_checks,
        "input_checks": input_checks,
    }


def controlled_failure() -> dict[str, object]:
    raise ValueError("intentional P2-14-16 failure-preservation control")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "reproducibility" / "data" / "p2_14_16_registered_provenance",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    expected_run_ids: set[str] = set()
    for task_id, relative_manifest in PIPELINE_MANIFESTS:
        run_id = f"verify_{task_id.lower().replace('-', '_')}"
        record = execute_registered_run(
            lambda task_id=task_id, relative_manifest=relative_manifest: verify_pipeline_manifest(
                task_id, relative_manifest
            ),
            run_root=args.output_dir,
            run_id=run_id,
            task_id="P2-14-16",
            command_label=f"verify registered reconstruction manifest {task_id}",
            parameters={"pipeline_task_id": task_id, "manifest_file": relative_manifest},
        )
        expected_run_ids.add(run_id)
        if record["status"] != "success":
            print(json.dumps(record, indent=2, sort_keys=True, allow_nan=False))

    failure_run_id = "controlled_failure_preservation"
    execute_registered_run(
        controlled_failure,
        run_root=args.output_dir,
        run_id=failure_run_id,
        task_id="P2-14-16",
        command_label="controlled failure-preservation validation",
        parameters={"expected_exception": "ValueError", "scientific_run": False},
    )
    expected_run_ids.add(failure_run_id)

    manifest = compile_manifest(args.output_dir, task_id="P2-14-16")
    observed_statuses = {str(run["run_id"]): str(run["status"]) for run in manifest["runs"]}
    reconstruction_statuses = {
        task_id: observed_statuses[f"verify_{task_id.lower().replace('-', '_')}"]
        for task_id, _ in PIPELINE_MANIFESTS
    }
    failed_reconstruction_task_ids = sorted(
        task_id for task_id, status in reconstruction_statuses.items() if status == "failed"
    )
    checks = {
        "exact_registered_run_set": set(observed_statuses) == expected_run_ids,
        "seven_reconstruction_outcomes_preserved": len(reconstruction_statuses) == 7,
        "controlled_failure_status_correct": observed_statuses.get(failure_run_id) == "failed",
        "failed_run_preserved": manifest["status_counts"]["failed"] >= 1,
        "all_run_artifact_hashes_verified": bool(manifest["all_artifact_hashes_verified"]),
    }
    failed_checks = sorted(name for name, passed in checks.items() if not passed)
    summary = {
        "task_id": "P2-14-16",
        "status": "PASS" if not failed_checks else "FAIL",
        "scope": "REGISTERED_RECONSTRUCTION_MANIFEST_VERIFICATION_AND_FAILED_RUN_PRESERVATION",
        "scientific_limit": (
            "The indexed pipelines retain their own declared validation or partial-production scope; "
            "this provenance audit does not upgrade missing production inputs."
        ),
        "checks": checks,
        "failed_checks": failed_checks,
        "pipeline_task_ids": [task_id for task_id, _ in PIPELINE_MANIFESTS],
        "reconstruction_verification_statuses": reconstruction_statuses,
        "failed_reconstruction_task_ids": failed_reconstruction_task_ids,
        "manifest_file": "manifest.json",
        "manifest_csv_file": "manifest.csv",
        "manifest_run_count": manifest["run_count"],
        "manifest_status_counts": manifest["status_counts"],
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
