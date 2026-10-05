#!/usr/bin/env python3
"""Binary-safe, restart-auditable authoring of all 806 V3 class manifests."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
SCOPE = BASE / "DEG24_SPLIT_HEAVY_KEYS_V3.tsv"
JOBS = BASE / "DEG24_MANIFEST_ALL_JOBS_V3.json"
STATUS = BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_STATUS_V3.json"
PROGRESS = BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_PROGRESS_V3.tsv"
LOCK = BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_V3.lock"
BUILDER = BASE / "build_key_authoritative_manifest_v3_gpt5.py"
CONTROLLER_VERSION = "V4_BINARY_CAPTURE"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, obj: dict) -> None:
    tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def wsl_path(path: Path) -> str:
    return "/mnt/d/work/revise/" + path.relative_to(ROOT).as_posix()


def source_valid(path: Path, classes: int) -> bool:
    if not path.exists():
        return False
    count = 0
    last = ""
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                last = line.rstrip("\r\n")
                if line.startswith("CLASS\t"):
                    count += 1
    except (OSError, UnicodeError):
        return False
    return count == classes and last == "DONE"


def manifest_valid(key: int, classes: int) -> bool:
    directory = BASE / f"manifests/24T{key}"
    summary_path = directory / f"DEG24_KEY_24T{key}_CLASS_MANIFEST_V3.json"
    if not summary_path.exists():
        return False
    try:
        manifest = json.loads(summary_path.read_text(encoding="utf-8"))
        tsv = ROOT / manifest["manifest"]
        gap = ROOT / manifest["gap_manifest"]
        return (
            manifest["key_id"] == f"24T{key}"
            and manifest["class_count"] == classes
            and manifest["class_id_count"] == classes
            and tsv.exists()
            and gap.exists()
            and sha(tsv) == manifest["manifest_sha256"]
            and sha(gap) == manifest["gap_manifest_sha256"]
        )
    except Exception:
        return False


def append_progress(event: str, key: int, completed: int, detail: str) -> None:
    new = not PROGRESS.exists()
    with PROGRESS.open("a", encoding="utf-8", newline="\n") as handle:
        if new:
            handle.write("utc\tevent\tkey\tcompleted\ttotal\tdetail\n")
        handle.write(f"{now()}\t{event}\t24T{key}\t{completed}\t806\t{detail}\n")


def write_exclusive(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)


def persist_attempt_logs(
    key: int,
    stage: str,
    command: list[str],
    returncode: int,
    stdout: bytes | None,
    stderr: bytes | None,
) -> Path:
    logdir = BASE / f"manifest_logs/24T{key}"
    logdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    stem = f"attempt_{stamp}_{os.getpid()}_{stage}"
    stdout_bytes = stdout or b""
    stderr_bytes = stderr or b""
    stdout_path = logdir / f"{stem}_stdout.bin"
    stderr_path = logdir / f"{stem}_stderr.bin"
    metadata_path = logdir / f"{stem}_metadata.json"
    write_exclusive(stdout_path, stdout_bytes)
    write_exclusive(stderr_path, stderr_bytes)
    metadata = {
        "schema": "DEG24_MANIFEST_AUTHORING_ATTEMPT_V4",
        "controller_version": CONTROLLER_VERSION,
        "utc": now(),
        "key_id": f"24T{key}",
        "stage": stage,
        "command": command,
        "returncode": returncode,
        "stdout": stdout_path.relative_to(ROOT).as_posix(),
        "stdout_size": len(stdout_bytes),
        "stdout_sha256": hashlib.sha256(stdout_bytes).hexdigest(),
        "stderr": stderr_path.relative_to(ROOT).as_posix(),
        "stderr_size": len(stderr_bytes),
        "stderr_sha256": hashlib.sha256(stderr_bytes).hexdigest(),
        "decoding_policy": "Raw subprocess bytes are authoritative; no implicit text decoding.",
    }
    with metadata_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return metadata_path


def status_payload(status: str, stage: str, completed: int, **extra: object) -> dict:
    payload = {
        "schema": "DEG24_MANIFEST_AUTHORING_CONTROLLER_V3",
        "controller_version": CONTROLLER_VERSION,
        "status": status,
        "stage": stage,
        "completed": completed,
        "total": 806,
        "updated_utc": now(),
    }
    payload.update(extra)
    return payload


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"pid={os.getpid()} utc={now()} controller={CONTROLLER_VERSION}\n".encode("ascii"))
        os.close(fd)
    except FileExistsError:
        raise SystemExit("controller lock exists; refuse duplicate")
    completed = 0
    current_key: int | None = None
    try:
        expected = {
            int(row["key"]): int(row["old_class_units"])
            for row in csv.DictReader(SCOPE.open(encoding="utf-8"), delimiter="\t")
        }
        jobs = json.loads(JOBS.read_text(encoding="utf-8"))["jobs"]
        if len(jobs) != 806 or {job["key"] for job in jobs} != set(expected):
            raise ValueError("job registry mismatch")
        valid_keys = [key for key, classes in expected.items() if manifest_valid(key, classes)]
        completed = len(valid_keys)
        first_invalid = next((int(job["key"]) for job in jobs if not manifest_valid(int(job["key"]), expected[int(job["key"])])), None)
        atomic_json(
            STATUS,
            status_payload(
                "RUNNING",
                "RECOVERY_AUDIT_COMPLETE",
                completed,
                valid_manifest_count=completed,
                first_invalid_key=None if first_invalid is None else f"24T{first_invalid}",
                recovery_contract="Skip only hash-valid manifests; preserve incomplete sources and all prior logs.",
            ),
        )
        if first_invalid is not None:
            append_progress("V4_BINARY_RECOVERY_START", first_invalid, completed, "validated exact manifest state before resume")
        for job in jobs:
            key = int(job["key"])
            current_key = key
            classes = expected[key]
            if manifest_valid(key, classes):
                continue
            source = ROOT / job["output"]
            wrapper = ROOT / job["wrapper"]
            if not source_valid(source, classes):
                if source.exists():
                    raise RuntimeError(f"incomplete source exists and is preserved: {source}")
                atomic_json(STATUS, status_payload("RUNNING", "EXPORT_SOURCE", completed, current_key=f"24T{key}"))
                command = ["wsl.exe", "gap", "-q", wsl_path(wrapper)]
                process = subprocess.run(command, cwd=ROOT, capture_output=True)
                stdout = process.stdout or b""
                stderr = process.stderr or b""
                log_metadata = persist_attempt_logs(key, "gap_export", command, process.returncode, stdout, stderr)
                pass_marker = f"MANIFEST_SOURCE_PASS\t24T{key}\tCLASSES\t{classes}".encode("ascii")
                if process.returncode != 0 or pass_marker not in stdout or not source_valid(source, classes):
                    raise RuntimeError(
                        f"GAP manifest export failed for 24T{key}, rc={process.returncode}, logs={log_metadata}"
                    )
            atomic_json(STATUS, status_payload("RUNNING", "SEAL_MANIFEST", completed, current_key=f"24T{key}"))
            command = [sys.executable, str(BUILDER), str(key)]
            process = subprocess.run(command, cwd=ROOT, capture_output=True)
            stdout = process.stdout or b""
            stderr = process.stderr or b""
            log_metadata = persist_attempt_logs(key, "seal_manifest", command, process.returncode, stdout, stderr)
            if process.returncode != 0 or not manifest_valid(key, classes):
                raise RuntimeError(
                    f"manifest sealing failed for 24T{key}, rc={process.returncode}, logs={log_metadata}"
                )
            completed += 1
            append_progress("MANIFEST_COMPLETE", key, completed, f"classes={classes};route={job['route']};controller={CONTROLLER_VERSION}")
        atomic_json(
            STATUS,
            status_payload(
                "ALL_MANIFESTS_COMPLETE_WAITING_COVERAGE_PLAN",
                "MANIFEST_AUTHORING_COMPLETE",
                806,
            ),
        )
        print("ALL_806_MANIFESTS_COMPLETE")
    except Exception as exc:
        atomic_json(
            STATUS,
            status_payload(
                "STOPPED_REQUIRES_GPT56SOL_RECOVERY",
                "MANIFEST_AUTHORING",
                completed,
                current_key=None if current_key is None else f"24T{current_key}",
                error=str(exc),
                traceback=traceback.format_exc(),
            ),
        )
        print(traceback.format_exc(), file=sys.stderr)
        raise
    finally:
        try:
            if LOCK.exists():
                LOCK.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
