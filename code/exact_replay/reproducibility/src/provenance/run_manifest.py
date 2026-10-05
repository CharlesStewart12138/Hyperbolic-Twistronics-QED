"""Capture successful and failed runs and compile a minimal provenance manifest."""

from __future__ import annotations

import csv
import hashlib
import json
import traceback
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import TypeVar


Result = TypeVar("Result")


def canonical_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def execute_registered_run(
    function: Callable[[], Result],
    *,
    run_root: Path,
    run_id: str,
    task_id: str,
    command_label: str,
    parameters: dict[str, object],
) -> dict[str, object]:
    """Execute one callable and always persist a success or failure record."""
    if not run_id or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for character in run_id):
        raise ValueError("run_id must contain only letters, digits, underscores, or hyphens")
    run_dir = run_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    base = {
        "schema_version": 1,
        "run_id": run_id,
        "task_id": task_id,
        "command_label": command_label,
        "parameters": parameters,
        "parameters_sha256": canonical_sha256(parameters),
        "started_at_utc": started_at,
    }
    try:
        result = function()
        artifact_path = run_dir / "result.json"
        artifact_path.write_text(
            json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
        )
        record = {
            **base,
            "status": "success",
            "completed_at_utc": utc_now(),
            "artifact": "result.json",
            "artifact_sha256": file_sha256(artifact_path),
            "failure_type": None,
            "failure_message": None,
        }
    except Exception as error:
        artifact_path = run_dir / "failure.json"
        failure = {
            "error_type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
        }
        artifact_path.write_text(
            json.dumps(failure, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
        )
        record = {
            **base,
            "status": "failed",
            "completed_at_utc": utc_now(),
            "artifact": "failure.json",
            "artifact_sha256": file_sha256(artifact_path),
            "failure_type": type(error).__name__,
            "failure_message": str(error),
        }
    record_path = run_dir / "run_record.json"
    record_path.write_text(
        json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    return record


def compile_manifest(run_root: Path, *, task_id: str) -> dict[str, object]:
    records = []
    for record_path in sorted(run_root.glob("*/run_record.json")):
        record = json.loads(record_path.read_text(encoding="utf-8"))
        artifact_path = record_path.parent / str(record["artifact"])
        record["record_file"] = str(record_path.relative_to(run_root)).replace("\\", "/")
        record["artifact_file"] = str(artifact_path.relative_to(run_root)).replace("\\", "/")
        record["artifact_hash_verified"] = bool(
            artifact_path.is_file() and file_sha256(artifact_path) == record["artifact_sha256"]
        )
        records.append(record)
    records.sort(key=lambda record: str(record["run_id"]))
    status_counts = {
        "success": sum(record["status"] == "success" for record in records),
        "failed": sum(record["status"] == "failed" for record in records),
    }
    manifest = {
        "schema_version": 1,
        "task_id": task_id,
        "generated_at_utc": utc_now(),
        "run_count": len(records),
        "status_counts": status_counts,
        "all_artifact_hashes_verified": bool(all(record["artifact_hash_verified"] for record in records)),
        "runs": records,
    }
    (run_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )
    with (run_root / "manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "run_id", "task_id", "status", "command_label", "parameters_sha256",
            "started_at_utc", "completed_at_utc", "artifact_file", "artifact_sha256",
            "artifact_hash_verified", "failure_type", "failure_message", "record_file",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    return manifest
