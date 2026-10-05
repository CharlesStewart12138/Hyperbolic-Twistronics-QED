from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent).resolve()
output_name = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_GPT56SOL_MANIFEST.sha256"
names = [
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AND_SEED_PLAN_GPT56SOL_MANIFEST.sha256",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_VERIFY_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_AGGREGATE_GPT56SOL.txt",
    "build_verify_degree24_aut_profile_full_merge_seed_plan_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGE_PLAN_RUN_STDOUT_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGE_PLAN_RUN_STDERR_V2_GPT56SOL.txt",
    "build_verify_degree24_aut_profile_full_manifest_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MANIFEST_VERIFY_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MANIFEST_VERIFY_STDERR_GPT56SOL.txt",
    "independent_audit_degree24_aut_profile_full_seed_plan_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_STDOUT_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_STDERR_FAILED_V1_GPT56SOL.txt",
    "independent_audit_degree24_aut_profile_full_seed_plan_v2_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_STDOUT_FAILED_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_STDERR_FAILED_V2_GPT56SOL.txt",
    "run_independent_audit_degree24_aut_profile_full_seed_plan_v3_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_V3_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_STDERR_V3_GPT56SOL.txt",
    "run_independent_audit_degree24_aut_profile_full_seed_plan_v4_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_V4_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_SECOND_AUDIT_STDERR_V4_GPT56SOL.txt",
    "build_verify_degree24_aut_profile_full_second_audit_manifest_gpt56sol.py",
]
if len(names) != len(set(names)):
    raise AssertionError("duplicate manifest dependency")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest().upper()


records = []
for name in names:
    path = base / name
    if not path.is_file():
        raise FileNotFoundError(name)
    records.append(f"{digest(path)}  {name}")

output = base / output_name
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="ascii", newline="\n")

checked = 0
for line in output.read_text(encoding="ascii").splitlines():
    match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
    if match is None or digest(base / match.group(2)) != match.group(1):
        raise AssertionError(f"manifest mismatch: {line}")
    checked += 1
if checked != len(names):
    raise AssertionError("manifest count")
print(f"PASS second-audit manifest entries={checked} mismatches=0")
