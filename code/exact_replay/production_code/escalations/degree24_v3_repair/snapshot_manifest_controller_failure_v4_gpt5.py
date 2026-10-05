#!/usr/bin/env python3
"""Seal one failed V4 manifest-controller state before any restart."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
SNAPSHOTS = BASE / "controller_recovery_snapshots"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("key", type=int)
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    snapshot = SNAPSHOTS / f"failure_v4_24T{args.key}_{stamp}_{os.getpid()}"
    snapshot.mkdir(parents=True, exist_ok=False)
    candidates = [
        BASE / "run_degree24_manifest_authoring_controller_v4_gpt5.py",
        BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_STATUS_V3.json",
        BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_PROGRESS_V3.tsv",
        *sorted(BASE.glob("DEG24_MANIFEST_AUTHORING_CONTROLLER_STDOUT_V4_*.bin")),
        *sorted(BASE.glob("DEG24_MANIFEST_AUTHORING_CONTROLLER_STDERR_V4_*.bin")),
        *sorted((BASE / f"manifest_logs/24T{args.key}").glob("*")),
    ]
    records = []
    for source in candidates:
        if not source.is_file():
            continue
        relative = source.relative_to(BASE)
        target_name = "__".join(relative.parts)
        target = snapshot / target_name
        with source.open("rb") as reader, target.open("xb") as writer:
            shutil.copyfileobj(reader, writer, length=8 * 1024 * 1024)
        records.append(
            {
                "source": source.relative_to(ROOT).as_posix(),
                "snapshot": target.relative_to(ROOT).as_posix(),
                "bytes": target.stat().st_size,
                "sha256": sha256(target),
            }
        )
    source_path = BASE / f"manifest_sources/DEG24_KEY_24T{args.key}_MANIFEST_SOURCE_V3.tsv"
    manifest_path = BASE / f"manifests/24T{args.key}/DEG24_KEY_24T{args.key}_CLASS_MANIFEST_V3.json"
    metadata = {
        "schema": "DEG24_MANIFEST_CONTROLLER_FAILURE_SNAPSHOT_V4",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "key_id": f"24T{args.key}",
        "source_exists": source_path.exists(),
        "manifest_exists": manifest_path.exists(),
        "lock_exists": (BASE / "DEG24_MANIFEST_AUTHORING_CONTROLLER_V3.lock").exists(),
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
            handle.write(f"{record['sha256']}  {Path(record['snapshot']).name}\n")
    print(json.dumps({"snapshot": snapshot.relative_to(ROOT).as_posix(), "files": len(records), "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
