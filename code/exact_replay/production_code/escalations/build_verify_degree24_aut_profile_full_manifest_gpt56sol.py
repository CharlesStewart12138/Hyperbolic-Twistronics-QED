from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
manifest_name = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AND_SEED_PLAN_GPT56SOL_MANIFEST.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest().upper()


names: list[str] = [
    "build_verify_degree24_aut_profile_full_merge_seed_plan_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGE_PLAN_RUN_STDOUT_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGE_PLAN_RUN_STDERR_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGE_PLAN_RUN_STDOUT_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGE_PLAN_RUN_STDERR_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_VERIFY_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_MANIFEST.sha256",
    "GAP_TRANSITIVE_DEGREE24_FORECAST_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_FORECAST_GPT56SOL_MANIFEST.sha256",
    "GAP_TRANSITIVE_DEGREE24_CHEAP_PROFILE_GPT56SOL_MANIFEST.sha256",
    "GAP_TRANSITIVE_DEGREE42_AUT_PROFILE_1_9491_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_MERGED_V3_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE45_AUT_PROFILE_1_10923_GPT56SOL.txt",
]

names.extend([
    f"GAP_TRANSITIVE_DEGREE24_PARITY_{lo}_{hi}_GPT56SOL.txt"
    for lo, hi in ((1, 7860), (7861, 10567), (10568, 13274), (13275, 25000))
])
names.extend([
    f"GAP_TRANSITIVE_DEGREE24_SOLVABILITY_{lo}_{hi}_GPT56SOL.txt"
    for lo, hi in ((1, 7860), (7861, 10567), (10568, 13274), (13275, 25000))
])

ranges = [
    (1, 5962), (5963, 6670), (6671, 7557), (7558, 8004),
    (8005, 8416), (8417, 8826), (8827, 9237), (9238, 9674),
    (9675, 10335), (10336, 10839), (10840, 11340), (11341, 11845),
    (11846, 12332), (12333, 12595), (12596, 12887), (12888, 13097),
    (13098, 13302), (13303, 13516), (13517, 13721), (13722, 13928),
    (13929, 14218), (14219, 14515), (14516, 14765), (14766, 14900),
    (14901, 15035), (15036, 15170), (15171, 15305), (15306, 15440),
    (15441, 15576), (15577, 15711), (15712, 15846), (15847, 25000),
]
for shard, (lo, hi) in enumerate(ranges, 1):
    tag = f"{shard:02d}"
    if shard <= 11:
        canonical = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_{lo}_{hi}_CHECKPOINT_GPT56SOL.txt"
    elif shard == 12:
        canonical = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11341_11845_MERGED_RECOVERY_GPT56SOL.txt"
    else:
        canonical = f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_{lo}_{hi}_MERGED_ROUTED_GPT56SOL.txt"
    names.extend([
        f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{tag}_GPT56SOL_MANIFEST.sha256",
        f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{tag}_AGGREGATE_GPT56SOL.txt",
        f"GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD{tag}_VERIFY_GPT56SOL.txt",
        canonical,
    ])

for degree in (42, 44, 45):
    for shard in range(1, 5):
        names.append(f"GAP_TRANSITIVE_DEGREE{degree}_C8_SHARD{shard}_AGGREGATE_GPT56SOL.txt")

names.append("build_verify_degree24_aut_profile_full_manifest_gpt56sol.py")
if len(names) != len(set(names)):
    raise AssertionError("duplicate manifest dependency")

records: list[str] = []
for name in names:
    path = base / name
    if not path.is_file():
        raise FileNotFoundError(name)
    records.append(f"{digest(path)}  {name}")

manifest = base / manifest_name
if manifest.exists():
    raise FileExistsError(manifest)
manifest.write_text("\n".join(records) + "\n", encoding="ascii", newline="\n")

checked = 0
for line in manifest.read_text(encoding="ascii").splitlines():
    match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
    if match is None or digest(base / match.group(2)) != match.group(1):
        raise AssertionError(f"bad manifest entry: {line}")
    checked += 1
if checked != len(names):
    raise AssertionError("manifest entry count")
print(f"PASS manifest entries={checked} mismatches=0")
