from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
names = [
    "gap_transitive_degree24_aut_profile_pc_domain_checkpoint_guard_recovery_gpt56sol.g",
    "gap_run_degree24_aut_profile_shard24_14766_14900_pc_domain_gpt56sol.g",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14766_14900_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_RUN_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_RUN_STDERR_GPT56SOL.txt",
    "build_verify_degree24_aut_profile_shard24_routing_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_ROUTING_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_ROUTING_VERIFY_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_ROUTING_VERIFY_STDERR_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_CHEAP_PROFILE_GPT56SOL_MANIFEST.sha256",
    "GAP_TRANSITIVE_DEGREE24_FORECAST_GPT56SOL_MANIFEST.sha256",
    "build_degree24_aut_profile_32shard_plan_gpt56sol.ps1",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_MANIFEST.sha256",
    "verify_single_pc_degree24_aut_profile_gpt56sol.py",
    "verify_merge_degree24_aut_profile_shard24_pc_routed_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_14766_14900_MERGED_ROUTED_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_VERIFY_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_VERIFY_RUN_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_VERIFY_RUN_STDERR_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_GPT56SOL_CERTIFICATE.md",
    "build_verify_degree24_aut_profile_shard24_manifest_gpt56sol.py",
]
assert len(names) == 27 and len(names) == len(set(names))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest().upper()


records = []
for name in names:
    path = base / name
    if not path.is_file():
        raise FileNotFoundError(name)
    records.append(f"{digest(path)}  {name}")
manifest = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD24_GPT56SOL_MANIFEST.sha256"
if manifest.exists():
    raise FileExistsError(manifest)
manifest.write_text("\n".join(records) + "\n", encoding="ascii", newline="\n")
checked = 0
for line in manifest.read_text(encoding="ascii").splitlines():
    match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
    if not match or digest(base / match.group(2)) != match.group(1):
        raise AssertionError(f"bad manifest entry: {line}")
    checked += 1
assert checked == len(names)
print(f"PASS manifest entries={checked} mismatches=0")
