from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "production"
SHELL = DATA / "geometric_ball"
KERNEL = DATA / "local_full_kernel"
BUCKETS = SHELL / "shell_r6_r7" / "buckets"
OUTPUTS = KERNEL / "m7_tensor_buckets"
MANIFEST = KERNEL / "M7_TENSOR_BUCKET_MANIFEST.json"
WORK_LOG = ROOT / "CODE_WORK_LOG.md"
SHELL_MANIFEST = SHELL / "geo_shell_6_7_bucket_manifest.json"
ENGINE = ROOT / "production_code" / "hodge" / "geometric_ball_tensor_bucket.exe"
DISK_GATE = 250_000_000_000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def output_paths(index: int) -> tuple[Path, Path]:
    return OUTPUTS / f"bucket-{index:03d}.json", OUTPUTS / f"bucket-{index:03d}.acc.tsv"


def validate(index: int, expected_count: int) -> dict[str, object] | None:
    output_json, accumulator = output_paths(index)
    if not output_json.exists() or not accumulator.exists():
        return None
    try:
        value = json.loads(output_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        value.get("status") != "COMPLETE"
        or value.get("bucket") != index
        or value.get("elements_consumed") != expected_count
        or value.get("mpfr_precision_bits") != 192
        or value.get("directed_rounding_contract", "").find("RNDD") < 0
        or value.get("directed_rounding_contract", "").find("RNDU") < 0
    ):
        return None
    lower = value.get("partial_tensor_entrywise_lower")
    upper = value.get("partial_tensor_entrywise_upper")
    if not isinstance(lower, list) or not isinstance(upper, list) or len(lower) != 4 or len(upper) != 4:
        return None
    for i in range(4):
        if len(lower[i]) != 4 or len(upper[i]) != 4:
            return None
        for j in range(4):
            if float(lower[i][j]) > float(upper[i][j]):
                return None
    return value


def write_manifest(shell_entries: list[dict[str, object]], resumed: int) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for source in shell_entries:
        index = int(source["bucket"])
        expected_count = int(source["count"])
        value = validate(index, expected_count)
        if value is None:
            continue
        output_json, accumulator = output_paths(index)
        entries.append({
            "bucket": index,
            "status": "COMPLETE",
            "source_count": expected_count,
            "source_bytes": int(source["bytes"]),
            "source_sha256": source["sha256"],
            "elements_consumed": value["elements_consumed"],
            "unweighted_integer_trace_sum": value["unweighted_integer_trace_sum"],
            "maximum_transport_word_depth": value["maximum_transport_word_depth"],
            "peak_rss_bytes": value["peak_rss_bytes"],
            "elapsed_seconds": value["elapsed_seconds"],
            "tensor_json_sha256": sha256(output_json),
            "accumulator_sha256": sha256(accumulator),
        })
    previous_created = None
    restart_events = resumed
    if MANIFEST.exists():
        try:
            previous = json.loads(MANIFEST.read_text(encoding="utf-8"))
            previous_created = previous.get("created_utc")
            restart_events += int(previous.get("restart_events", 0))
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            pass
    result = {
        "schema_version": "1.0",
        "task_id": "CM-047-NP-M7-STREAM",
        "scope": "exact geometric shell 6a_B<d<=7a_B full 4D tensor",
        "status": "COMPLETE" if len(entries) == 256 else "IN_PROGRESS",
        "buckets_total": 256,
        "buckets_complete": len(entries),
        "elements_consumed_complete": sum(int(item["elements_consumed"]) for item in entries),
        "unweighted_integer_trace_sum_complete": sum(int(item["unweighted_integer_trace_sum"]) for item in entries),
        "peak_rss_bytes": max((int(item["peak_rss_bytes"]) for item in entries), default=0),
        "elapsed_seconds_sum": sum(float(item["elapsed_seconds"]) for item in entries),
        "restart_events": restart_events,
        "merge_order": "bucket index 000..255, then fixed adjacent binary tree",
        "mpfr_precision_bits": 192,
        "lower_rounding": "RNDD",
        "upper_rounding": "RNDU",
        "source_shell_sha256": "bbc94d6556b63a7aa2ac797cee68ff127e9153694d0eb35a885aa70db187afe7",
        "engine_sha256": sha256(ENGINE),
        "created_utc": previous_created or utc_now(),
        "updated_utc": utc_now(),
        "entries": entries,
    }
    temporary = MANIFEST.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, MANIFEST)
    return result


def update_work_log(progress: dict[str, object], last_bucket: int | None) -> None:
    """Replace one bounded checkpoint block after every sealed bucket."""
    start = "<!-- M7_BUCKET_PROGRESS_START -->"
    end = "<!-- M7_BUCKET_PROGRESS_END -->"
    block = (
        f"{start}\n"
        "### CM-047-NP-M7-STREAM live checkpoint\n\n"
        f"- Status: `{progress['status']}`\n"
        f"- Sealed buckets: `{progress['buckets_complete']}/256`\n"
        f"- Last submitted bucket: `{last_bucket if last_bucket is not None else 'none'}`\n"
        f"- Elements consumed: `{progress['elements_consumed_complete']}`\n"
        f"- Integer trace subtotal: `{progress['unweighted_integer_trace_sum_complete']}`\n"
        f"- Peak RSS: `{progress['peak_rss_bytes']}` bytes\n"
        f"- Manifest: `data/production/local_full_kernel/M7_TENSOR_BUCKET_MANIFEST.json`\n"
        f"- Updated UTC: `{progress['updated_utc']}`\n"
        f"{end}"
    )
    log_text = WORK_LOG.read_text(encoding="utf-8") if WORK_LOG.exists() else "# Code work log\n"
    left = log_text.find(start)
    right = log_text.find(end)
    if left >= 0 and right >= left:
        right += len(end)
        log_text = log_text[:left] + block + log_text[right:]
    else:
        log_text = log_text.rstrip() + "\n\n" + block + "\n"
    temporary = WORK_LOG.with_suffix(".md.tmp")
    temporary.write_text(log_text, encoding="utf-8")
    temporary.replace(WORK_LOG)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True, help="inclusive bucket index")
    args = parser.parse_args()
    if not (0 <= args.start <= args.stop < 256):
        raise SystemExit("bucket range must satisfy 0 <= start <= stop < 256")
    shell_manifest = json.loads(SHELL_MANIFEST.read_text(encoding="utf-8"))
    shell_entries = shell_manifest["entries"]
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    resumed = 0
    for index in range(args.start, args.stop + 1):
        expected_count = int(shell_entries[index]["count"])
        if validate(index, expected_count) is not None:
            resumed += 1
            print(f"already_complete bucket={index}", flush=True)
            continue
        free = shutil.disk_usage(ROOT.drive + "\\").free
        if free < DISK_GATE:
            raise RuntimeError(f"disk gate failed before tensor bucket {index}: {free}")
        output_json, accumulator = output_paths(index)
        for path in (output_json.with_suffix(".json.tmp"), accumulator.with_suffix(".tsv.tmp")):
            if path.exists():
                path.unlink()
        subprocess.run(
            [str(ENGINE), str(BUCKETS / f"bucket-{index:03d}.bin"), str(index),
             str(output_json), str(accumulator)],
            cwd=ROOT,
            check=True,
        )
        if validate(index, expected_count) is None:
            raise RuntimeError(f"tensor bucket {index} failed post-write validation")
        progress = write_manifest(shell_entries, resumed=0)
        update_work_log(progress, index)
        print(f"progress={progress['buckets_complete']}/256 elements={progress['elements_consumed_complete']}", flush=True)
    final = write_manifest(shell_entries, resumed=resumed)
    update_work_log(final, args.stop)
    print(json.dumps({
        "buckets_complete": final["buckets_complete"],
        "elements_consumed_complete": final["elements_consumed_complete"],
        "peak_rss_bytes": final["peak_rss_bytes"],
        "restart_events": final["restart_events"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
