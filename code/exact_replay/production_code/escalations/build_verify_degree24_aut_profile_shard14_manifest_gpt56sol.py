from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
names = [
    "gap_transitive_degree24_aut_profile_pc_domain_checkpoint_guard_recovery_gpt56sol.g",
    "gap_run_degree24_aut_profile_shard14_12333_12595_pc_domain_gpt56sol.g",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12333_12595_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_RUN_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_RUN_STDERR_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt",
    "build_degree24_aut_profile_32shard_plan_gpt56sol.ps1",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_MANIFEST.sha256",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_AUDIT_FAILED_V1_RECORD_GPT56SOL.txt",
    "verify_merge_degree24_aut_profile_shard14_pc_routed_FAILED_V1_PARSER_GPT56SOL.ps1",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_VERIFY_FAILED_V1_RECORD_GPT56SOL.txt",
    "verify_merge_degree24_aut_profile_shard14_pc_routed_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12333_12595_MERGED_ROUTED_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_VERIFY_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_VERIFY_RUN_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_VERIFY_RUN_STDERR_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_GPT56SOL_CERTIFICATE.md",
    "build_verify_degree24_aut_profile_shard14_manifest_gpt56sol.py",
]
if len(names) != len(set(names)):
    raise AssertionError("duplicate manifest target")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


records: list[str] = []
for name in names:
    path = base / name
    if not path.is_file():
        raise FileNotFoundError(name)
    records.append(f"{sha256(path)}  {name}")

manifest = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD14_GPT56SOL_MANIFEST.sha256"
if manifest.exists():
    raise FileExistsError(manifest)
manifest.write_text("\n".join(records) + "\n", encoding="ascii", newline="\n")

verified = 0
for line in manifest.read_text(encoding="ascii").splitlines():
    match = re.fullmatch(r"([0-9A-F]{64})  (.+)", line)
    if not match:
        raise AssertionError(f"malformed manifest record: {line}")
    if sha256(base / match.group(2)) != match.group(1):
        raise AssertionError(f"hash mismatch: {match.group(2)}")
    verified += 1
if verified != len(names):
    raise AssertionError("manifest item count")
print(f"PASS manifest entries={verified} mismatches=0")
