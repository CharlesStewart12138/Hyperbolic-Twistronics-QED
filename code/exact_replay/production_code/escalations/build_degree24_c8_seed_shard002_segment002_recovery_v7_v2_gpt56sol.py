#!/usr/bin/env python3
"""Build exact shard002 segment002 recovery artifacts from committed unit 12357."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
SOURCE_WRAPPER = B / "gap_run_degree24_c8_seed_shard002_segment001_unit1_14513_postverify_v7_gpt56sol.g"
SOURCE_OUTPUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt"
CHECKPOINT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt"
WRAPPER = B / "gap_run_degree24_c8_seed_shard002_segment002_unit12358_14513_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard002_segment002_postverify_v7.sh"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_UNIT12358_14513_POSTVERIFY_V7_GPT56SOL.txt"

CP_SHA = "f9bba393686f0035fc9e248a9741a9e51a7b79f64d94da2ba89e1cf9aec2d5a3"
PREFIX_BYTES = 9_401_850
PREFIX_SHA = "7e5750670227d6fba370de06f2d420a64ad59040e3104d4eae2ee6b34d231e22"
COUNTERS = [12_357, 37_960_704, 12_357, 574, 2_628_096, 1_557_392,
            430_464, 48_256, 0, 0, 0, 0]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert path.read_bytes() == data


cp_bytes = CHECKPOINT.read_bytes()
assert digest(cp_bytes) == CP_SHA
cp_lines = cp_bytes.decode("ascii").splitlines()
assert len(cp_lines) == 3
assert cp_lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002"
assert cp_lines[2] == "DONE"
fields = cp_lines[1].split("\t")
assert fields[0:2] == ["SHARD", "002"]
values = dict(zip(fields[2::2], fields[3::2], strict=True))
assert values["UNIT"] == "12357" and values["NEXT_UNIT"] == "12358"
assert values["KEY"] == "24T5940" and values["ALPHA"] == "18"
assert values["OUTPUT_PREFIX_BYTES"] == str(PREFIX_BYTES)
assert values["OUTPUT_PREFIX_SHA256"] == PREFIX_SHA
counter_names = (
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR",
    "CUM_B3", "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
)
assert [int(values[name]) for name in counter_names] == COUNTERS

previous = SOURCE_OUTPUT.read_bytes()
assert len(previous) == PREFIX_BYTES and digest(previous) == PREFIX_SHA
assert previous.endswith(
    b"CHECKPOINT_COMMITTED\tUNIT\t12357\tCHECKPOINT_SHA256\t"
    + CP_SHA.encode("ascii")
    + b"\tOUTPUT_PREFIX_BYTES\t9401850\tOUTPUT_PREFIX_SHA256\t"
    + PREFIX_SHA.encode("ascii") + b"\n"
)
assert b"\nCANDIDATE_NUMERIC\t" not in previous
assert b"\nTOTAL\t" not in previous and b"\nTOTAL_PARTIAL\t" not in previous

text = SOURCE_WRAPPER.read_text(encoding="ascii")
changes = {
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt";':
        f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;":
        "INTERNAL_GUARD_MS:=1320000; START_UNIT:=12358;",
    "INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];":
        "INITIAL_COUNTERS:=[" + ",".join(map(str, COUNTERS)) + "];",
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";':
        f'PREVIOUS_CHECKPOINT_SHA256:="{CP_SHA}";',
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;':
        f'PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/{SOURCE_OUTPUT.name}"; PREVIOUS_OUTPUT_PREFIX_BYTES:={PREFIX_BYTES};',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";':
        f'PREVIOUS_OUTPUT_PREFIX_SHA256:="{PREFIX_SHA}";',
}
for old, new in changes.items():
    assert text.count(old) == 1, old
    text = text.replace(old, new)
wrapper_bytes = text.encode("ascii")
runner_bytes = (
    "#!/usr/bin/env bash\nset -euo pipefail\nulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s "
    "/usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n"
).encode("ascii")
atomic_write(WRAPPER, wrapper_bytes)
atomic_write(RUNNER, runner_bytes)

print("PASS START_UNIT=12358 PREVIOUS_UNIT=12357 NO_REPLAY=1")
print(f"CHECKPOINT\t{CHECKPOINT.name}\tSHA256\t{digest(cp_bytes)}")
print(f"PREVIOUS_OUTPUT\t{SOURCE_OUTPUT.name}\tBYTES\t{len(previous)}\tSHA256\t{digest(previous)}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{digest(wrapper_bytes)}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{digest(runner_bytes)}")
