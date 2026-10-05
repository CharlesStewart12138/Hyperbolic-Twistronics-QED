#!/usr/bin/env python3
"""Create an immutable, byte-exact snapshot of the failed V3 controller evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
SNAPSHOT_ROOT = BASE / "controller_recovery_snapshots"
EVIDENCE = (
    BASE / "run_degree24_manifest_authoring_controller_v3_gpt5.py",
    BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_STATUS_V3.json",
    BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_PROGRESS_V3.tsv",
    BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_STDOUT_V3.txt",
    BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_STDERR_V3.txt",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    snapshot = SNAPSHOT_ROOT / f"failure_v3_{stamp}_{os.getpid()}"
    snapshot.mkdir(parents=True, exist_ok=False)
    records = []
    for source in EVIDENCE:
        if not source.exists():
            records.append({"source": source.relative_to(ROOT).as_posix(), "exists": False})
            continue
        target = snapshot / source.name
        with source.open("rb") as reader, target.open("xb") as writer:
            shutil.copyfileobj(reader, writer, length=8 * 1024 * 1024)
        stat = source.stat()
        records.append(
            {
                "source": source.relative_to(ROOT).as_posix(),
                "snapshot": target.relative_to(ROOT).as_posix(),
                "exists": True,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "sha256": sha256(target),
            }
        )
    metadata = {
        "schema": "DEG24_MANIFEST_CONTROLLER_FAILURE_SNAPSHOT_V3",
        "created_utc": utc_now(),
        "purpose": "Byte-exact pre-recovery evidence; files are never overwritten by the V4 controller.",
        "diagnosed_root_cause": "Python text-mode subprocess reader failed on non-UTF-8 GAP stdout byte 0x8e; subprocess stdout became None before log persistence.",
        "validated_resume_state": {
            "valid_manifests": 25,
            "total_manifests": 806,
            "first_invalid_key": "24T9008",
            "source_24T9008_exists": False,
            "manifest_24T9008_exists": False,
            "legacy_lock_exists": (BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_V3.lock").exists(),
        },
        "files": records,
    }
    metadata_path = snapshot / "SNAPSHOT_METADATA.json"
    with metadata_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    seal_path = snapshot / "SNAPSHOT_SEAL.sha256"
    with seal_path.open("x", encoding="ascii", newline="\n") as handle:
        handle.write(f"{sha256(metadata_path)}  SNAPSHOT_METADATA.json\n")
        for record in records:
            if record.get("exists"):
                handle.write(f"{record['sha256']}  {Path(record['snapshot']).name}\n")
    print(json.dumps({"snapshot": snapshot.relative_to(ROOT).as_posix(), "file_count": sum(r.get("exists", False) for r in records), "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
