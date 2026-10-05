#!/usr/bin/env python3
"""Build the exact no-replay V7 recovery wrapper for seed shard002 segment002."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


BASE = Path(__file__).resolve().parent
SOURCE_WRAPPER = BASE / "gap_run_degree24_c8_seed_shard002_segment001_unit1_14513_postverify_v7_gpt56sol.g"
SOURCE_OUTPUT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt"
CHECKPOINT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt"
WRAPPER = BASE / "gap_run_degree24_c8_seed_shard002_segment002_unit12358_14513_postverify_v7_gpt56sol.g"
RUNNER = BASE / "run_degree24_c8_seed_shard002_segment002_postverify_v7.sh"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_UNIT12358_14513_POSTVERIFY_V7_GPT56SOL.txt"

EXPECTED_CHECKPOINT_SHA256 = "f9bba393686f0035fc9e248a9741a9e51a7b79f64d94da2ba89e1cf9aec2d5a3"
EXPECTED_PREFIX_BYTES = 9_401_850
EXPECTED_PREFIX_SHA256 = "7e5750670227d6fba370de06f2d420a64ad59040e3104d4eae2ee6b34d231e22"
INITIAL_COUNTERS = [
    12_357,
    37_960_704,
    12_357,
    574,
    2_628_096,
    1_557_392,
    430_464,
    48_256,
    0,
    0,
    0,
    0,
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    if path.read_bytes() != data:
        raise RuntimeError(f"post-write byte mismatch: {path}")


checkpoint_bytes = CHECKPOINT.read_bytes()
assert sha256(checkpoint_bytes) == EXPECTED_CHECKPOINT_SHA256
checkpoint_lines = checkpoint_bytes.decode("ascii").splitlines()
assert len(checkpoint_lines) == 2 and checkpoint_lines[1] == "DONE"
fields = checkpoint_lines[0].split("\t")
assert fields[0:2] == ["CERTIFICATE_CHECKPOINT", "PF-GRP-001-C8-DEGREE24-SEED-SHARD002"]
values = dict(zip(fields[2::2], fields[3::2], strict=True))
assert values["UNIT"] == "12357" and values["NEXT_UNIT"] == "12358"
assert values["KEY"] == "24T5940" and values["ALPHA"] == "18"
assert values["OUTPUT_PREFIX_BYTES"] == str(EXPECTED_PREFIX_BYTES)
assert values["OUTPUT_PREFIX_SHA256"] == EXPECTED_PREFIX_SHA256
assert [int(values[name]) for name in (
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR",
    "CUM_B3", "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
)] == INITIAL_COUNTERS

source_output = SOURCE_OUTPUT.read_bytes()
assert len(source_output) == EXPECTED_PREFIX_BYTES
assert sha256(source_output) == EXPECTED_PREFIX_SHA256
assert source_output.endswith((
    b"CHECKPOINT_COMMITTED\tUNIT\t12357\tCHECKPOINT_SHA256\t"
    + EXPECTED_CHECKPOINT_SHA256.encode("ascii")
    + b"\tOUTPUT_PREFIX_BYTES\t9401850\tOUTPUT_PREFIX_SHA256\t"
    + EXPECTED_PREFIX_SHA256.encode("ascii")
    + b"\n"
))
assert b"\nCANDIDATE_NUMERIC\t" not in source_output
assert b"\nTOTAL\t" not in source_output and b"\nTOTAL_PARTIAL\t" not in source_output

text = SOURCE_WRAPPER.read_text(encoding="ascii")
replacements = {
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt";':
        f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;":
        "INTERNAL_GUARD_MS:=1320000; START_UNIT:=12358;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];":
        "INITIAL_COUNTERS:=[" + ",".join(map(str, INITIAL_COUNTERS)) + "];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";':
        f'PREVIOUS_CHECKPOINT_SHA256:="{EXPECTED_CHECKPOINT_SHA256}";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;':
        'PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/'
        + SOURCE_OUTPUT.name + f'"; PREVIOUS_OUTPUT_PREFIX_BYTES:={EXPECTED_PREFIX_BYTES};',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";':
        f'PREVIOUS_OUTPUT_PREFIX_SHA256:="{EXPECTED_PREFIX_SHA256}";',
}
for old, new in replacements.items():
    assert text.count(old) == 1, old
    text = text.replace(old, new)
wrapper_bytes = text.encode("ascii")

runner_text = (
    "#!/usr/bin/env bash\n"
    "set -euo pipefail\n"
    "ulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s "
    "/usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n"
)
atomic_write(WRAPPER, wrapper_bytes)
atomic_write(RUNNER, runner_text.encode("ascii"))

print("PASS START_UNIT=12358 PREVIOUS_UNIT=12357 NO_REPLAY=1")
print(f"CHECKPOINT\t{CHECKPOINT.name}\tSHA256\t{sha256(checkpoint_bytes)}")
print(f"PREVIOUS_OUTPUT\t{SOURCE_OUTPUT.name}\tBYTES\t{len(source_output)}\tSHA256\t{sha256(source_output)}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{sha256(wrapper_bytes)}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{sha256(runner_text.encode('ascii'))}")
