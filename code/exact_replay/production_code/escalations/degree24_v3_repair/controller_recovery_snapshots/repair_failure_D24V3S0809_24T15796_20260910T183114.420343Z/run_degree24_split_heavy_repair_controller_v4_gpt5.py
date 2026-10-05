#!/usr/bin/env python3
"""Binary-safe controller for the proof-gated V3 explicit-CLASS_ID repair plan."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import traceback
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
PLAN = BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.tsv"
PLAN_META = BASE / "DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.json"
COVERAGE = BASE / "DEG24_SPLIT_HEAVY_COVERAGE_CERTIFICATE_V3.json"
SAMPLE_CERT = BASE / "DEG24_MANIFEST_REPRODUCIBILITY_CERTIFICATE_V3.json"
ENGINE = BASE / "gap_run_degree24_split_heavy_segment_v3.g"
STATUS = BASE / "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_STATUS_V3.json"
PROGRESS = BASE / "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_PROGRESS_V3.tsv"
LOCK = BASE / "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3.lock"
WRAPPERS = BASE / "repair_wrappers"
OUTPUTS = BASE / "repair_outputs"
CHECKPOINTS = BASE / "repair_checkpoints"
LOGS = BASE / "repair_logs"
COMPLETIONS = BASE / "repair_completions"
CONTROLLER_VERSION = "V4_BINARY_CAPTURE"
COUNTER_FIELDS = [
    "CUM_UNITS",
    "CUM_RAW",
    "CUM_INVARIANT_ALPHA",
    "CUM_BETA",
    "CUM_INVERSE",
    "CUM_INVERSE_ODD",
    "CUM_ORBIT8",
    "CUM_RELATOR",
    "CUM_B3",
    "CUM_GENERATE",
    "CUM_CENTRALIZER_ORBITS",
    "CUM_CANDIDATE_NUMERIC",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
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


def win_from_wsl(path: str) -> Path:
    prefix = "/mnt/d/work/revise/"
    if not path.startswith(prefix):
        raise ValueError(f"unexpected output path {path}")
    return ROOT / path[len(prefix) :]


def parse_pairs(tokens: list[str]) -> dict[str, str]:
    if len(tokens) % 2:
        raise ValueError("odd key/value token count")
    return {tokens[index]: tokens[index + 1] for index in range(0, len(tokens), 2)}


def read_checkpoint(path: Path, row: dict[str, str]) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    lines = text.splitlines()
    if len(lines) != 3 or lines[0] != "CERTIFICATE_CHECKPOINT\tDEG24_SPLIT_HEAVY_REPAIR_V3" or lines[2] != "DONE":
        raise ValueError("checkpoint envelope")
    marker = "\tPAYLOAD_SHA256\t"
    payload, claimed = lines[1].rsplit(marker, 1)
    if sha_bytes(payload.encode("utf-8")) != claimed.lower():
        raise ValueError("checkpoint payload hash")
    fields = parse_pairs(payload.split("\t"))
    if fields["SEGMENT_ID"] != row["segment_id"] or fields["SEGMENT_FILE_SHA256"].lower() != row["segment_data_sha256"].lower():
        raise ValueError("checkpoint segment binding")
    previous = win_from_wsl(fields["OUTPUT_FILE"])
    prefix_bytes = int(fields["OUTPUT_PREFIX_BYTES"])
    data = previous.read_bytes()
    if len(data) < prefix_bytes or sha_bytes(data[:prefix_bytes]) != fields["OUTPUT_PREFIX_SHA256"].lower():
        raise ValueError("checkpoint output prefix")
    counters = [int(fields[name]) for name in COUNTER_FIELDS]
    return {
        "start_index": int(fields["NEXT_INDEX"]),
        "counters": counters,
        "checkpoint_sha256": sha_bytes(raw),
        "previous_output": previous,
        "previous_output_prefix_bytes": prefix_bytes,
        "previous_output_prefix_sha256": fields["OUTPUT_PREFIX_SHA256"].lower(),
        "last_class_id": fields["LAST_CLASS_ID_V3"],
    }


def completion_path(row: dict[str, str]) -> Path:
    return COMPLETIONS / f"{row['segment_id']}_COMPLETE_V3.json"


def completion_valid(row: dict[str, str]) -> bool:
    path = completion_path(row)
    if not path.exists():
        return False
    try:
        cert = json.loads(path.read_text(encoding="utf-8"))
        segment_data = ROOT / row["segment_data"]
        class_ids = ROOT / row["class_id_list"]
        checkpoint = ROOT / cert["final_checkpoint"]
        return (
            cert["schema"] == "DEG24_SPLIT_HEAVY_REPAIR_SEGMENT_COMPLETE_V3"
            and cert["status"] == "COMPLETE"
            and cert["segment_id"] == row["segment_id"]
            and cert["segment_data_sha256"] == row["segment_data_sha256"]
            and cert["class_id_list_sha256"] == row["class_id_list_sha256"]
            and cert["class_units"] == int(row["class_count"])
            and cert["raw_pairs"] == int(row["raw_pairs"])
            and segment_data.exists()
            and sha_file(segment_data) == row["segment_data_sha256"]
            and class_ids.exists()
            and sha_file(class_ids) == row["class_id_list_sha256"]
            and checkpoint.exists()
            and sha_file(checkpoint) == cert["final_checkpoint_sha256"]
            and bool(cert["output_parts"])
            and all(
                (ROOT / part["path"]).exists()
                and (ROOT / part["path"]).stat().st_size == part["bytes"]
                and sha_file(ROOT / part["path"]) == part["sha256"]
                for part in cert["output_parts"]
            )
        )
    except Exception:
        return False


def parse_total(path: Path) -> dict[str, str] | None:
    total = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("TOTAL\t"):
            total = parse_pairs(line.split("\t")[1:])
    return total


def finalize(row: dict[str, str], output: Path, checkpoint: Path) -> dict:
    total = parse_total(output)
    if not total or int(total["CLASS_UNITS"]) != int(row["class_count"]) or int(total["RAW_PAIRS"]) != int(row["raw_pairs"]):
        raise ValueError("terminal TOTAL mismatch")
    parts = []
    for path in sorted(OUTPUTS.glob(f"{row['segment_id']}_ATTEMPT*_V3.txt")):
        parts.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha_file(path)})
    certificate = {
        "schema": "DEG24_SPLIT_HEAVY_REPAIR_SEGMENT_COMPLETE_V3",
        "controller_version": CONTROLLER_VERSION,
        "segment_id": row["segment_id"],
        "key_id": row["key_id"],
        "class_units": int(total["CLASS_UNITS"]),
        "raw_pairs": int(total["RAW_PAIRS"]),
        "candidate_numeric": int(total["CANDIDATE_NUMERIC"]),
        "segment_data_sha256": row["segment_data_sha256"],
        "class_id_list_sha256": row["class_id_list_sha256"],
        "final_checkpoint": checkpoint.relative_to(ROOT).as_posix(),
        "final_checkpoint_sha256": sha_file(checkpoint),
        "output_parts": parts,
        "status": "COMPLETE",
        "completed_utc": now(),
    }
    atomic_json(completion_path(row), certificate)
    return certificate


def append_progress(event: str, row: dict[str, str], done: int, total: int, detail: str) -> None:
    new = not PROGRESS.exists()
    with PROGRESS.open("a", encoding="utf-8", newline="\n") as handle:
        if new:
            handle.write("utc\tevent\tsegment_id\tkey_id\tcompleted\ttotal\tdetail\n")
        handle.write(f"{now()}\t{event}\t{row['segment_id']}\t{row['key_id']}\t{done}\t{total}\t{detail}\n")


def wrapper_text(row: dict[str, str], state: dict, output: Path, checkpoint: Path, tmp: Path) -> str:
    counters = ",".join(str(value) for value in state["counters"])
    previous = wsl_path(state["previous_output"]) if state["previous_output"] else "NONE_FRESH_START"
    return (
        f'SEGMENT_FILE:="{wsl_path(ROOT / row["segment_data"])}"; EXPECTED_SEGMENT_FILE_SHA256:="{row["segment_data_sha256"]}";\n'
        f'OUT:="{wsl_path(output)}"; CHECKPOINT_FILE:="{wsl_path(checkpoint)}"; CHECKPOINT_TMP:="{wsl_path(tmp)}";\n'
        f'START_INDEX:={state["start_index"]}; INITIAL_COUNTERS:=[{counters}]; PREVIOUS_CHECKPOINT_SHA256:="{state["checkpoint_sha256"]}";\n'
        f'PREVIOUS_OUTPUT_FILE:="{previous}"; PREVIOUS_OUTPUT_PREFIX_BYTES:={state["previous_output_prefix_bytes"]}; PREVIOUS_OUTPUT_PREFIX_SHA256:="{state["previous_output_prefix_sha256"]}";\n'
        f'INTERNAL_GUARD_MS:=1320000; STOP_AFTER_INDEX:=fail;\nRead("{wsl_path(ENGINE)}");\n'
    )


def next_attempt(row: dict[str, str]) -> int:
    pattern = re.compile(re.escape(row["segment_id"]) + r"_ATTEMPT(\d+)")
    used = []
    for directory in (WRAPPERS, OUTPUTS, LOGS):
        for path in directory.glob(f"{row['segment_id']}_ATTEMPT*"):
            match = pattern.search(path.name)
            if match:
                used.append(int(match.group(1)))
    return max(used, default=0) + 1


def persist_process_logs(row: dict[str, str], attempt: int, process: subprocess.CompletedProcess[bytes]) -> None:
    stdout = process.stdout or b""
    stderr = process.stderr or b""
    stdout_path = LOGS / f"{row['segment_id']}_ATTEMPT{attempt:03d}_STDOUT.bin"
    stderr_path = LOGS / f"{row['segment_id']}_ATTEMPT{attempt:03d}_STDERR.bin"
    metadata_path = LOGS / f"{row['segment_id']}_ATTEMPT{attempt:03d}_PROCESS.json"
    with stdout_path.open("xb") as handle:
        handle.write(stdout)
    with stderr_path.open("xb") as handle:
        handle.write(stderr)
    with metadata_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(
            {
                "schema": "DEG24_SPLIT_HEAVY_REPAIR_PROCESS_ATTEMPT_V4",
                "controller_version": CONTROLLER_VERSION,
                "segment_id": row["segment_id"],
                "attempt": attempt,
                "returncode": process.returncode,
                "stdout_sha256": sha_bytes(stdout),
                "stdout_bytes": len(stdout),
                "stderr_sha256": sha_bytes(stderr),
                "stderr_bytes": len(stderr),
                "completed_utc": now(),
            },
            handle,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")


def completed_key_count(rows: list[dict[str, str]], valid: dict[str, bool]) -> int:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        groups[row["key_id"]].append(row["segment_id"])
    return sum(all(valid[segment_id] for segment_id in segment_ids) for segment_ids in groups.values())


def validate_gates() -> tuple[list[dict[str, str]], dict, dict]:
    sample = json.loads(SAMPLE_CERT.read_text(encoding="utf-8"))
    if sample.get("status") != "PASS" or sample.get("coverage_missing_count") != 0 or sample.get("coverage_duplicate_count") != 0:
        raise ValueError("independent manifest reproducibility gate not PASS")
    plan_meta = json.loads(PLAN_META.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    if (
        plan_meta.get("status") != "PASS"
        or coverage.get("status") != "PASS"
        or coverage.get("coverage_missing_count") != 0
        or coverage.get("coverage_extra_count") != 0
        or coverage.get("coverage_duplicate_count") != 0
        or coverage.get("every_class_id_occurs_exactly_once") is not True
    ):
        raise ValueError("coverage gate not PASS")
    if sha_file(PLAN) != plan_meta["plan_sha256"] or sha_file(COVERAGE) != plan_meta["coverage_certificate_sha256"]:
        raise ValueError("plan/certificate hash mismatch")
    rows = list(csv.DictReader(PLAN.open(encoding="utf-8"), delimiter="\t"))
    if len(rows) != plan_meta["segments"] or len(rows) != coverage["segments"]:
        raise ValueError("segment-count mismatch")
    if len({row["segment_id"] for row in rows}) != len(rows) or len({row["key_id"] for row in rows}) != 806:
        raise ValueError("segment/key identity mismatch")
    global_ids: set[str] = set()
    total_units = 0
    total_raw = 0
    for row in rows:
        data_path = ROOT / row["segment_data"]
        id_path = ROOT / row["class_id_list"]
        if sha_file(data_path) != row["segment_data_sha256"] or sha_file(id_path) != row["class_id_list_sha256"]:
            raise ValueError(f"segment input hash mismatch: {row['segment_id']}")
        ids = id_path.read_text(encoding="ascii").splitlines()
        if len(ids) != int(row["class_count"]) or len(set(ids)) != len(ids) or ids[0] != row["class_id_first"] or ids[-1] != row["class_id_last"]:
            raise ValueError(f"segment class-ID list mismatch: {row['segment_id']}")
        namespaced = {f"{row['key_id']}:{class_id}" for class_id in ids}
        if global_ids.intersection(namespaced):
            raise ValueError(f"global duplicate CLASS_ID assignment: {row['segment_id']}")
        global_ids.update(namespaced)
        total_units += len(ids)
        total_raw += int(row["raw_pairs"])
    if total_units != plan_meta["class_units"] or total_units != coverage["manifest_class_units"] or total_raw != plan_meta["raw_pairs"] or total_raw != coverage["v3_raw_pairs"]:
        raise ValueError("authoritative plan totals mismatch")
    return rows, plan_meta, coverage


def status_payload(status: str, stage: str, done: int, total: int, rows: list[dict[str, str]], valid: dict[str, bool], **extra: object) -> dict:
    payload = {
        "schema": "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3",
        "controller_version": CONTROLLER_VERSION,
        "status": status,
        "stage": stage,
        "completed_segments": done,
        "total_segments": total,
        "completed_keys": completed_key_count(rows, valid),
        "total_keys": 806,
        "updated_utc": now(),
    }
    payload.update(extra)
    return payload


def main() -> None:
    for directory in (WRAPPERS, OUTPUTS, CHECKPOINTS, LOGS, COMPLETIONS):
        directory.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, f"pid={os.getpid()} utc={now()} controller={CONTROLLER_VERSION}\n".encode("ascii"))
        os.close(fd)
    except FileExistsError:
        raise SystemExit("repair controller lock exists; refuse duplicate")
    rows: list[dict[str, str]] = []
    valid: dict[str, bool] = {}
    done = 0
    current: dict[str, str] | None = None
    try:
        rows, _, _ = validate_gates()
        total_segments = len(rows)
        valid = {row["segment_id"]: completion_valid(row) for row in rows}
        done = sum(valid.values())
        atomic_json(STATUS, status_payload("RUNNING", "AFFECTED_DOMAIN_RECOMPUTATION", done, total_segments, rows, valid))
        for row in rows:
            current = row
            if valid[row["segment_id"]]:
                continue
            checkpoint = CHECKPOINTS / f"{row['segment_id']}_CHECKPOINT_V3.txt"
            tmp = CHECKPOINTS / f"{row['segment_id']}_CHECKPOINT_TMP_V3.txt"
            if tmp.exists():
                raise RuntimeError(f"stale checkpoint tmp preserved: {tmp}")
            if checkpoint.exists():
                state = read_checkpoint(checkpoint, row)
            else:
                state = {
                    "start_index": 1,
                    "counters": [0] * 12,
                    "checkpoint_sha256": "NONE_FRESH_START",
                    "previous_output": None,
                    "previous_output_prefix_bytes": 0,
                    "previous_output_prefix_sha256": "NONE_FRESH_START",
                    "last_class_id": None,
                }
            while True:
                attempt = next_attempt(row)
                output = OUTPUTS / f"{row['segment_id']}_ATTEMPT{attempt:03d}_V3.txt"
                wrapper = WRAPPERS / f"{row['segment_id']}_ATTEMPT{attempt:03d}_V3.g"
                if output.exists() or wrapper.exists():
                    raise RuntimeError("attempt path collision")
                with wrapper.open("x", encoding="utf-8", newline="\n") as handle:
                    handle.write(wrapper_text(row, state, output, checkpoint, tmp))
                atomic_json(
                    STATUS,
                    status_payload(
                        "RUNNING",
                        "SEGMENT_EXECUTION",
                        done,
                        total_segments,
                        rows,
                        valid,
                        current_segment=row["segment_id"],
                        current_key=row["key_id"],
                        start_index=state["start_index"],
                        attempt=attempt,
                    ),
                )
                command = ["wsl.exe", "timeout", "--signal=TERM", "--kill-after=10s", "1400s", "gap", "-q", wsl_path(wrapper)]
                process = subprocess.run(command, cwd=ROOT, capture_output=True)
                persist_process_logs(row, attempt, process)
                if process.returncode != 0 or not output.exists():
                    raise RuntimeError(f"unexpected segment termination {row['segment_id']} attempt {attempt} rc={process.returncode}")
                output_text = output.read_text(encoding="utf-8")
                if output_text.endswith("DONE\n") and "\nTOTAL\t" in output_text:
                    certificate = finalize(row, output, checkpoint)
                    valid[row["segment_id"]] = True
                    done += 1
                    append_progress("SEGMENT_COMPLETE", row, done, total_segments, f"raw={certificate['raw_pairs']};candidates={certificate['candidate_numeric']}")
                    break
                if "STOPPED_GUARD\n" not in output_text:
                    raise RuntimeError(f"nonterminal segment output without normal guard stop: {row['segment_id']}")
                state = read_checkpoint(checkpoint, row)
                append_progress("SEGMENT_GUARD_RESUME", row, done, total_segments, f"next_index={state['start_index']}")
        certificates = [json.loads(completion_path(row).read_text(encoding="utf-8")) for row in rows]
        atomic_json(
            STATUS,
            status_payload(
                "ALL_AFFECTED_SEGMENTS_COMPLETE",
                "AFFECTED_DOMAIN_RECOMPUTATION_COMPLETE",
                total_segments,
                total_segments,
                rows,
                valid,
                class_units=sum(cert["class_units"] for cert in certificates),
                raw_pairs=sum(cert["raw_pairs"] for cert in certificates),
                candidate_numeric=sum(cert["candidate_numeric"] for cert in certificates),
            ),
        )
        print("ALL_AFFECTED_SEGMENTS_COMPLETE")
    except Exception as exc:
        atomic_json(
            STATUS,
            {
                "schema": "DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3",
                "controller_version": CONTROLLER_VERSION,
                "status": "STOPPED_REQUIRES_GPT56SOL_RECOVERY",
                "stage": "AFFECTED_DOMAIN_RECOMPUTATION",
                "completed_segments": done,
                "completed_keys": completed_key_count(rows, valid) if rows else 0,
                "current_segment": current["segment_id"] if current else None,
                "current_key": current["key_id"] if current else None,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "updated_utc": now(),
            },
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
