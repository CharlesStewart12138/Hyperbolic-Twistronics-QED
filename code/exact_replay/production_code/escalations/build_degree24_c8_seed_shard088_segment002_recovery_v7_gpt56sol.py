#!/usr/bin/env python3
"""Build an exact no-replay recovery segment for shard088.

Segment001 committed unit 2167 atomically, then GAP could not reopen the
output file to append the matching CHECKPOINT_COMMITTED record.  The physical
output is exactly the checkpoint-sealed prefix, so resume at unit 2168.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
SOURCE_WRAPPER = B / "gap_run_degree24_c8_seed_shard088_segment001_unit1_3662_postverify_v7_gpt56sol.g"
SOURCE_OUTPUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt"
SOURCE_STDOUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt"
SOURCE_STDERR = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt"
CHECKPOINT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_CHECKPOINT_GPT56SOL.txt"
CHECKPOINT_TMP = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_CHECKPOINT_TMP_GPT56SOL.txt"
EVIDENCE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_APPEND_OPEN_RECOVERY_EVIDENCE_GPT56SOL.txt"
WRAPPER = B / "gap_run_degree24_c8_seed_shard088_segment002_unit2168_3662_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard088_segment002_postverify_v7.sh"
PARSE = B / "gap_parse_smoke_degree24_c8_seed_shard088_segment002_v7_gpt56sol.g"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT002_UNIT2168_3662_POSTVERIFY_V7_GPT56SOL.txt"

CP_SHA = "55d9349a83e248ce47822ef26e86a243d6ea774f1430569c0d0d6b576fbb74aa"
PREFIX_BYTES = 1_609_443
PREFIX_SHA = "f77f63818b7e403c7b710f8212cde10053fa82dd3f15b25e178c7d291f83e7c7"
COUNTERS = [2167, 26628096, 2167, 12, 1804384, 1735040,
            0, 0, 0, 0, 0, 0]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    if temp.exists():
        raise RuntimeError(f"stale temp: {temp}")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists() and path.read_bytes() == data


cp_bytes = CHECKPOINT.read_bytes()
assert digest(cp_bytes) == CP_SHA
cp_lines = cp_bytes.decode("ascii").splitlines()
assert len(cp_lines) == 3
assert cp_lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD088"
assert cp_lines[2] == "DONE"
payload, payload_sha = cp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert digest(payload.encode("ascii")) == payload_sha
fields = payload.split("\t")
assert fields[0:2] == ["SHARD", "088"]
values = dict(zip(fields[2::2], fields[3::2], strict=True))
assert values["UNIT"] == "2167" and values["NEXT_UNIT"] == "2168"
assert values["KEY"] == "24T11606" and values["ALPHA"] == "714"
assert values["OUTPUT_PREFIX_BYTES"] == str(PREFIX_BYTES)
assert values["OUTPUT_PREFIX_SHA256"] == PREFIX_SHA
counter_names = (
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR",
    "CUM_B3", "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
)
assert [int(values[name]) for name in counter_names] == COUNTERS

physical = SOURCE_OUTPUT.read_bytes()
assert len(physical) == PREFIX_BYTES and digest(physical) == PREFIX_SHA
assert physical.endswith(b"\n")
assert b"CHECKPOINT_COMMITTED\tUNIT\t2167\t" not in physical
assert b"ALPHA_DONE\tUNIT\t2168\t" not in physical
assert b"\nCANDIDATE_NUMERIC\t" not in physical
assert b"\nTOTAL\t" not in physical and b"\nTOTAL_PARTIAL\t" not in physical
assert not CHECKPOINT_TMP.exists()

stdout_bytes = SOURCE_STDOUT.read_bytes()
stderr_bytes = SOURCE_STDERR.read_bytes()
evidence = (
    "CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD088-SEGMENT001-APPEND-OPEN\n"
    "STATUS\tRECOVERABLE_COMMITTED_PREFIX_NOT_TERMINAL_SHARD_RESULT\n"
    "END_STATE\tCHECKPOINT_ATOMICALLY_COMMITTED_BEFORE_OUTPUT_COMMIT_RECORD_APPEND\n"
    "ORIGINAL_FILES_MODIFIED\t0\nSYNTHETIC_RECORDS_ADDED\t0\n"
    f"OUTPUT\t{SOURCE_OUTPUT.name}\tBYTES\t{len(physical)}\tSHA256\t{digest(physical).upper()}\n"
    f"STDOUT\t{SOURCE_STDOUT.name}\tBYTES\t{len(stdout_bytes)}\tSHA256\t{digest(stdout_bytes).upper()}\n"
    f"STDERR\t{SOURCE_STDERR.name}\tBYTES\t{len(stderr_bytes)}\tSHA256\t{digest(stderr_bytes).upper()}\n"
    "LAST_DURABLE_UNIT\t2167\nNEXT_UNIT\t2168\nLAST_DURABLE_KEY_ALPHA\t24T11606\t714\n"
    f"CHECKPOINT_SHA256\t{CP_SHA.upper()}\nOUTPUT_PREFIX_BYTES\t{PREFIX_BYTES}\nOUTPUT_PREFIX_SHA256\t{PREFIX_SHA.upper()}\n"
    "PHYSICAL_OUTPUT_EQUALS_SEALED_PREFIX\t1\nUNCOMMITTED_SUFFIX_BYTES\t0\n"
    "RECOVERY\tSTART_UNIT2168; committed units1..2167 are not replayed\n"
    "RESOURCE_TELEMETRY\tFAILED_PROCESS_ABSENT\nDONE\n"
).encode("ascii")
atomic_write(EVIDENCE, evidence)

text = SOURCE_WRAPPER.read_text(encoding="ascii")
changes = {
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";':
        f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;":
        "INTERNAL_GUARD_MS:=1320000; START_UNIT:=2168;",
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
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}\n"
).encode("ascii")
parse_bytes = (
    f'f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}");\n'
    'if f=fail then Error("S088 segment002 wrapper parse failed"); fi;\n'
    'g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard088_v7_gpt56sol.g");\n'
    'if g=fail then Error("S088 segment002 engine parse failed"); fi;\n'
    'Print("SHARD088_SEGMENT002_V7_WRAPPER_ENGINE_PARSE_PASS\\n");\nQUIT_GAP(0);\n'
).encode("ascii")
atomic_write(WRAPPER, wrapper_bytes)
atomic_write(RUNNER, runner_bytes)
atomic_write(PARSE, parse_bytes)

print("PASS START_UNIT=2168 PREVIOUS_UNIT=2167 NO_REPLAY=1 UNCOMMITTED_SUFFIX_BYTES=0")
print(f"CHECKPOINT\t{CHECKPOINT.name}\tSHA256\t{digest(cp_bytes).upper()}")
print(f"PREVIOUS_OUTPUT\t{SOURCE_OUTPUT.name}\tBYTES\t{len(physical)}\tSHA256\t{digest(physical).upper()}")
print(f"EVIDENCE\t{EVIDENCE.name}\tSHA256\t{digest(evidence).upper()}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{digest(wrapper_bytes).upper()}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{digest(runner_bytes).upper()}")
print(f"PARSE\t{PARSE.name}\tSHA256\t{digest(parse_bytes).upper()}")
