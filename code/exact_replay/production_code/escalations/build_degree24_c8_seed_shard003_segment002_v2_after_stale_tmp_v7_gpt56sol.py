#!/usr/bin/env python3
"""Preserve the stale-TMP pre-execution failure and build a unique V2 launch."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
LIVE_TMP = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_TMP_GPT56SOL.txt"
PRESERVED_TMP = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNCOMMITTED_CHECKPOINT_TMP_UNIT8090_GPT56SOL.txt"
V1_STDOUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_RUN_STDOUT_V7_GPT56SOL.txt"
V1_STDERR = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_RUN_STDERR_V7_GPT56SOL.txt"
FAILED_STDOUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_RUN_STDOUT_FAILED_PREEXEC_V1_GPT56SOL.txt"
FAILED_STDERR = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_RUN_STDERR_FAILED_PREEXEC_V1_GPT56SOL.txt"
V1_WRAPPER = B / "gap_run_degree24_c8_seed_shard003_segment002_unit8090_14648_postverify_v7_gpt56sol.g"
V2_WRAPPER = B / "gap_run_degree24_c8_seed_shard003_segment002_v2_unit8090_14648_postverify_v7_gpt56sol.g"
V2_RUNNER = B / "run_degree24_c8_seed_shard003_segment002_v2_postverify_v7.sh"
V1_OUTPUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_UNIT8090_14648_POSTVERIFY_V7_GPT56SOL.txt"
V2_OUTPUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_V2_UNIT8090_14648_POSTVERIFY_V7_GPT56SOL.txt"
EVIDENCE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_FAILED_PREEXEC_STALE_TMP_EVIDENCE_GPT56SOL.txt"
TMP_SHA = "1a4655a876aadd4ca6ed21fc7e2f4219a306fd57a0e0cc7ad616e7326acde0f8"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists() and path.read_bytes() == data


live = LIVE_TMP.read_bytes()
preserved = PRESERVED_TMP.read_bytes()
assert digest(live) == TMP_SHA and live == preserved
stdout = V1_STDOUT.read_bytes()
stderr = V1_STDERR.read_bytes()
assert b"Error, stale checkpoint temp" in stderr
assert not (B / V1_OUTPUT).exists()
atomic_write(FAILED_STDOUT, stdout)
atomic_write(FAILED_STDERR, stderr)

v1_wrapper = V1_WRAPPER.read_text(encoding="ascii")
old = f'OUT:="/mnt/d/work/revise/production_code/escalations/{V1_OUTPUT}";'
new = f'OUT:="/mnt/d/work/revise/production_code/escalations/{V2_OUTPUT}";'
assert v1_wrapper.count(old) == 1
v2_wrapper = v1_wrapper.replace(old, new).encode("ascii")
v2_runner = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s "
    "/usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{V2_WRAPPER.name}\n"
).encode("ascii")
atomic_write(V2_WRAPPER, v2_wrapper)
atomic_write(V2_RUNNER, v2_runner)

evidence = (
    "CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003-SEGMENT002-PREEXEC-V1\n"
    "STATUS\tFAILED_PREEXEC_SUPERSEDED_EXCLUDED\n"
    "FAILURE\tEngine correctly rejected stale canonical checkpoint TMP preserved from segment001 failure\n"
    "SCIENTIFIC_UNITS_EXECUTED\t0\nOUTPUT_FILE_CREATED\t0\nCHECKPOINT_MODIFIED\t0\n"
    f"STDOUT\t{FAILED_STDOUT.name}\tBYTES\t{len(stdout)}\tSHA256\t{digest(stdout).upper()}\n"
    f"STDERR\t{FAILED_STDERR.name}\tBYTES\t{len(stderr)}\tSHA256\t{digest(stderr).upper()}\n"
    f"STALE_TMP_PRESERVED_AS\t{PRESERVED_TMP.name}\tBYTES\t{len(preserved)}\tSHA256\t{digest(preserved).upper()}\n"
    "REMEDIATION\tAfter exact-byte preservation, remove only live TMP pathname and relaunch unique V2 from unchanged START_UNIT8090\n"
    "DONE\n"
).encode("ascii")
atomic_write(EVIDENCE, evidence)

# Delete only the stale live temporary pathname after its exact-byte copy and
# evidence have been durably written.  The durable checkpoint is untouched.
assert LIVE_TMP.resolve().parent == B.resolve()
LIVE_TMP.unlink()
assert not LIVE_TMP.exists() and PRESERVED_TMP.read_bytes() == preserved

print("PASS FAILED_PREEXEC_PRESERVED=1 LIVE_STALE_TMP_REMOVED=1 CHECKPOINT_UNTOUCHED=1")
print(f"EVIDENCE\t{EVIDENCE.name}\tSHA256\t{digest(evidence).upper()}")
print(f"FAILED_STDOUT\t{FAILED_STDOUT.name}\tSHA256\t{digest(stdout).upper()}")
print(f"FAILED_STDERR\t{FAILED_STDERR.name}\tSHA256\t{digest(stderr).upper()}")
print(f"V2_WRAPPER\t{V2_WRAPPER.name}\tSHA256\t{digest(v2_wrapper).upper()}")
print(f"V2_RUNNER\t{V2_RUNNER.name}\tSHA256\t{digest(v2_runner).upper()}")
