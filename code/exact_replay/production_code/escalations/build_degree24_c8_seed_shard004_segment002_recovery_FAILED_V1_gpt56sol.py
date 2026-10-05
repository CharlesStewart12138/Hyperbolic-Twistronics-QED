#!/usr/bin/env python3
"""Build exact shard004 recovery from durable unit 11896.

Segment001 reached ALPHA_DONE unit11897 but the external wall ended the
process before CHECKPOINT_COMMITTED.  Preserve that suffix as evidence and
restart at unit11897, so committed units are never replayed.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
SOURCE_WRAPPER = B / "gap_run_degree24_c8_seed_shard004_segment001_unit1_14031_postverify_v7_gpt56sol.g"
SOURCE_OUTPUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_UNIT1_14031_POSTVERIFY_V7_GPT56SOL.txt"
SOURCE_STDOUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt"
SOURCE_STDERR = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt"
CHECKPOINT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CHECKPOINT_GPT56SOL.txt"
PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_UNCOMMITTED_OUTPUT_SUFFIX_UNIT11897_GPT56SOL.txt"
EVIDENCE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_EXTERNAL_WALL_RECOVERY_EVIDENCE_GPT56SOL.txt"
WRAPPER = B / "gap_run_degree24_c8_seed_shard004_segment002_unit11897_14031_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard004_segment002_postverify_v7.sh"
PARSE = B / "gap_parse_smoke_degree24_c8_seed_shard004_segment002_v7_gpt56sol.g"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT002_UNIT11897_14031_POSTVERIFY_V7_GPT56SOL.txt"

CP_SHA = "bbe5270942524e5fe250e4a9a9656040c7d9a889b5d838074235ddb991fc0423"
PREFIX_BYTES = 9_065_618
PREFIX_SHA = "d8addbd6fe7afcc9507da0794e5761bfc44e40ab0aad46a71816bfb65e784898"
PHYSICAL_BYTES = 9_066_383
PHYSICAL_SHA = "4580fdd32dece25f022dbfb369b31cb0b84ff16d3fc6ae1d35dc939681604550"
COUNTERS = [11_896, 36_544_512, 11_896, 606, 3_091_144, 2_304_656,
            678_848, 108_608, 0, 0, 0, 0]


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
assert cp_lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD004"
assert cp_lines[2] == "DONE"
payload, payload_sha = cp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert digest(payload.encode("ascii")) == payload_sha
fields = payload.split("\t")
# The inherited engine's non-scientific SHARD value is 003; the certificate
# header, filenames, profile/plan hashes, and all numerical records are S004.
assert fields[0:2] == ["SHARD", "003"]
values = dict(zip(fields[2::2], fields[3::2], strict=True))
assert values["UNIT"] == "11896" and values["NEXT_UNIT"] == "11897"
assert values["KEY"] == "24T6728" and values["ALPHA"] == "43"
assert values["OUTPUT_PREFIX_BYTES"] == str(PREFIX_BYTES)
assert values["OUTPUT_PREFIX_SHA256"] == PREFIX_SHA
counter_names = (
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR",
    "CUM_B3", "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
)
assert [int(values[name]) for name in counter_names] == COUNTERS

physical = SOURCE_OUTPUT.read_bytes()
assert len(physical) == PHYSICAL_BYTES and digest(physical) == PHYSICAL_SHA
prefix = physical[:PREFIX_BYTES]
suffix = physical[PREFIX_BYTES:]
assert digest(prefix) == PREFIX_SHA
suffix_lines = suffix.decode("ascii").splitlines()
assert len(suffix_lines) == 1
assert suffix_lines[0].startswith("ALPHA_DONE\tUNIT\t11897\tKEY\t24T6728\tALPHA\t44\t")
assert "\tCUM_UNITS\t11897\t" in suffix_lines[0]
assert "\tNEXT_UNIT\t11898\t" in suffix_lines[0]
assert "\tPREVIOUS_CHECKPOINT_SHA256\t" + CP_SHA + "\t" in suffix_lines[0]
assert b"CHECKPOINT_COMMITTED\tUNIT\t11897\t" not in physical
assert b"ALPHA_DONE\tUNIT\t11898\t" not in physical
assert b"\nCANDIDATE_NUMERIC\t" not in physical
assert b"\nTOTAL\t" not in physical and b"\nTOTAL_PARTIAL\t" not in physical

stdout_bytes = SOURCE_STDOUT.read_bytes()
stderr_bytes = SOURCE_STDERR.read_bytes()
atomic_write(PRESERVED_SUFFIX, suffix)

evidence = (
    "CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD004-SEGMENT001-EXTERNAL-WALL\n"
    "STATUS\tRECOVERABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT\n"
    "END_STATE\tEXTERNAL_WALL_AFTER_UNCOMMITTED_ALPHA_DONE\n"
    "ORIGINAL_FILES_MODIFIED\t0\nSYNTHETIC_RECORDS_ADDED\t0\n"
    f"OUTPUT\t{SOURCE_OUTPUT.name}\tBYTES\t{len(physical)}\tSHA256\t{digest(physical).upper()}\n"
    f"STDOUT\t{SOURCE_STDOUT.name}\tBYTES\t{len(stdout_bytes)}\tSHA256\t{digest(stdout_bytes).upper()}\n"
    f"STDERR\t{SOURCE_STDERR.name}\tBYTES\t{len(stderr_bytes)}\tSHA256\t{digest(stderr_bytes).upper()}\n"
    "LAST_DURABLE_UNIT\t11896\nNEXT_UNIT\t11897\nLAST_DURABLE_KEY_ALPHA\t24T6728\t43\n"
    f"CHECKPOINT_SHA256\t{CP_SHA.upper()}\nOUTPUT_PREFIX_BYTES\t{PREFIX_BYTES}\nOUTPUT_PREFIX_SHA256\t{PREFIX_SHA.upper()}\n"
    f"UNCOMMITTED_SUFFIX\t{PRESERVED_SUFFIX.name}\tBYTES\t{len(suffix)}\tSHA256\t{digest(suffix).upper()}\tRECORD\tALPHA_DONE_UNIT11897_24T6728_ALPHA44\n"
    "EXCLUSION\tUncommitted ALPHA_DONE unit11897 is evidence only and excluded from scientific totals\n"
    "RECOVERY\tSTART_UNIT11897 recomputes 24T6728 alpha44; committed units1..11896 are not replayed\n"
    "RESOURCE_TELEMETRY\tEXTERNAL_WALL_PROCESS_ABSENT\n"
    "LABEL_NOTE\tCheckpoint SHARD=003 is an inherited non-scientific label defect; certificate header and all S004 identities are correct\n"
    "DONE\n"
).encode("ascii")
atomic_write(EVIDENCE, evidence)

text = SOURCE_WRAPPER.read_text(encoding="ascii")
changes = {
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_UNIT1_14031_POSTVERIFY_V7_GPT56SOL.txt";':
        f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;":
        "INTERNAL_GUARD_MS:=1320000; START_UNIT:=11897;",
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
parse_bytes = (
    f'f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/{WRAPPER.name}");\n'
    'if f=fail then Error("S004 segment002 wrapper parse failed"); fi;\n'
    'g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard004_v7_v2_gpt56sol.g");\n'
    'if g=fail then Error("S004 segment002 engine parse failed"); fi;\n'
    'Print("SHARD004_SEGMENT002_V7_WRAPPER_ENGINE_PARSE_PASS\\n");\nQUIT_GAP(0);\n'
).encode("ascii")
atomic_write(WRAPPER, wrapper_bytes)
atomic_write(RUNNER, runner_bytes)
atomic_write(PARSE, parse_bytes)

print("PASS START_UNIT=11897 PREVIOUS_UNIT=11896 NO_REPLAY=1 RECOMPUTE_UNCOMMITTED=1")
print(f"CHECKPOINT\t{CHECKPOINT.name}\tSHA256\t{digest(cp_bytes).upper()}")
print(f"PREVIOUS_OUTPUT\t{SOURCE_OUTPUT.name}\tPHYSICAL_BYTES\t{len(physical)}\tPHYSICAL_SHA256\t{digest(physical).upper()}\tPREFIX_BYTES\t{PREFIX_BYTES}\tPREFIX_SHA256\t{digest(prefix).upper()}")
print(f"EXCLUDED_SUFFIX\t{PRESERVED_SUFFIX.name}\tBYTES\t{len(suffix)}\tSHA256\t{digest(suffix).upper()}")
print(f"EVIDENCE\t{EVIDENCE.name}\tSHA256\t{digest(evidence).upper()}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{digest(wrapper_bytes).upper()}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{digest(runner_bytes).upper()}")
print(f"PARSE\t{PARSE.name}\tSHA256\t{digest(parse_bytes).upper()}")
