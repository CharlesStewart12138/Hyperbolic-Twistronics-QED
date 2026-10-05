from __future__ import annotations

import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
source = base / "gap_run_degree24_c8_seed_shard001_gpt56sol.g"
profile = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
target = base / "gap_run_degree24_c8_seed_shard001_v2_gpt56sol.g"


def fields(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0
    return {parts[i]: parts[i + 1] for i in range(start, len(parts), 2)}


profile_rows: dict[int, dict[str, str]] = {}
for line in profile.read_text(encoding="utf-8").splitlines():
    if line.startswith("ENTRY\t"):
        parts = line.split("\t")
        profile_rows[int(parts[1][3:])] = fields(parts, 2)

text = source.read_text(encoding="utf-8")
record_pattern = re.compile(r'rec\(k:=(\d+),[^\n]+method:="(pc|native)",profileMs:=\d+\)')
counts = {"pc": 0, "native": 0}


def enrich(match: re.Match[str]) -> str:
    key = int(match.group(1))
    method = match.group(2)
    row = profile_rows[key]
    expected_representation = "legacy_sealed_pc" if method == "pc" else "legacy_original_native"
    expected_pc_order = int(row["ORDER"]) if method == "pc" else 0
    assert row["ROUTE"] == method
    assert row["REPRESENTATION"] == expected_representation
    assert int(row["PC_ORDER"]) == expected_pc_order
    counts[method] += 1
    return match.group(0).replace(
        f'method:="{method}",',
        f'method:="{method}",representation:="{expected_representation}",pcOrder:={expected_pc_order},',
    )


text, replacements = record_pattern.subn(enrich, text)
assert replacements == 466 and counts == {"pc": 453, "native": 13}
text = text.replace(
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";',
    'PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";\n'
    'PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;\n'
    'PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";\n'
    'CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_GPT56SOL.txt";\n'
    'CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_TMP_GPT56SOL.txt";',
)
text = text.replace(
    'gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_gpt56sol.g',
    'gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v2_gpt56sol.g',
)
assert text.count("CHECKPOINT_FILE:=") == 1
assert text.count("representation:=") == 466
assert text.count("alpha_checkpoint_v2_gpt56sol.g") == 1
if target.exists():
    raise FileExistsError(target)
target.write_text(text, encoding="utf-8", newline="\n")
print("PASS S001 V2 wrapper records=466 pc=453 native=13 representations=PASS pcOrder=PASS recovery=FRESH checkpoint=ATOMIC noSeeds=PASS")
