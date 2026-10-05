from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
checkpoint = base / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_GPT56SOL.txt"
previous_output = base / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_UNIT1_V4_GPT56SOL.txt"
source_wrapper = base / "gap_run_degree24_c8_seed_shard001_segment001_unit1_v5_gpt56sol.g"
target_wrapper = base / "gap_run_degree24_c8_seed_shard001_segment002_unit2_14622_v5_gpt56sol.g"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


lines = checkpoint.read_text(encoding="utf-8").splitlines()
assert lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001"
assert lines[-1] == "DONE" and len(lines) == 3
payload_line = lines[1]
payload, payload_hash = payload_line.rsplit("\tPAYLOAD_SHA256\t", 1)
assert sha(payload.encode("utf-8")) == payload_hash
parts = payload.split("\t")
assert len(parts) % 2 == 0
record = {parts[i]: parts[i + 1] for i in range(0, len(parts), 2)}
assert record["SHARD"] == "001" and record["UNIT"] == "1" and record["NEXT_UNIT"] == "2"
assert record["KEY"] == "24T5155" and record["ALPHA"] == "1"
counter_names = [
    "CUM_UNITS", "CUM_RAW", "CUM_INVARIANT_ALPHA", "CUM_BETA", "CUM_INVERSE",
    "CUM_INVERSE_ODD", "CUM_ORBIT8", "CUM_RELATOR", "CUM_B3", "CUM_GENERATE",
    "CUM_CENTRALIZER_ORBITS", "CUM_CANDIDATE_NUMERIC",
]
counters = [int(record[name]) for name in counter_names]
assert counters == [1, 2592, 1, 1, 76, 36, 32, 32, 0, 0, 0, 0]

previous_bytes = previous_output.read_bytes()
prefix_bytes = int(record["OUTPUT_PREFIX_BYTES"])
assert prefix_bytes == 1516 and len(previous_bytes) >= prefix_bytes
assert sha(previous_bytes[:prefix_bytes]) == record["OUTPUT_PREFIX_SHA256"]
checkpoint_sha = sha(checkpoint.read_bytes())
assert checkpoint_sha == "64d6d862836150d64297ffc206d9312f21f4ce347f75955c809d624223d05913"
assert record["PROFILE_SHA256"] == "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
assert record["PLAN_SHA256"] == "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
previous_text = previous_output.read_text(encoding="utf-8")
assert previous_text.count("ALPHA_DONE\tUNIT\t1\t") == 1
assert "CANDIDATE_NUMERIC\t" not in previous_text
assert previous_text.endswith("STOPPED_RECOVERY_SMOKE\n")

wrapper = source_wrapper.read_text(encoding="utf-8")
wrapper = wrapper.replace(
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_UNIT1_V4_GPT56SOL.txt";',
    'OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_UNIT2_14622_V5_GPT56SOL.txt";',
)
wrapper = wrapper.replace("STOP_AFTER_UNIT:=1;", "STOP_AFTER_UNIT:=fail;")
wrapper = wrapper.replace("INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;", "INTERNAL_GUARD_MS:=1320000; START_UNIT:=2;")
wrapper = re.sub(r"INITIAL_COUNTERS:=\[[^\n]+\];", "INITIAL_COUNTERS:=[" + ",".join(map(str, counters)) + "];", wrapper, count=1)
wrapper = wrapper.replace('PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";', f'PREVIOUS_CHECKPOINT_SHA256:="{checkpoint_sha}";')
wrapper = wrapper.replace('PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;',
    'PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_UNIT1_V4_GPT56SOL.txt"; '
    f'PREVIOUS_OUTPUT_PREFIX_BYTES:={prefix_bytes};')
wrapper = wrapper.replace('PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";',
    f'PREVIOUS_OUTPUT_PREFIX_SHA256:="{record["OUTPUT_PREFIX_SHA256"]}";')
assert wrapper.count("START_UNIT:=2") == 1
assert wrapper.count("STOP_AFTER_UNIT:=fail") == 1
assert wrapper.count(checkpoint_sha) == 1
assert wrapper.count(record["OUTPUT_PREFIX_SHA256"]) == 1
if target_wrapper.exists():
    raise FileExistsError(target_wrapper)
target_wrapper.write_text(wrapper, encoding="utf-8", newline="\n")
print(
    "PASS unit1 checkpoint/payload/output-prefix hashes; counters=" + ",".join(map(str, counters)) +
    f"; continuation START_UNIT=2 previousCheckpoint={checkpoint_sha} betaCacheRebuildRequired=24T5155:a1 noReplay=PASS"
)
