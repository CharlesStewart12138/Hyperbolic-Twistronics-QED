from __future__ import annotations

import hashlib
import os
from pathlib import Path


BASE = Path(__file__).resolve().parent
CHECKPOINT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_GPT56SOL.txt"
CHECKPOINT_TMP = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_TMP_GPT56SOL.txt"
FAILED_TMP = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_CHECKPOINT_TMP_FAILED_AT_UNIT8115_GPT56SOL.txt"
PREVIOUS_WRAPPER = BASE / "gap_run_degree24_c8_seed_shard001_segment002_unit2_14622_v5_gpt56sol.g"
PREVIOUS_OUTPUT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_UNIT2_14622_V5_GPT56SOL.txt"
PREVIOUS_STDERR = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_RUN_STDERR_V5_GPT56SOL.txt"
WRAPPER = BASE / "gap_run_degree24_c8_seed_shard001_segment003_unit8115_14622_retry_v6_gpt56sol.g"
OUTPUT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_UNIT8115_14622_RETRY_V6_GPT56SOL.txt"
RUNNER = BASE / "run_degree24_c8_seed_shard001_segment003_retry_v6.sh"
FAILURE_NOTE = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_FAILED_ATOMIC_RENAME_EVIDENCE_GPT56SOL.txt"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fields(line: str) -> dict[str, str]:
    parts = line.rstrip("\r\n").split("\t")
    if len(parts) % 2:
        raise AssertionError("odd checkpoint field count")
    return dict(zip(parts[0::2], parts[1::2]))


for path in (CHECKPOINT, CHECKPOINT_TMP, PREVIOUS_WRAPPER, PREVIOUS_OUTPUT, PREVIOUS_STDERR):
    assert path.is_file(), path
for path in (FAILED_TMP, WRAPPER, OUTPUT, RUNNER, FAILURE_NOTE):
    assert not path.exists(), f"no-clobber: {path}"

cp_bytes = CHECKPOINT.read_bytes()
cp_lines = cp_bytes.decode("ascii").splitlines()
assert cp_lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001"
assert cp_lines[-1] == "DONE" and len(cp_lines) == 3
record = fields(cp_lines[1])
assert record["SHARD"] == "001"
assert record["UNIT"] == "8114" and record["NEXT_UNIT"] == "8115"
assert record["KEY"] == "24T5512" and record["ALPHA"] == "24"
payload, payload_hash = cp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert sha(payload.encode("ascii")) == payload_hash
cp_hash = sha(cp_bytes)

previous_bytes = PREVIOUS_OUTPUT.read_bytes()
prefix_bytes = int(record["OUTPUT_PREFIX_BYTES"])
assert len(previous_bytes) > prefix_bytes
assert sha(previous_bytes[:prefix_bytes]) == record["OUTPUT_PREFIX_SHA256"]
tail = previous_bytes[prefix_bytes:].decode("ascii")
assert "ALPHA_DONE\tUNIT\t8115\tKEY\t24T5513\tALPHA\t1\t" in tail
assert "CHECKPOINT_COMMITTED\tUNIT\t8115\t" not in tail
assert "CANDIDATE_NUMERIC\t" not in tail

tmp_bytes = CHECKPOINT_TMP.read_bytes()
tmp_lines = tmp_bytes.decode("ascii").splitlines()
assert tmp_lines[0] == cp_lines[0] and tmp_lines[-1] == "DONE" and len(tmp_lines) == 3
tmp_record = fields(tmp_lines[1])
assert tmp_record["UNIT"] == "8115" and tmp_record["NEXT_UNIT"] == "8116"
tmp_payload, tmp_payload_hash = tmp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert sha(tmp_payload.encode("ascii")) == tmp_payload_hash
assert tmp_record["PREVIOUS_CHECKPOINT_SHA256"] == cp_hash
assert tmp_record["CUM_CANDIDATE_NUMERIC"] == "0"
tmp_hash = sha(tmp_bytes)
os.replace(CHECKPOINT_TMP, FAILED_TMP)

counter_names = [
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA",
    "CUM_INVERSE", "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR",
    "CUM_B3", "CUM_GENERATE", "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
]
counters = [int(record[name]) for name in counter_names]
assert counters == [8114, 23156448, 8114, 1011, 2062008, 1085580, 468448, 308288, 0, 0, 0, 0]

wrapper = PREVIOUS_WRAPPER.read_text(encoding="ascii")
replacements = {
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_UNIT2_14622_V5_GPT56SOL.txt";':
        'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_UNIT8115_14622_RETRY_V6_GPT56SOL.txt";',
    "INTERNAL_GUARD_MS:=1320000; START_UNIT:=2;":
        "INTERNAL_GUARD_MS:=1320000; START_UNIT:=8115;",
    "INITIAL_COUNTERS:=[1,2592,1,1,76,36,32,32,0,0,0,0];":
        "INITIAL_COUNTERS:=[" + ",".join(map(str, counters)) + "];",
    'PREVIOUS_CHECKPOINT_SHA256:="64d6d862836150d64297ffc206d9312f21f4ce347f75955c809d624223d05913";':
        f'PREVIOUS_CHECKPOINT_SHA256:="{cp_hash}";',
    'PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_UNIT1_V4_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=1516;':
        f'PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/{PREVIOUS_OUTPUT.name}"; PREVIOUS_OUTPUT_PREFIX_BYTES:={prefix_bytes};',
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="438b65b1fb2c892511cd8bf22459bfbfd1c9830db6f07661cfa54cd9cfbd2d1e";':
        f'PREVIOUS_OUTPUT_PREFIX_SHA256:="{record["OUTPUT_PREFIX_SHA256"]}";',
}
for old, new in replacements.items():
    assert wrapper.count(old) == 1, old
    wrapper = wrapper.replace(old, new)

read_line = 'Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v5_gpt56sol.g");'
assert wrapper.count(read_line) == 1
retry_overlay = r'''
# Recovery-only I/O hardening. Frozen seed science remains in the hash-pinned V5 engine.
if LoadPackage("io")=fail then Error("IO package required by rename retry overlay"); fi;
S001_RAW_IO_RENAME:=IO_rename;
S001_RENAME_RETRY_MAX:=500;
S001_RENAME_RETRY_USEC:=20000;
MakeReadWriteGlobal("IO_rename");
IO_rename:=function(oldpath,newpath)
 local attempt,result;
 for attempt in [1..S001_RENAME_RETRY_MAX] do
  result:=S001_RAW_IO_RENAME(oldpath,newpath);
  if result=true then
   if attempt>1 then Print("ATOMIC_RENAME_RETRY_SUCCESS\tATTEMPTS\t",attempt,"\n"); fi;
   return true;
  fi;
  IO_select([],[],[],0,S001_RENAME_RETRY_USEC);
 od;
 Print("ATOMIC_RENAME_RETRY_EXHAUSTED\tATTEMPTS\t",S001_RENAME_RETRY_MAX,"\n");
 return false;
end;
'''.strip()
wrapper = wrapper.replace(read_line, retry_overlay + "\n" + read_line)
assert 'START_UNIT:=8115;' in wrapper
assert wrapper.count('S001_RAW_IO_RENAME:=IO_rename;') == 1
WRAPPER.write_text(wrapper, encoding="ascii", newline="\n")

runner = f'''#!/usr/bin/env bash
set -euo pipefail
ulimit -v 50331648
exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q /mnt/d/work/revise/production_code/escalations/{WRAPPER.name}
'''
RUNNER.write_text(runner, encoding="ascii", newline="\n")

failure_note = "\n".join([
    "CERTIFICATE\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001-SEGMENT002-FAILED-ATOMIC-RENAME",
    "STATUS\tFAILED_PARTIAL_SUPERSEDED_FOR_CONTINUATION",
    "REASON\tIO_rename returned fail while committing unit8115; GAP entered error break loop and external guard terminated it.",
    "LAST_VALID_UNIT\t8114",
    "NEXT_UNIT\t8115",
    "UNCOMMITTED_ALPHA_EVIDENCE\t24T5513 alpha1 unit8115",
    f"VALID_CHECKPOINT_SHA256\t{cp_hash}",
    f"VALID_OUTPUT_PREFIX_BYTES\t{prefix_bytes}",
    f"VALID_OUTPUT_PREFIX_SHA256\t{record['OUTPUT_PREFIX_SHA256']}",
    f"FAILED_TMP_PRESERVED_AS\t{FAILED_TMP.name}",
    f"FAILED_TMP_SHA256\t{tmp_hash}",
    f"SEGMENT002_OUTPUT_SHA256\t{sha(previous_bytes)}",
    f"SEGMENT002_STDERR_SHA256\t{sha(PREVIOUS_STDERR.read_bytes())}",
    "CANDIDATE_NUMERIC_IN_UNCOMMITTED_TAIL\t0",
    "RECOVERY_RULE\tResume lexicographic successor of last valid checkpoint, unit8115; do not count the uncommitted tail.",
    "DONE",
    "",
])
FAILURE_NOTE.write_text(failure_note, encoding="ascii", newline="\n")

print(f"BUILD_PASS\tSTART_UNIT\t8115\tCHECKPOINT_SHA256\t{cp_hash}")
print(f"FAILED_TMP_SHA256\t{tmp_hash}")
print(f"WRAPPER\t{WRAPPER.name}\tSHA256\t{sha(WRAPPER.read_bytes())}")
print(f"RUNNER\t{RUNNER.name}\tSHA256\t{sha(RUNNER.read_bytes())}")
print(f"FAILURE_NOTE\t{FAILURE_NOTE.name}\tSHA256\t{sha(FAILURE_NOTE.read_bytes())}")
