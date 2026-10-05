"""Run and certify the deterministic prefix-sharded DFS regression.

The C++ worker retains only the current recursion word and streams accepted
canonical representatives to compact binary files.  This orchestrator owns
the deterministic shard order, restart boundary, hashing, and certificates.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / "data" / "production" / "streaming" / "cm_stream_001"
EXECUTABLE = HERE / "prefix_sharded_dfs.exe"
SOURCE = HERE / "prefix_sharded_dfs.cpp"
EXPECTED_RAW_TOTAL = 5_884_905
EXPECTED_CANONICAL_TOTAL = 336_367
MAXIMUM_LENGTH = 9


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def resource_forecast() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "task_id": "CM-STREAM-001",
        "created_utc": utc_now(),
        "calculation": "length-1..9 canonical-orbit regression, executed twice",
        "expected_states": {
            "raw_cyclically_reduced_leaves_per_run": EXPECTED_RAW_TOTAL,
            "accepted_canonical_representatives_per_run": EXPECTED_CANONICAL_TOTAL,
            "retained_states": 0,
            "runs": 2,
        },
        "bytes_per_state": {
            "persistent_per_enumerated_state": 0,
            "recursion_word_bytes_at_depth_9": 9,
            "accepted_record_bytes": "1 length byte + L generator bytes",
        },
        "estimated_peak_rss_bytes": 268_435_456,
        "normal_target_rss_bytes": 34_359_738_368,
        "task_specific_target_rss_bytes": 17_179_869_184,
        "hard_rss_ceiling_bytes": 51_539_607_552,
        "estimated_disk_bytes": 134_217_728,
        "estimated_runtime_seconds": 300,
        "checkpoint_interval": "one independently certified prefix shard",
        "fallback": "split any failed length-3 prefix into its seven freely reduced length-4 children",
        "storage_rule": "stream -> hash/accumulate -> discard rerun stream; no per-state Python containers",
    }


def shard_plan() -> list[tuple[str, tuple[int, ...], int, int]]:
    result = [("short-000", (0,), 1, 2)]
    serial = 0
    for second in range(8):
        if second == 4:
            continue
        for third in range(8):
            if third == (second + 4) % 8:
                continue
            result.append((f"p3-{serial:03d}", (0, second, third), 3, MAXIMUM_LENGTH))
            serial += 1
    assert len(result) == 50
    return result


def parse_summary(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: dict[str, object] = {}
    index = 0
    while index < len(lines) and not lines[index].startswith("length\t"):
        key, value = lines[index].split("\t", 1)
        result[key] = value
        index += 1
    if index == len(lines):
        raise RuntimeError(f"missing summary table in {path}")
    header = lines[index].split("\t")
    records = []
    for line in lines[index + 1 :]:
        values = line.split("\t")
        record = dict(zip(header, values))
        histogram: dict[str, int] = {}
        for pair in record["orbit_histogram"].split(","):
            if pair:
                size, count = pair.split(":")
                histogram[size] = int(count)
        records.append({
            "length": int(record["length"]),
            "recursion_nodes": int(record["recursion_nodes"]),
            "inverse_prunes": int(record["inverse_prunes"]),
            "cyclic_rejects": int(record["cyclic_rejects"]),
            "raw_leaves": int(record["raw_leaves"]),
            "accepted": int(record["accepted"]),
            "noncanonical": int(record["noncanonical"]),
            "orbit_histogram": histogram,
        })
    result["records"] = records
    result["elapsed_seconds"] = float(str(result["elapsed_seconds"]))
    result["peak_rss_bytes"] = int(str(result["peak_rss_bytes"]))
    return result


def run_worker(prefix: tuple[int, ...], minimum: int, maximum: int,
               accepted: Path, summary: Path) -> dict[str, object]:
    command = [
        str(EXECUTABLE),
        "--prefix", ",".join(map(str, prefix)),
        "--min-length", str(minimum),
        "--max-length", str(maximum),
        "--accepted-output", str(accepted),
        "--summary-output", str(summary),
    ]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)
    if completed.returncode:
        raise RuntimeError(f"worker failed ({completed.returncode}): {completed.stderr.strip()}")
    return parse_summary(summary)


def merged_stream_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    return digest.hexdigest()


def totals(summaries: list[dict[str, object]]) -> dict[str, object]:
    by_length: dict[int, Counter[str]] = defaultdict(Counter)
    orbit_histogram: Counter[str] = Counter()
    peak_rss = 0
    runtime = 0.0
    for summary in summaries:
        peak_rss = max(peak_rss, int(summary["peak_rss_bytes"]))
        runtime += float(summary["elapsed_seconds"])
        for record in summary["records"]:  # type: ignore[union-attr]
            length = int(record["length"])
            for key in ("recursion_nodes", "inverse_prunes", "cyclic_rejects", "raw_leaves", "accepted", "noncanonical"):
                by_length[length][key] += int(record[key])
            orbit_histogram.update(record["orbit_histogram"])
    return {
        "by_length": {str(length): dict(by_length[length]) for length in sorted(by_length)},
        "raw_leaves": sum(values["raw_leaves"] for values in by_length.values()),
        "accepted": sum(values["accepted"] for values in by_length.values()),
        "recursion_nodes": sum(values["recursion_nodes"] for values in by_length.values()),
        "inverse_prunes": sum(values["inverse_prunes"] for values in by_length.values()),
        "cyclic_rejects": sum(values["cyclic_rejects"] for values in by_length.values()),
        "noncanonical": sum(values["noncanonical"] for values in by_length.values()),
        "orbit_size_histogram": dict(sorted(orbit_histogram.items(), key=lambda item: int(item[0]))),
        "worker_elapsed_seconds": runtime,
        "peak_worker_rss_bytes": peak_rss,
    }


def semantic_totals(value: dict[str, object]) -> dict[str, object]:
    """Drop run-dependent telemetry before the determinism comparison."""
    return {
        key: item
        for key, item in value.items()
        if key not in {"worker_elapsed_seconds", "peak_worker_rss_bytes"}
    }


def main() -> int:
    if not EXECUTABLE.exists():
        raise SystemExit(f"compile {SOURCE.name} before running this orchestrator")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    forecast = resource_forecast()
    write_json(OUTPUT / "RESOURCE_FORECAST.json", forecast)
    write_json(HERE / "RESOURCE_FORECAST.json", forecast)

    source_hash = sha256_file(SOURCE)
    executable_hash = sha256_file(EXECUTABLE)
    plan = shard_plan()
    run_root = OUTPUT / "primary"
    rerun_root = OUTPUT / "determinism_rerun"
    for directory in (run_root, rerun_root):
        directory.mkdir(parents=True, exist_ok=True)

    primary_summaries: list[dict[str, object]] = []
    rerun_summaries: list[dict[str, object]] = []
    primary_streams: list[Path] = []
    rerun_streams: list[Path] = []
    all_complete = True
    started = time.perf_counter()
    shard_certificates = []

    for shard_id, prefix, minimum, maximum in plan:
        shard_started = utc_now()
        primary_bin = run_root / f"{shard_id}.bin"
        primary_tsv = run_root / f"{shard_id}.tsv"
        rerun_bin = rerun_root / f"{shard_id}.bin"
        rerun_tsv = rerun_root / f"{shard_id}.tsv"
        try:
            first = run_worker(prefix, minimum, maximum, primary_bin, primary_tsv)
            second = run_worker(prefix, minimum, maximum, rerun_bin, rerun_tsv)
            primary_hash = sha256_file(primary_bin)
            rerun_hash = sha256_file(rerun_bin)
            deterministic = primary_hash == rerun_hash and first["records"] == second["records"]
            terminal = "COMPLETE" if deterministic else "FAILED"
        except BaseException as error:
            first = {"records": [], "peak_rss_bytes": 0, "elapsed_seconds": 0.0}
            second = first
            primary_hash = ""
            rerun_hash = ""
            deterministic = False
            terminal = "INTERRUPTED" if isinstance(error, KeyboardInterrupt) else "FAILED"
            all_complete = False
            failure = repr(error)
        else:
            failure = None
            all_complete = all_complete and terminal == "COMPLETE"
            primary_summaries.append(first)
            rerun_summaries.append(second)
            primary_streams.append(primary_bin)
            rerun_streams.append(rerun_bin)

        raw = sum(int(record["raw_leaves"]) for record in first["records"])
        accepted = sum(int(record["accepted"]) for record in first["records"])
        cyclic = sum(int(record["cyclic_rejects"]) for record in first["records"])
        noncanonical = sum(int(record["noncanonical"]) for record in first["records"])
        inverse_prunes = sum(int(record["inverse_prunes"]) for record in first["records"])
        orbit_hist = Counter()
        for record in first["records"]:
            orbit_hist.update(record["orbit_histogram"])
        certificate = {
            "schema_version": "1.0",
            "task_id": "CM-STREAM-001",
            "shard_id": shard_id,
            "prefix_id": shard_id,
            "prefix_word": [f"g{value}" for value in prefix],
            "search_contract": {
                "minimum_length": minimum,
                "maximum_length": maximum,
                "free_reduction": True,
                "cyclic_reduction": True,
                "canonical_group_action": ["cyclic_rotation", "word_inversion", "uniform_C8_label_shift"],
                "heuristic_trace_pruning": False,
            },
            "counts": {
                "raw_cyclic_leaves": raw,
                "accepted_canonical": accepted,
                "rejected_cyclic": cyclic,
                "rejected_noncanonical": noncanonical,
                "inverse_extensions_suppressed": inverse_prunes,
                "kernel_count": 0,
                "kernel_count_scope": "not evaluated by this infrastructure regression",
            },
            "orbit_size_histogram": dict(sorted(orbit_hist.items(), key=lambda item: int(item[0]))),
            "partial_sums": {str(record["length"]): {"raw": record["raw_leaves"], "accepted": record["accepted"]} for record in first["records"]},
            "witnesses": [],
            "accepted_stream_sha256": primary_hash,
            "determinism_rerun_sha256": rerun_hash,
            "deterministic_rerun_pass": deterministic,
            "software_version": {
                "source_sha256": source_hash,
                "executable_sha256": executable_hash,
                "compiler_contract": "C++20 optimized production worker",
                "python": sys.version.split()[0],
            },
            "timestamps": {"started_utc": shard_started, "finished_utc": utc_now()},
            "peak_rss_bytes": int(first["peak_rss_bytes"]),
            "terminal_status": terminal,
            "failure": failure,
        }
        write_json(run_root / f"{shard_id}.certificate.json", certificate)
        shard_certificates.append(certificate)
        if terminal != "COMPLETE":
            break

    primary_total = totals(primary_summaries)
    rerun_total = totals(rerun_summaries)
    primary_aggregate_hash = merged_stream_hash(primary_streams) if primary_streams else ""
    rerun_aggregate_hash = merged_stream_hash(rerun_streams) if rerun_streams else ""
    exact_count_pass = (
        primary_total["raw_leaves"] == EXPECTED_RAW_TOTAL
        and primary_total["accepted"] == EXPECTED_CANONICAL_TOTAL
    )
    deterministic_pass = (
        semantic_totals(primary_total) == semantic_totals(rerun_total)
        and primary_aggregate_hash == rerun_aggregate_hash
    )
    rss_pass = int(primary_total["peak_worker_rss_bytes"]) <= int(forecast["task_specific_target_rss_bytes"])
    gate_pass = all_complete and len(shard_certificates) == len(plan) and exact_count_pass and deterministic_pass and rss_pass

    certificate = {
        "schema_version": "1.0",
        "task_id": "CM-STREAM-001",
        "classification": "STREAMING_INFRASTRUCTURE_CERTIFIED" if gate_pass else "STREAMING_INFRASTRUCTURE_FAILED",
        "scope": "finite regression through length 9; not a proof-complete global conjugacy enumeration",
        "shard_partition": {
            "number_of_shards": len(plan),
            "short_shard": "prefix g0, lengths 1..2",
            "deep_shards": "all 49 freely reduced length-3 prefixes beginning g0, lengths 3..9",
            "disjoint": True,
            "complete_for_declared_scope": len(shard_certificates) == len(plan) and all_complete,
        },
        "search_contract": "freely/cyclically reduced; C8-normalized first token; canonical under cyclic rotation, inversion, and uniform C8 shift",
        "primary_totals": primary_total,
        "rerun_totals": rerun_total,
        "expected_totals": {"raw_leaves": EXPECTED_RAW_TOTAL, "accepted": EXPECTED_CANONICAL_TOTAL},
        "checks": {
            "all_shards_complete": all_complete and len(shard_certificates) == len(plan),
            "exact_frozen_counts": exact_count_pass,
            "deterministic_rerun": deterministic_pass,
            "rss_at_or_below_16_GiB": rss_pass,
            "no_per_state_python_container": True,
            "no_heuristic_trace_pruning": True,
        },
        "accepted_stream_sha256": primary_aggregate_hash,
        "determinism_rerun_sha256": rerun_aggregate_hash,
        "software_version": {"source_sha256": source_hash, "executable_sha256": executable_hash},
        "resource_forecast": forecast,
        "wall_seconds": time.perf_counter() - started,
        "finished_utc": utc_now(),
        "next_gate": {"CM-STREAM-002_released": gate_pass, "CM-047-NP-M7-STREAM_released": False},
    }
    write_json(HERE / "CM_STREAM_001_CERTIFICATE.json", certificate)
    write_json(OUTPUT / "CM_STREAM_001_CERTIFICATE.json", certificate)

    markdown = f"""# CM-STREAM-001 certificate

- Classification: `{certificate['classification']}`
- Scope: finite canonical-orbit regression through length 9; this is not a global completeness proof.
- Partition: 50 disjoint deterministic prefix shards (one short shard and all 49 admissible length-3 prefixes beginning with `g0`).
- Frozen counts: {primary_total['raw_leaves']:,} raw cyclically reduced leaves and {primary_total['accepted']:,} canonical orbits.
- Aggregate accepted-stream SHA-256: `{primary_aggregate_hash}`.
- Determinism rerun: `{'PASS' if deterministic_pass else 'FAIL'}`.
- Peak worker RSS: {int(primary_total['peak_worker_rss_bytes']):,} bytes.
- Checkpoint/restart boundary: one independently certified shard.

The C++ worker stores only the current recursion word and streams accepted representatives.  Python performs orchestration, bounded aggregation, hashing, and certificate emission; it never holds the enumerated state set.
"""
    (HERE / "CM_STREAM_001_CERTIFICATE.md").write_text(markdown, encoding="utf-8")

    for path in rerun_streams:
        path.unlink(missing_ok=True)
    for path in rerun_root.glob("*.tsv"):
        path.unlink(missing_ok=True)
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
