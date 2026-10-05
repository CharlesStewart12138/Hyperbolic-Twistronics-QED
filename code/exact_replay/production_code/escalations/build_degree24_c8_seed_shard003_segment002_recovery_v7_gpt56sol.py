#!/usr/bin/env python3
"""Build shard003 recovery segment002 from the last durable unit 8089.

The physical segment001 output contains one additional ALPHA_DONE record for
unit 8090, but its checkpoint PrintTo failed.  That suffix is preserved as
evidence and excluded; recovery therefore restarts at unit 8090.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
SOURCE_WRAPPER = B / "gap_run_degree24_c8_seed_shard003_segment001_unit1_14648_postverify_v7_gpt56sol.g"
SOURCE_OUTPUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNIT1_14648_POSTVERIFY_V7_GPT56SOL.txt"
SOURCE_STDOUT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt"
SOURCE_STDERR = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt"
CHECKPOINT = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_GPT56SOL.txt"
FAILED_TMP = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_TMP_GPT56SOL.txt"
PRESERVED_TMP = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNCOMMITTED_CHECKPOINT_TMP_UNIT8090_GPT56SOL.txt"
PRESERVED_SUFFIX = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNCOMMITTED_OUTPUT_SUFFIX_UNIT8090_GPT56SOL.txt"
EVIDENCE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_CHECKPOINT_WRITE_FAILURE_EVIDENCE_GPT56SOL.txt"
WRAPPER = B / "gap_run_degree24_c8_seed_shard003_segment002_unit8090_14648_postverify_v7_gpt56sol.g"
RUNNER = B / "run_degree24_c8_seed_shard003_segment002_postverify_v7.sh"
OUTPUT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_UNIT8090_14648_POSTVERIFY_V7_GPT56SOL.txt"

CP_SHA = "261556ab596d01304c742d7ea5b55dc7cbbd524b68bcb9daf03ec59d545e2360"
PREFIX_BYTES = 6_148_317
PREFIX_SHA = "77a95f05b20d2daf91a477a36caaf520c4b6dd042e91d5f17642b9b0fa382773"
PHYSICAL_BYTES = 6_149_074
PHYSICAL_SHA = "6057f218a149b1da02ad61befd315a8fb3575993f6b535010d927258f357dc16"
TMP_SHA = "1a4655a876aadd4ca6ed21fc7e2f4219a306fd57a0e0cc7ad616e7326acde0f8"
STDOUT_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
STDERR_SHA = "7c961574c49d09b36471bcbb079ccbee72bced0cc2cfcbec3c1760fc9ddf9099"
COUNTERS = [8_089, 24_849_408, 8_089, 411, 2_138_368, 1_370_312,
            290_816, 37_504, 0, 0, 0, 0]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists()
    assert path.read_bytes() == data


cp_bytes = CHECKPOINT.read_bytes()
assert digest(cp_bytes) == CP_SHA
cp_lines = cp_bytes.decode("ascii").splitlines()
assert len(cp_lines) == 3
assert cp_lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD003"
assert cp_lines[2] == "DONE"
fields = cp_lines[1].split("\t")
assert fields[0:2] == ["SHARD", "003"]
values = dict(zip(fields[2::2], fields[3::2], strict=True))
assert values["UNIT"] == "8089" and values["NEXT_UNIT"] == "8090"
assert values["KEY"] == "24T6257" and values["ALPHA"] == "15"
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
assert suffix_lines[0].startswith("ALPHA_DONE\tUNIT\t8090\tKEY\t24T6257\tALPHA\t16\t")
assert "\tCUM_UNITS\t8090\t" in suffix_lines[0]
assert "\tNEXT_UNIT\t8091\t" in suffix_lines[0]
assert "\tPREVIOUS_CHECKPOINT_SHA256\t" + CP_SHA + "\t" in suffix_lines[0]
assert b"CHECKPOINT_COMMITTED\tUNIT\t8090\t" not in physical
assert b"ALPHA_DONE\tUNIT\t8091\t" not in physical
assert b"\nCANDIDATE_NUMERIC\t" not in physical
assert b"\nTOTAL\t" not in physical and b"\nTOTAL_PARTIAL\t" not in physical

tmp_bytes = FAILED_TMP.read_bytes()
assert digest(tmp_bytes) == TMP_SHA
assert b"\tUNIT\t8090\tKEY\t24T6257\tALPHA\t16\tNEXT_UNIT\t8091\t" in tmp_bytes
assert not tmp_bytes.endswith(b"DONE\n")
stdout_bytes = SOURCE_STDOUT.read_bytes()
stderr_bytes = SOURCE_STDERR.read_bytes()
assert digest(stdout_bytes) == STDOUT_SHA and digest(stderr_bytes) == STDERR_SHA
assert b"Could not write to file descriptor" in stderr_bytes
atomic_write(PRESERVED_TMP, tmp_bytes)
atomic_write(PRESERVED_SUFFIX, suffix)

evidence = (
    "CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003-SEGMENT001-CHECKPOINT-WRITE-FAILURE\n"
    "STATUS\tRECOVERABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT\n"
    "END_STATE\tCHECKPOINT_PRINTTO_FAILURE_AFTER_UNCOMMITTED_ALPHA_DONE\n"
    "ORIGINAL_FILES_MODIFIED\t0\nSYNTHETIC_RECORDS_ADDED\t0\n"
    f"OUTPUT\t{SOURCE_OUTPUT.name}\tBYTES\t{len(physical)}\tSHA256\t{digest(physical).upper()}\n"
    f"STDOUT\t{SOURCE_STDOUT.name}\tBYTES\t{len(stdout_bytes)}\tSHA256\t{digest(stdout_bytes).upper()}\n"
    f"STDERR\t{SOURCE_STDERR.name}\tBYTES\t{len(stderr_bytes)}\tSHA256\t{digest(stderr_bytes).upper()}\n"
    "LAST_DURABLE_UNIT\t8089\nNEXT_UNIT\t8090\nLAST_DURABLE_KEY_ALPHA\t24T6257\t15\n"
    f"CHECKPOINT_SHA256\t{CP_SHA.upper()}\nOUTPUT_PREFIX_BYTES\t{PREFIX_BYTES}\nOUTPUT_PREFIX_SHA256\t{PREFIX_SHA.upper()}\n"
    f"UNCOMMITTED_SUFFIX\t{PRESERVED_SUFFIX.name}\tBYTES\t{len(suffix)}\tSHA256\t{digest(suffix).upper()}\tRECORD\tALPHA_DONE_UNIT8090_24T6257_ALPHA16\n"
    f"FAILED_TMP\t{PRESERVED_TMP.name}\tBYTES\t{len(tmp_bytes)}\tSHA256\t{digest(tmp_bytes).upper()}\tPAYLOAD_UNIT\t8090\tTERMINAL_DONE\t0\n"
    "FAILURE\tCould not write to file descriptor during checkpoint PrintTo\n"
    "EXCLUSION\tUncommitted ALPHA_DONE unit8090 and failed TMP payload are evidence only and excluded from scientific totals\n"
    "RECOVERY\tSTART_UNIT8090 recomputes 24T6257 alpha16; committed units1..8089 are not replayed\n"
    "RESOURCE_TELEMETRY\tUNAVAILABLE_PROCESS_FAILURE\nDONE\n"
).encode("ascii")
atomic_write(EVIDENCE, evidence)

text = SOURCE_WRAPPER.read_text(encoding="ascii")
changes = {
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNIT1_14648_POSTVERIFY_V7_GPT56SOL.txt";':
        f'OUT:="/mnt/d/work/revise/production_code/escalations/{OUTPUT_NAME}";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;":
        "INTERNAL_GUARD_MS:=1320000; START_UNIT:=8090;",
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

print("PASS START_UNIT=8090 PREVIOUS_UNIT=8089 NO_REPLAY=1 RECOMPUTE_UNCOMMITTED=1")
print(f"CHECKPOINT\t{CHECKPOINT.name}\tSHA256\t{digest(cp_bytes).upper()}")
print(f"PREVIOUS_OUTPUT\t{SOURCE_OUTPUT.name}\tPHYSICAL_BYTES\t{len(physical)}\tPHYSICAL_SHA256\t{digest(physical).upper()}\tPREFIX_BYTES\t{PREFIX_BYTES}\tPREFIX_SHA256\t{digest(prefix).upper()}")
print(f"EXCLUDED_SUFFIX\t{PRESERVED_SUFFIX.name}\tBYTES\t{len(suffix)}\tSHA256\t{digest(suffix).upper()}")
print(f"PRESERVED_TMP\t{PRESERVED_TMP.name}\tBYTES\t{len(tmp_bytes)}\tSHA256\t{digest(tmp_bytes).upper()}")
print(f"EVIDENCE\t{EVIDENCE.name}\tSHA256\t{digest(evidence).upper()}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{digest(wrapper_bytes).upper()}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{digest(runner_bytes).upper()}")
