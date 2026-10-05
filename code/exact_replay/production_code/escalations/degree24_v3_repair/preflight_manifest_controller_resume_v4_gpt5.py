#!/usr/bin/env python3
"""Independently seal the exact manifest-controller resume boundary."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"


def load_controller():
    path = BASE / "run_degree24_manifest_authoring_controller_v4_gpt5.py"
    spec = importlib.util.spec_from_file_location("manifest_controller_v4", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V4 manifest controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-valid", type=int, required=True)
    parser.add_argument("--expected-first-invalid", type=int, required=True)
    args = parser.parse_args()
    output = BASE / f"DEG24_MANIFEST_CONTROLLER_RESUME_PREFLIGHT_24T{args.expected_first_invalid}_V4.json"
    if output.exists():
        raise SystemExit(f"refusing to overwrite {output}")
    controller = load_controller()
    expected = {
        int(row["key"]): int(row["old_class_units"])
        for row in csv.DictReader(controller.SCOPE.open(encoding="utf-8"), delimiter="\t")
    }
    jobs = json.loads(controller.JOBS.read_text(encoding="utf-8"))["jobs"]
    valid = [int(job["key"]) for job in jobs if controller.manifest_valid(int(job["key"]), expected[int(job["key"])])]
    invalid = [int(job["key"]) for job in jobs if not controller.manifest_valid(int(job["key"]), expected[int(job["key"])])]
    first_invalid = invalid[0] if invalid else None
    source = BASE / f"manifest_sources/DEG24_KEY_24T{args.expected_first_invalid}_MANIFEST_SOURCE_V3.tsv"
    manifest = BASE / f"manifests/24T{args.expected_first_invalid}/DEG24_KEY_24T{args.expected_first_invalid}_CLASS_MANIFEST_V3.json"
    checks = {
        "job_count_806": len(jobs) == 806,
        "scope_count_806": len(expected) == 806,
        "valid_count": len(valid) == args.expected_valid,
        "first_invalid_key": first_invalid == args.expected_first_invalid,
        "resume_source_absent": not source.exists(),
        "resume_manifest_invalid": not controller.manifest_valid(args.expected_first_invalid, expected[args.expected_first_invalid]),
        "controller_lock_absent": not controller.LOCK.exists(),
    }
    if not all(checks.values()):
        raise ValueError(f"resume preflight failed: {checks}")
    certificate = {
        "schema": "DEG24_MANIFEST_CONTROLLER_RESUME_PREFLIGHT_V4",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "valid_manifest_count": len(valid),
        "invalid_manifest_count": len(invalid),
        "first_invalid_key": f"24T{first_invalid}",
        "resume_source_exists": source.exists(),
        "resume_manifest_exists": manifest.exists(),
        "checks": checks,
        "status": "PASS",
    }
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(certificate, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"certificate": output.relative_to(ROOT).as_posix(), "valid": len(valid), "first_invalid": f"24T{first_invalid}", "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
