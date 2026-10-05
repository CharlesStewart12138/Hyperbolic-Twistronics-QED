#!/usr/bin/env python3
"""Freeze the S0809 ENOMEM failure boundary before any V6 recovery attempt."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
SEGMENT = "D24V3S0809_24T15796"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def capture(command: list[str]) -> dict[str, object]:
    proc = subprocess.run(command, cwd=ROOT, capture_output=True)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout_hex": proc.stdout.hex(),
        "stderr_hex": proc.stderr.hex(),
    }


def main() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    target = BASE / "controller_recovery_snapshots" / f"repair_failure_{SEGMENT}_{stamp}"
    target.mkdir(parents=True, exist_ok=False)
    controller_stdout = sorted(BASE.glob("DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V6_STDOUT_*.txt"), key=lambda p: p.stat().st_mtime_ns)[-1]
    controller_stderr = sorted(BASE.glob("DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V6_STDERR_*.txt"), key=lambda p: p.stat().st_mtime_ns)[-1]
    paths = [
        BASE / "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_STATUS_V3.json",
        BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.tsv",
        BASE / "DEG24_SPLIT_HEAVY_COVERAGE_INDEPENDENT_AUDIT_V3.json",
        BASE / "run_degree24_split_heavy_repair_controller_v6_gpt5.py",
        BASE / "run_degree24_split_heavy_repair_controller_v5_gpt5.py",
        BASE / "run_degree24_split_heavy_repair_controller_v4_gpt5.py",
        BASE / "gap_run_degree24_split_heavy_segment_v3.g",
        BASE / f"repair_plan_segments/{SEGMENT}.class_ids.txt",
        BASE / f"repair_plan_segments/{SEGMENT}.g",
        BASE / f"repair_wrappers/{SEGMENT}_ATTEMPT001_V3.g",
        BASE / f"repair_outputs/{SEGMENT}_ATTEMPT001_V3.txt",
        BASE / f"repair_checkpoints/{SEGMENT}_CHECKPOINT_V3.txt",
        BASE / f"repair_logs/{SEGMENT}_ATTEMPT001_PROCESS.json",
        BASE / f"repair_logs/{SEGMENT}_ATTEMPT001_STDOUT.bin",
        BASE / f"repair_logs/{SEGMENT}_ATTEMPT001_STDERR.bin",
        controller_stdout,
        controller_stderr,
    ]
    records = []
    for source in paths:
        if not source.exists():
            raise FileNotFoundError(source)
        relative = source.relative_to(BASE)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        records.append({
            "source": source.relative_to(ROOT).as_posix(),
            "snapshot": destination.relative_to(ROOT).as_posix(),
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        })
    payload = {
        "schema": "DEG24_SPLIT_HEAVY_REPAIR_FAILURE_SNAPSHOT_V6",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "segment_id": SEGMENT,
        "attempt": 1,
        "controller_status": "STOPPED_REQUIRES_GPT56SOL_RECOVERY",
        "failure": "GAP StringFile(OUT) failed with Cannot allocate memory (12); break loop was later ended by external timeout rc=124.",
        "valid_completion_certificates": 808,
        "checkpoint_boundary": {
            "index": 139,
            "next_index": 140,
            "output_prefix_bytes": 126597,
            "output_prefix_sha256": "1b36a26ba6f9b9a36622ee4ae0c4a29598491958c8f08d6d3f7ccd25c1c5fd08",
            "checkpoint_sha256": "1128941418998f6bcceb5cf3aeeba79c7a74a811befcf5336500ba8181739a4d",
            "uncommitted_output_tail_bytes": 916,
            "resume_contract": "Preserve attempt 1 unchanged; V6 attempt 2 must recompute index 140 from the committed prefix.",
        },
        "gpt56sol_diagnosis": "Confirmed ENOMEM before the internal guard, valid checkpoint/prefix, and recommendation to wait for unrelated EPW memory pressure to clear before V6-only recovery.",
        "files": records,
        "wsl_memory": capture(["wsl.exe", "free", "-h"]),
        "wsl_top_rss": capture(["wsl.exe", "ps", "-eo", "pid,ppid,comm,rss,vsz,etimes,stat,args", "--sort=-rss"]),
        "constraints": [
            "Do not touch unrelated EPW PID 1984.",
            "Do not launch V2 or old V3/V4/V5 production entries.",
            "Do not delete or truncate the uncommitted attempt-1 tail.",
            "Resume only through V6 after memory pressure has cleared.",
        ],
        "status": "SNAPSHOT_COMPLETE_WAITING_FOR_MEMORY_SAFE_RECOVERY",
    }
    manifest = target / "snapshot_manifest.json"
    with manifest.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"snapshot": manifest.relative_to(ROOT).as_posix(), "files": len(records), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
