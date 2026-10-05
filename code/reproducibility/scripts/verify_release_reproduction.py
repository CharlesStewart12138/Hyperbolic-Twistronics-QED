"""Run the complete executable reproduction chain for released evidence."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reproducibility/release_reproduction_report.json"

COMMANDS = [
    ("figures", [sys.executable, "reproducibility/figures/rebuild_all.py"]),
    ("raw_data", [sys.executable, "reproducibility/data/verify_raw_data_policy.py", "--output", "reproducibility/data/raw_data_policy_verification.json"]),
    ("caption_status", [sys.executable, "reproducibility/data/verify_caption_status.py"]),
    ("reported_uncertainty", [sys.executable, "reproducibility/data/verify_reported_uncertainty.py"]),
    ("abstract_values", [sys.executable, "reproducibility/data/verify_abstract_values.py"]),
    ("seed_policy", [sys.executable, "reproducibility/random/verify_seed_policy.py", "--output", "reproducibility/random/seed_verification.json"]),
    ("environment", [sys.executable, "reproducibility/scripts/verify_environment.py"]),
]

def main() -> int:
    records = []
    start_all = time.perf_counter()
    for name, command in COMMANDS:
        start = time.perf_counter()
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace")
        record = {
            "name": name,
            "command": command,
            "exit_code": proc.returncode,
            "elapsed_seconds": round(time.perf_counter() - start, 3),
            "stdout_tail": proc.stdout[-3000:],
            "stderr_tail": proc.stderr[-3000:],
            "status": "PASS" if proc.returncode == 0 else "FAIL",
        }
        records.append(record)
        print(f"{name}: {record['status']} ({record['elapsed_seconds']} s)")
        if proc.returncode != 0:
            break
    report = {
        "task_id": "P3-20-15",
        "status": "PASS" if len(records) == len(COMMANDS) and all(r["exit_code"] == 0 for r in records) else "FAIL",
        "python_executable": sys.executable,
        "steps_expected": len(COMMANDS),
        "steps_completed": len(records),
        "elapsed_seconds": round(time.perf_counter() - start_all, 3),
        "records": records,
        "scope": "released evaluated evidence only; absent production branches are not reproduced claims",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, indent=2))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
