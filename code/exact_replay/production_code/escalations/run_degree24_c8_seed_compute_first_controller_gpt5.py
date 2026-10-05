#!/usr/bin/env python3
"""Compute-first controller for Degree-24 seed shards.

The controller performs only the frozen minimum per shard: build/parse, one
GAP run, numerical aggregate, atomic COMPLETE, and immediate next-shard
launch.  It stops on any nonzero exit or nonterminal shard so that recovery is
explicit and no committed unit is replayed.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


B = Path(__file__).resolve().parent
BUILDER = B / "build_degree24_c8_seed_shard_generic_v7_gpt56sol.py"
FINALIZER = B / "finalize_degree24_c8_seed_shard_minimal_generic_gpt56sol.py"
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
PROGRESS = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_PROGRESS_GPT56SOL.tsv"
STATUS = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_CONTROLLER_STATUS_GPT5.json"
LOG = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_CONTROLLER_GPT5.log"
LOCK = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_CONTROLLER_GPT5.lock"


def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    if tmp.exists():
        raise RuntimeError(f"stale temp: {tmp}")
    with tmp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, path)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def note(message: str) -> None:
    line = f"{stamp()}\t{message}\n"
    with LOG.open("a", encoding="ascii", newline="") as stream:
        stream.write(line)
        stream.flush()
        os.fsync(stream.fileno())


def state(**values: object) -> None:
    payload = {"updated_utc": stamp(), **values}
    atomic_write(STATUS, (json.dumps(payload, sort_keys=True) + "\n").encode("ascii"))


def run_to_files(command: list[str], stdout_path: Path, stderr_path: Path) -> int:
    if stdout_path.exists() or stderr_path.exists():
        raise RuntimeError(f"no-clobber run logs: {stdout_path.name}")
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        process = subprocess.run(command, stdout=stdout, stderr=stderr, check=False)
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    return process.returncode


def planned_totals() -> dict[int, tuple[int, int]]:
    result: dict[int, tuple[int, int]] = {}
    for line in PLAN.read_text(encoding="ascii").splitlines():
        parts = line.split("\t")
        if parts[:1] == ["SHARD"]:
            row = dict(zip(parts[2::2], parts[3::2], strict=True))
            result[int(parts[1])] = (int(row["CLASS_UNITS"]), int(row["RAW_PAIRS"]))
    assert len(result) == 905
    return result


def completed_set() -> set[int]:
    result: set[int] = set()
    lines = PROGRESS.read_text(encoding="ascii").splitlines()
    for line in lines[1:]:
        if line:
            result.add(int(line.split("\t", 1)[0]))
    return result


parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, required=True)
parser.add_argument("--end", type=int, default=905)
args = parser.parse_args()
assert 6 <= args.start <= args.end <= 905

lock_fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    os.write(lock_fd, f"PID\t{os.getpid()}\nSTART\t{args.start}\nEND\t{args.end}\n".encode("ascii"))
    os.fsync(lock_fd)
finally:
    os.close(lock_fd)

try:
    totals = planned_totals()
    note(f"CONTROLLER_START\tPID\t{os.getpid()}\tSTART\t{args.start}\tEND\t{args.end}")
    for shard in range(args.start, args.end + 1):
        tag = f"{shard:03d}"
        marker = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_COMPLETE_GPT56SOL.txt"
        completed = completed_set()
        if shard in completed:
            if not marker.exists():
                raise RuntimeError(f"progress/marker mismatch shard{tag}")
            note(f"SKIP_COMPLETE\tSHARD\t{tag}")
            continue
        if any(done > shard for done in completed):
            raise RuntimeError(f"non-prefix progress before shard{tag}")
        if marker.exists():
            raise RuntimeError(f"marker/progress mismatch shard{tag}")

        state(status="BUILDING", shard=shard, completed=shard - 1,
              units=totals[shard][0], raw_pairs=totals[shard][1], candidates=0)
        build_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_BUILD_STDOUT_GPT5.txt"
        build_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_BUILD_STDERR_GPT5.txt"
        rc = run_to_files([sys.executable, str(BUILDER), "--shard", str(shard)], build_out, build_err)
        if rc != 0:
            raise RuntimeError(f"builder exit {rc} shard{tag}")

        parse_script = B / f"gap_parse_smoke_degree24_c8_seed_shard{tag}_v7_gpt56sol.g"
        parse_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PARSE_SMOKE_STDOUT_GPT5.txt"
        parse_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PARSE_SMOKE_STDERR_GPT5.txt"
        wsl_parse = "/mnt/d/work/revise/production_code/escalations/" + parse_script.name
        rc = run_to_files(["wsl.exe", "bash", "-lc", f"gap -q {wsl_parse}"], parse_out, parse_err)
        if rc != 0 or f"SHARD{tag}_V7_WRAPPER_ENGINE_PARSE_PASS" not in parse_out.read_text(encoding="ascii"):
            raise RuntimeError(f"parse smoke failed shard{tag}, exit {rc}")

        state(status="RUNNING", shard=shard, completed=shard - 1,
              units=totals[shard][0], raw_pairs=totals[shard][1], candidates=0)
        runner = B / f"run_degree24_c8_seed_shard{tag}_segment001_postverify_v7.sh"
        run_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT001_RUN_STDOUT_V7_GPT5.txt"
        run_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT001_RUN_STDERR_V7_GPT5.txt"
        wsl_runner = "/mnt/d/work/revise/production_code/escalations/" + runner.name
        started = time.monotonic()
        rc = run_to_files(["wsl.exe", "bash", wsl_runner], run_out, run_err)
        wall = round(time.monotonic() - started, 3)
        if rc != 0:
            raise RuntimeError(f"GAP exit {rc} shard{tag} after {wall}s")

        state(status="FINALIZING", shard=shard, completed=shard - 1,
              units=totals[shard][0], raw_pairs=totals[shard][1], candidates=0, wall_seconds=wall)
        final_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_MINIMAL_FINALIZE_STDOUT_GPT5.txt"
        final_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_MINIMAL_FINALIZE_STDERR_GPT5.txt"
        rc = run_to_files([sys.executable, str(FINALIZER), "--shard", str(shard)], final_out, final_err)
        if rc != 0 or not marker.exists():
            raise RuntimeError(f"minimal finalizer failed shard{tag}, exit {rc}")
        final_text = final_out.read_text(encoding="ascii")
        candidate_token = "CANDIDATES="
        candidate_count = int(final_text.split(candidate_token, 1)[1].split()[0])
        note(f"COMPLETE\tSHARD\t{tag}\tUNITS\t{totals[shard][0]}\tRAW\t{totals[shard][1]}\tCANDIDATES\t{candidate_count}\tWALL_SECONDS\t{wall}")
        state(status="COMPLETE_LAUNCHING_NEXT", shard=shard, completed=shard,
              units=totals[shard][0], raw_pairs=totals[shard][1],
              candidates=candidate_count, wall_seconds=wall)
        if shard % 50 == 0:
            milestone = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_MILESTONE_{tag}_GPT5.txt"
            atomic_write(milestone, (
                f"MILESTONE\t{tag}\tOF\t905\nSTATUS\tCOMPUTE_FIRST_IN_PROGRESS\n"
                f"LATEST_SHARD_UNITS\t{totals[shard][0]}\nLATEST_SHARD_RAW\t{totals[shard][1]}\n"
                f"LATEST_SHARD_CANDIDATES\t{candidate_count}\nDONE\n"
            ).encode("ascii"))

    state(status="ALL_SHARDS_NUMERICALLY_COMPLETE", shard=args.end,
          completed=args.end, candidates=None)
    note(f"CONTROLLER_COMPLETE\tEND\t{args.end}")
except Exception as exc:
    note(f"STOPPED\tERROR\t{type(exc).__name__}\t{exc}")
    state(status="STOPPED_REQUIRES_RECOVERY", error_type=type(exc).__name__, error=str(exc))
    raise
finally:
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass
