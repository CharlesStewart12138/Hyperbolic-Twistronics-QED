#!/usr/bin/env python3
"""Run an isolated two-process CLASS_ID_V3 checkpoint/resume smoke test."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\work\revise")
BASE = ROOT / "production_code/escalations/degree24_v3_repair"
SMOKE = BASE / "engine_checkpoint_resume_smoke"
CERT = BASE / "DEG24_SPLIT_HEAVY_ENGINE_CHECKPOINT_RESUME_SMOKE_V3.json"
KEY = 14186
SEGMENT_ID = "D24V3SMOKE_24T14186"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def gap_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def wsl_path(path: Path) -> str:
    return "/mnt/d/work/revise/" + path.relative_to(ROOT).as_posix()


def load_controller_module():
    path = BASE / "run_degree24_split_heavy_repair_controller_v4_gpt5.py"
    spec = importlib.util.spec_from_file_location("degree24_repair_controller_v4", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load V4 repair controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_segment() -> tuple[dict[str, str], list[str]]:
    manifest_dir = BASE / f"manifests/24T{KEY}"
    summary_path = manifest_dir / f"DEG24_KEY_24T{KEY}_CLASS_MANIFEST_V3.json"
    manifest_path = manifest_dir / f"DEG24_KEY_24T{KEY}_CLASS_MANIFEST_V3.tsv"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if sha_file(manifest_path) != summary["manifest_sha256"]:
        raise ValueError("smoke manifest hash mismatch")
    rows = list(csv.DictReader(manifest_path.open(encoding="utf-8"), delimiter="\t"))
    if len(rows) != 5:
        raise ValueError("smoke key no longer has exactly five classes")
    class_ids = [row["class_id_v3"] for row in rows]
    class_id_path = SMOKE / f"{SEGMENT_ID}.class_ids.txt"
    segment_path = SMOKE / f"{SEGMENT_ID}.g"
    with class_id_path.open("x", encoding="ascii", newline="\n") as handle:
        handle.write("\n".join(class_ids) + "\n")
    class_id_sha = sha_file(class_id_path)
    raw_pairs = summary["group_order"] * len(rows)
    with segment_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("D24C8_SEGMENT_META:=rec(\n")
        handle.write(
            f" segmentId:={gap_string(SEGMENT_ID)}, key:={KEY}, route:={gap_string(summary['gap_route'])}, representation:={gap_string(summary['representation'])},\n"
        )
        handle.write(
            f" groupOrder:={summary['group_order']}, autOrder:={summary['automorphism_group_order']}, parity:={summary['parity_maps']}, schema:={gap_string(summary['representation_schema'])},\n"
        )
        handle.write(
            f" generatorTupleSha256:={gap_string(summary['generator_tuple_sha256'])}, manifestSha256:={gap_string(summary['manifest_sha256'])}, classIdListSha256:={gap_string(class_id_sha)}, classCount:={len(rows)}, rawPairs:={raw_pairs});\n"
        )
        handle.write("D24C8_SEGMENT_RECORDS:=[\n")
        for index, row in enumerate(rows):
            images = ",".join("[" + value + "]" for value in row["representative_serialization"].split(";"))
            suffix = "," if index + 1 < len(rows) else ""
            handle.write(
                f"rec(classId:={gap_string(row['class_id_v3'])},manifestPositionDiagnostic:={row['manifest_position']},images:=[{images}],classSize:={row['class_size']},centralizerSize:={row['centralizer_size']},order:={row['order']}){suffix}\n"
            )
        handle.write("];\n")
    row = {
        "segment_id": SEGMENT_ID,
        "key_id": f"24T{KEY}",
        "class_count": str(len(rows)),
        "raw_pairs": str(raw_pairs),
        "class_id_first": class_ids[0],
        "class_id_last": class_ids[-1],
        "class_id_list": class_id_path.relative_to(ROOT).as_posix(),
        "class_id_list_sha256": class_id_sha,
        "segment_data": segment_path.relative_to(ROOT).as_posix(),
        "segment_data_sha256": sha_file(segment_path),
        "manifest_sha256": summary["manifest_sha256"],
    }
    return row, class_ids


def wrapper_text(row: dict[str, str], state: dict, output: Path, checkpoint: Path, tmp: Path, stop_after: str) -> str:
    counters = ",".join(str(value) for value in state["counters"])
    previous = wsl_path(state["previous_output"]) if state["previous_output"] else "NONE_FRESH_START"
    return (
        f'SEGMENT_FILE:="{wsl_path(ROOT / row["segment_data"])}"; EXPECTED_SEGMENT_FILE_SHA256:="{row["segment_data_sha256"]}";\n'
        f'OUT:="{wsl_path(output)}"; CHECKPOINT_FILE:="{wsl_path(checkpoint)}"; CHECKPOINT_TMP:="{wsl_path(tmp)}";\n'
        f'START_INDEX:={state["start_index"]}; INITIAL_COUNTERS:=[{counters}]; PREVIOUS_CHECKPOINT_SHA256:="{state["checkpoint_sha256"]}";\n'
        f'PREVIOUS_OUTPUT_FILE:="{previous}"; PREVIOUS_OUTPUT_PREFIX_BYTES:={state["previous_output_prefix_bytes"]}; PREVIOUS_OUTPUT_PREFIX_SHA256:="{state["previous_output_prefix_sha256"]}";\n'
        f'INTERNAL_GUARD_MS:=540000; STOP_AFTER_INDEX:={stop_after};\nRead("{wsl_path(BASE / "gap_run_degree24_split_heavy_segment_v3.g")}");\n'
    )


def run_gap(wrapper: Path, stdout_path: Path, stderr_path: Path) -> subprocess.CompletedProcess[bytes]:
    command = ["wsl.exe", "timeout", "--signal=TERM", "--kill-after=10s", "600s", "gap", "-q", wsl_path(wrapper)]
    process = subprocess.run(command, cwd=ROOT, capture_output=True)
    with stdout_path.open("xb") as handle:
        handle.write(process.stdout or b"")
    with stderr_path.open("xb") as handle:
        handle.write(process.stderr or b"")
    return process


def class_ids_done(path: Path) -> list[str]:
    result = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("CLASS_DONE\t"):
            fields = line.split("\t")
            result.append(fields[fields.index("CLASS_ID_V3") + 1])
    return result


def main() -> None:
    if CERT.exists() or SMOKE.exists():
        raise SystemExit("refusing to overwrite prior checkpoint/resume smoke evidence")
    SMOKE.mkdir(parents=True, exist_ok=False)
    controller = load_controller_module()
    row, expected_ids = write_segment()
    checkpoint = SMOKE / f"{SEGMENT_ID}_CHECKPOINT_V3.txt"
    tmp = SMOKE / f"{SEGMENT_ID}_CHECKPOINT_TMP_V3.txt"
    output1 = SMOKE / f"{SEGMENT_ID}_ATTEMPT001_V3.txt"
    wrapper1 = SMOKE / f"{SEGMENT_ID}_ATTEMPT001_V3.g"
    fresh = {
        "start_index": 1,
        "counters": [0] * 12,
        "checkpoint_sha256": "NONE_FRESH_START",
        "previous_output": None,
        "previous_output_prefix_bytes": 0,
        "previous_output_prefix_sha256": "NONE_FRESH_START",
    }
    with wrapper1.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(wrapper_text(row, fresh, output1, checkpoint, tmp, "1"))
    process1 = run_gap(wrapper1, SMOKE / "ATTEMPT001_STDOUT.bin", SMOKE / "ATTEMPT001_STDERR.bin")
    text1 = output1.read_text(encoding="utf-8") if output1.exists() else ""
    if process1.returncode != 0 or "STOPPED_RECOVERY_SMOKE\n" not in text1 or text1.endswith("DONE\n"):
        raise RuntimeError(f"first smoke process failed, rc={process1.returncode}")
    resumed = controller.read_checkpoint(checkpoint, row)
    if resumed["start_index"] != 2 or resumed["last_class_id"] != expected_ids[0]:
        raise ValueError("checkpoint did not bind the first CLASS_ID_V3")
    output2 = SMOKE / f"{SEGMENT_ID}_ATTEMPT002_V3.txt"
    wrapper2 = SMOKE / f"{SEGMENT_ID}_ATTEMPT002_V3.g"
    with wrapper2.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(wrapper_text(row, resumed, output2, checkpoint, tmp, "fail"))
    process2 = run_gap(wrapper2, SMOKE / "ATTEMPT002_STDOUT.bin", SMOKE / "ATTEMPT002_STDERR.bin")
    text2 = output2.read_text(encoding="utf-8") if output2.exists() else ""
    if process2.returncode != 0 or not text2.endswith("DONE\n") or "\nTOTAL\t" not in text2:
        raise RuntimeError(f"resume smoke process failed, rc={process2.returncode}")
    seen = class_ids_done(output1) + class_ids_done(output2)
    if seen != expected_ids or len(set(seen)) != len(expected_ids):
        raise ValueError("checkpoint/resume class coverage mismatch")
    final_state = controller.read_checkpoint(checkpoint, row)
    if final_state["start_index"] != len(expected_ids) + 1 or final_state["counters"][0] != len(expected_ids) or final_state["counters"][1] != int(row["raw_pairs"]):
        raise ValueError("final checkpoint totals mismatch")
    certificate = {
        "schema": "DEG24_SPLIT_HEAVY_ENGINE_CHECKPOINT_RESUME_SMOKE_V3",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "key_id": f"24T{KEY}",
        "segment_id": SEGMENT_ID,
        "process_count": 2,
        "first_process_stop_after_index": 1,
        "resume_start_index": resumed["start_index"],
        "last_committed_class_id_v3": resumed["last_class_id"],
        "expected_class_ids": expected_ids,
        "observed_class_ids": seen,
        "coverage_missing_count": len(set(expected_ids) - set(seen)),
        "coverage_duplicate_count": len(seen) - len(set(seen)),
        "class_units": final_state["counters"][0],
        "raw_pairs": final_state["counters"][1],
        "segment_data_sha256": row["segment_data_sha256"],
        "final_checkpoint_sha256": sha_file(checkpoint),
        "attempt1_output_sha256": sha_file(output1),
        "attempt2_output_sha256": sha_file(output2),
        "status": "PASS",
    }
    with CERT.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(certificate, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"certificate": CERT.relative_to(ROOT).as_posix(), "class_units": certificate["class_units"], "raw_pairs": certificate["raw_pairs"], "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
