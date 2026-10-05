#!/usr/bin/env python3
"""Finish the latest recovery segment, minimally close it, then resume shards."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


B = Path(__file__).resolve().parent
STATUS = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_CONTROLLER_STATUS_GPT5.json"
LOG = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_CONTROLLER_GPT5.log"
LOCK = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_RECOVERY_CONTROLLER_GPT5.lock"
MAIN_LOCK = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_CONTROLLER_GPT5.lock"
FINALIZER = B / "finalize_degree24_c8_seed_shard_minimal_generic_gpt56sol.py"
CONTROLLER = B / "run_degree24_c8_seed_compute_first_controller_v2_gpt5.py"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write(path: Path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    if tmp.exists():
        raise RuntimeError(f"stale temp: {tmp}")
    with tmp.open("wb") as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    os.replace(tmp, path)


def state(**values: object) -> None:
    atomic_write(STATUS, (json.dumps({"updated_utc": stamp(), **values}, sort_keys=True) + "\n").encode("ascii"))


def note(message: str) -> None:
    with LOG.open("a", encoding="ascii", newline="") as stream:
        stream.write(f"{stamp()}\t{message}\n"); stream.flush(); os.fsync(stream.fileno())


def run_to_files(command: list[str], stdout_path: Path, stderr_path: Path) -> int:
    if stdout_path.exists() or stderr_path.exists():
        raise RuntimeError(f"no-clobber logs: {stdout_path.name}")
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        process = subprocess.run(command, stdout=stdout, stderr=stderr, check=False)
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    return process.returncode


parser = argparse.ArgumentParser()
parser.add_argument("--shard", type=int, required=True)
parser.add_argument("--end", type=int, default=905)
args = parser.parse_args()
assert 6 <= args.shard < args.end <= 905
tag = f"{args.shard:03d}"

assert not MAIN_LOCK.exists(), "main controller still owns lock"
fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    os.write(fd, f"PID\t{os.getpid()}\nSHARD\t{tag}\n".encode("ascii")); os.fsync(fd)
finally:
    os.close(fd)

try:
    marker = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_COMPLETE_GPT56SOL.txt"
    assert not marker.exists()
    runners: list[tuple[int, Path]] = []
    for path in B.glob(f"run_degree24_c8_seed_shard{tag}_segment*_postverify_v7.sh"):
        match = re.search(r"_segment([0-9]+)_", path.name)
        assert match
        runners.append((int(match.group(1)), path))
    assert runners
    runners.sort()
    segment, runner = runners[-1]
    assert segment >= 2
    segment_label = f"{segment:03d}"
    run_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT{segment_label}_RUN_STDOUT_V7_GPT5.txt"
    run_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT{segment_label}_RUN_STDERR_V7_GPT5.txt"
    note(f"RECOVERY_RUN_START\tSHARD\t{tag}\tSEGMENT\t{segment_label}\tPID\t{os.getpid()}")
    state(status="RUNNING_RECOVERY", shard=args.shard, completed=args.shard - 1,
          segment=segment, candidates=0)
    started = time.monotonic()
    wsl_runner = "/mnt/d/work/revise/production_code/escalations/" + runner.name
    rc = run_to_files(["wsl.exe", "bash", wsl_runner], run_out, run_err)
    wall = round(time.monotonic() - started, 3)
    if rc != 0:
        raise RuntimeError(f"recovery GAP exit {rc} shard{tag} segment{segment_label} after {wall}s")

    final_out = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_RECOVERY_MINIMAL_FINALIZE_STDOUT_GPT5.txt"
    final_err = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_RECOVERY_MINIMAL_FINALIZE_STDERR_GPT5.txt"
    state(status="FINALIZING_RECOVERY", shard=args.shard, completed=args.shard - 1,
          segment=segment, candidates=0, wall_seconds=wall)
    rc = run_to_files([sys.executable, str(FINALIZER), "--shard", str(args.shard)], final_out, final_err)
    if rc != 0 or not marker.exists():
        raise RuntimeError(f"recovery finalizer failed shard{tag}, exit {rc}")
    final_text = final_out.read_text(encoding="ascii")
    candidates = int(final_text.split("CANDIDATES=", 1)[1].split()[0])
    note(f"RECOVERY_COMPLETE\tSHARD\t{tag}\tSEGMENT\t{segment_label}\tCANDIDATES\t{candidates}\tWALL_SECONDS\t{wall}")
    state(status="RECOVERY_COMPLETE_LAUNCHING_NEXT", shard=args.shard,
          completed=args.shard, segment=segment, candidates=candidates, wall_seconds=wall)
except Exception as exc:
    note(f"RECOVERY_STOPPED\tSHARD\t{tag}\tERROR\t{type(exc).__name__}\t{exc}")
    state(status="STOPPED_REQUIRES_RECOVERY", shard=args.shard,
          completed=args.shard - 1, error_type=type(exc).__name__, error=str(exc))
    raise
finally:
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass

next_shard = args.shard + 1
note(f"CONTROLLER_RELAUNCH\tSTART\t{next_shard}\tEND\t{args.end}")
os.execv(sys.executable, [sys.executable, str(CONTROLLER), "--start", str(next_shard), "--end", str(args.end)])
