#!/usr/bin/env python3
"""Strict V6-only resume preflight after the S0809 ENOMEM incident."""
from __future__ import annotations

import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
V4 = BASE / "run_degree24_split_heavy_repair_controller_v4_gpt5.py"
STATUS = BASE / "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_STATUS_V3.json"
OBS1 = BASE / "DEG24_V6_MEMORY_SAFE_OBSERVATION_1.json"
OBS2 = BASE / "DEG24_V6_MEMORY_SAFE_OBSERVATION_2.json"
SNAPSHOT = BASE / "controller_recovery_snapshots/repair_failure_D24V3S0809_24T15796_20260910T183114.420343Z/snapshot_manifest.json"
OUTPUT = BASE / "DEG24_V6_V6_RECOVERY_PREFLIGHT_S0809.json"
SEGMENT_ID = "D24V3S0809_24T15796"


def load_v4():
    spec = importlib.util.spec_from_file_location("degree24_repair_v4", V4)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V4 implementation used by V6")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite {OUTPUT}")
    module = load_v4()
    rows, plan_meta, coverage = module.validate_gates()
    status = json.loads(STATUS.read_text(encoding="utf-8"))
    obs1 = json.loads(OBS1.read_text(encoding="utf-8"))
    obs2 = json.loads(OBS2.read_text(encoding="utf-8"))
    valid = {row["segment_id"]: module.completion_valid(row) for row in rows}
    valid_count = sum(valid.values())
    first_invalid = next(row for row in rows if not valid[row["segment_id"]])
    row = next(row for row in rows if row["segment_id"] == SEGMENT_ID)
    checkpoint = module.CHECKPOINTS / f"{SEGMENT_ID}_CHECKPOINT_V3.txt"
    checkpoint_tmp = module.CHECKPOINTS / f"{SEGMENT_ID}_CHECKPOINT_TMP_V3.txt"
    state = module.read_checkpoint(checkpoint, row)
    attempt2_paths = [
        module.WRAPPERS / f"{SEGMENT_ID}_ATTEMPT002_V3.g",
        module.OUTPUTS / f"{SEGMENT_ID}_ATTEMPT002_V3.txt",
        module.LOGS / f"{SEGMENT_ID}_ATTEMPT002_PROCESS.json",
        module.LOGS / f"{SEGMENT_ID}_ATTEMPT002_STDOUT.bin",
        module.LOGS / f"{SEGMENT_ID}_ATTEMPT002_STDERR.bin",
    ]
    memory_observations_valid = (
        obs1.get("status") == "FIRST_CONSECUTIVE_SAFE_OBSERVATION"
        and obs2.get("status") == "SECOND_CONSECUTIVE_SAFE_OBSERVATION"
        and obs1.get("wsl_available_gib", 0) >= 20
        and obs1.get("host_free_physical_gib", 0) >= 16
        and obs2.get("wsl_available_gib", 0) >= 20
        and obs2.get("host_free_physical_gib", 0) >= 16
        and obs1.get("observed_local", "") < obs2.get("observed_local", "")
    )
    checks = {
        "status_requires_recovery": status.get("status") == "STOPPED_REQUIRES_GPT56SOL_RECOVERY",
        "status_segment_s0809": status.get("current_segment") == SEGMENT_ID,
        "status_completed_808": status.get("completed_segments") == 808,
        "plan_segments_1006": len(rows) == 1006 and plan_meta.get("segments") == 1006 and coverage.get("segments") == 1006,
        "valid_completion_count_808": valid_count == 808,
        "first_invalid_is_s0809": first_invalid["segment_id"] == SEGMENT_ID,
        "controller_lock_absent": not module.LOCK.exists(),
        "checkpoint_tmp_absent": not checkpoint_tmp.exists(),
        "snapshot_exists": SNAPSHOT.exists(),
        "checkpoint_start_index_140": state["start_index"] == 140,
        "checkpoint_last_class_id": state["last_class_id"] == "8654b1d1c0662fc7d8b9d41876a9bd55fdfc806cada72b8fd453f59c9c939c6e",
        "checkpoint_sha256": state["checkpoint_sha256"] == "1128941418998f6bcceb5cf3aeeba79c7a74a811befcf5336500ba8181739a4d",
        "output_prefix_bytes": state["previous_output_prefix_bytes"] == 126597,
        "output_prefix_sha256": state["previous_output_prefix_sha256"] == "1b36a26ba6f9b9a36622ee4ae0c4a29598491958c8f08d6d3f7ccd25c1c5fd08",
        "attempt1_tail_preserved": state["previous_output"].stat().st_size == 127513,
        "next_attempt_is_2": module.next_attempt(row) == 2,
        "attempt2_paths_absent": not any(path.exists() for path in attempt2_paths),
        "two_consecutive_memory_observations": memory_observations_valid,
    }
    if not all(checks.values()):
        raise ValueError(f"V6 resume preflight failed: {checks}")
    certificate = {
        "schema": "DEG24_V6_RECOVERY_PREFLIGHT_S0809",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "segment_id": SEGMENT_ID,
        "valid_completion_certificates": valid_count,
        "first_invalid_segment": first_invalid["segment_id"],
        "resume_attempt": 2,
        "resume_start_index": state["start_index"],
        "committed_class_units": state["counters"][0],
        "checkpoint_sha256": state["checkpoint_sha256"],
        "previous_output_prefix_bytes": state["previous_output_prefix_bytes"],
        "previous_output_prefix_sha256": state["previous_output_prefix_sha256"],
        "checks": checks,
        "status": "PASS",
    }
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(certificate, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"certificate": OUTPUT.relative_to(ROOT).as_posix(), "status": "PASS", "resume_attempt": 2, "resume_start_index": 140}, sort_keys=True))


if __name__ == "__main__":
    main()
