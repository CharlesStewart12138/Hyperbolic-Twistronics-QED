#!/usr/bin/env python3
"""Snapshot the failed low-memory 24T8491 replay before exact-PID recovery."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
WRAPPER = BASE / "manifest_replay_jobs/gap_replay_24T8491_membership_seed12345_v4.g"
VERIFIER = BASE / "gap_verify_native_key_manifest_membership_v4.g"
MANIFEST = BASE / "manifests/24T8491/DEG24_KEY_24T8491_CLASS_MANIFEST_V3.g"
EXPECTED = BASE / "manifest_replay/DEG24_KEY_24T8491_MANIFEST_REPLAY_SEED12345_V3.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
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
    stdout_logs = sorted(BASE.glob("DEG24_KEY_24T8491_MEMBERSHIP_REPLAY_STDOUT_*.txt"), key=lambda p: p.stat().st_mtime_ns)
    stderr_logs = sorted(BASE.glob("DEG24_KEY_24T8491_MEMBERSHIP_REPLAY_STDERR_*.txt"), key=lambda p: p.stat().st_mtime_ns)
    latest_stdout = stdout_logs[-1]
    latest_stderr = stderr_logs[-1]
    payload = {
        "schema": "DEG24_NATIVE_REPLAY_24T8491_HANG_SNAPSHOT_V4",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "key_id": "24T8491",
        "gap_pid": 3031,
        "diagnosis_trigger": "GAP is sleeping in do_select with zero CPU time because an Error entered the interactive break loop.",
        "metadata_conflict": {
            "manifest_route": "native",
            "manifest_representation": "legacy_original_native",
            "verifier_required_route": "native",
            "verifier_incorrect_required_representation": "native",
        },
        "wrapper": {"path": WRAPPER.relative_to(ROOT).as_posix(), "sha256": sha256(WRAPPER)},
        "verifier": {"path": VERIFIER.relative_to(ROOT).as_posix(), "sha256": sha256(VERIFIER)},
        "manifest": {"path": MANIFEST.relative_to(ROOT).as_posix(), "sha256": sha256(MANIFEST)},
        "expected_output": {"path": EXPECTED.relative_to(ROOT).as_posix(), "exists": EXPECTED.exists()},
        "latest_stdout": {"path": latest_stdout.relative_to(ROOT).as_posix(), "size": latest_stdout.stat().st_size, "sha256": sha256(latest_stdout)},
        "latest_stderr": {"path": latest_stderr.relative_to(ROOT).as_posix(), "size": latest_stderr.stat().st_size, "sha256": sha256(latest_stderr)},
        "process_status": capture(["wsl.exe", "sh", "-lc", "cat /proc/3031/wchan; cat /proc/3031/status | grep -E '^(State|VmRSS|VmSwap|voluntary_ctxt_switches|nonvoluntary_ctxt_switches):'"]),
        "process_command": capture(["wsl.exe", "ps", "-p", "3031", "-o", "pid,ppid,stat,comm,rss,etimes,time,args"]),
        "recovery_constraints": [
            "Do not kill or alter unrelated EPW PID 1984.",
            "Do not restart the old generic 24T8491 replay.",
            "Preserve all V2 and V3 manifests.",
            "Consult GPT-5.6-sol before correcting and replaying.",
        ],
        "status": "SNAPSHOT_COMPLETE_REQUIRES_GPT56SOL_RECOVERY",
    }
    directory = BASE / "controller_recovery_snapshots" / f"native_replay_hang_24T8491_{stamp}_3031"
    directory.mkdir(parents=True, exist_ok=False)
    output = directory / "snapshot.json"
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"snapshot": output.relative_to(ROOT).as_posix(), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
