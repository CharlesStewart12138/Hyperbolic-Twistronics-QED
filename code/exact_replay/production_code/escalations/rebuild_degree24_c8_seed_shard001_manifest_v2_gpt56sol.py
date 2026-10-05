from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent
MANIFEST = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL_MANIFEST.sha256"
AUDIT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_MANIFEST_CHECK_GPT56SOL.txt"
EXCLUSIONS = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_EXCLUSIONS_GPT56SOL.txt"
OLD_MANIFEST = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL_MANIFEST_SUPERSEDED_V1.sha256"
OLD_AUDIT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_MANIFEST_CHECK_SUPERSEDED_V1_GPT56SOL.txt"
OLD_EXCLUSIONS = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_EXCLUSIONS_SUPERSEDED_V1_GPT56SOL.txt"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


for path in (MANIFEST, AUDIT, EXCLUSIONS):
    assert path.is_file(), path
for path in (OLD_MANIFEST, OLD_AUDIT, OLD_EXCLUSIONS):
    assert not path.exists(), path

# Preserve and validate the broad V1 manifest before replacing it.
old_lines = MANIFEST.read_text(encoding="ascii").splitlines()
assert len(old_lines) == 44
for line in old_lines:
    match = re.fullmatch(r"([0-9A-F]{64})  ([^\\/]+)", line)
    assert match
    digest, name = match.groups()
    assert sha(BASE / name) == digest
old_manifest_sha = sha(MANIFEST)
old_audit_sha = sha(AUDIT)
old_exclusions_sha = sha(EXCLUSIONS)
os.replace(MANIFEST, OLD_MANIFEST)
os.replace(AUDIT, OLD_AUDIT)
os.replace(EXCLUSIONS, OLD_EXCLUSIONS)

core = [
    "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v5_gpt56sol.g",
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_PLAN_SLICE_GPT56SOL.tsv",
    "gap_run_degree24_c8_seed_shard001_segment001_unit1_v5_gpt56sol.g",
    "run_degree24_c8_seed_shard001_segment001_v5.sh",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_UNIT1_V4_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_RUN_STDOUT_V5_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_RUN_STDERR_V5_GPT56SOL.txt",
    "gap_run_degree24_c8_seed_shard001_segment002_unit2_14622_v5_gpt56sol.g",
    "run_degree24_c8_seed_shard001_segment002_v5.sh",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_UNIT2_14622_V5_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_RUN_STDOUT_V5_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_RUN_STDERR_V5_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_FAILED_ATOMIC_RENAME_EVIDENCE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_CHECKPOINT_TMP_FAILED_AT_UNIT8115_GPT56SOL.txt",
    "gap_run_degree24_c8_seed_shard001_segment003_unit8115_14622_postverify_v7_gpt56sol.g",
    "run_degree24_c8_seed_shard001_segment003_postverify_v7.sh",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_UNIT8115_14622_POSTVERIFY_V7_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_RUN_STDOUT_V7_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_RUN_STDERR_V7_GPT56SOL.txt",
    "verify_merge_degree24_c8_seed_shard001_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDOUT_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDERR_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL_CERTIFICATE.md",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_GPT56SOL.txt",
    "gap_probe_io_rename_retry_override_gpt56sol.g",
    "GAP_IO_RENAME_RETRY_OVERRIDE_PROBE_STDOUT_GPT56SOL.txt",
    "GAP_IO_RENAME_RETRY_OVERRIDE_PROBE_STDERR_GPT56SOL.txt",
    "GAP_IO_RENAME_RETRY_PROBE_TARGET_GPT56SOL.txt",
]
assert len(core) == 32 and len(core) == len(set(core))
for name in core:
    assert (BASE / name).is_file(), name

excluded = sorted({
    *(line.split("  ", 1)[1] for line in old_lines),
    "build_verify_degree24_c8_seed_shard001_manifest_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_MANIFEST_BUILD_STDOUT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_MANIFEST_BUILD_STDERR_GPT56SOL.txt",
    OLD_MANIFEST.name, OLD_AUDIT.name, OLD_EXCLUSIONS.name,
} - set(core))
exclusion_lines = [
    "CERTIFICATE\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001-EXCLUSIONS-V2",
    "RULE\tOnly the 32 independently audited core artifacts plus this exclusions record enter the canonical manifest.",
    f"SUPERSEDED_V1_MANIFEST\t{OLD_MANIFEST.name}\tSHA256\t{old_manifest_sha}",
    f"SUPERSEDED_V1_AUDIT\t{OLD_AUDIT.name}\tSHA256\t{old_audit_sha}",
    f"SUPERSEDED_V1_EXCLUSIONS\t{OLD_EXCLUSIONS.name}\tSHA256\t{old_exclusions_sha}",
]
for name in excluded:
    path = BASE / name
    assert path.is_file(), name
    exclusion_lines.append(f"EXCLUDED\tPRESERVED_NOT_CANONICAL\t{name}\tSHA256\t{sha(path)}")
exclusion_lines.extend([
    "EXCEPTION\tSegment002 failed output/resources/note/tmp are core recovery lineage and remain canonical.",
    "DONE", "",
])
EXCLUSIONS.write_text("\n".join(exclusion_lines), encoding="ascii", newline="\n")

members = core + [EXCLUSIONS.name]
MANIFEST.write_text(
    "\n".join(f"{sha(BASE / name)}  {name}" for name in members) + "\n",
    encoding="ascii", newline="\n",
)

# Independent second pass.
seen: set[str] = set()
for line in MANIFEST.read_text(encoding="ascii").splitlines():
    match = re.fullmatch(r"([0-9A-F]{64})  ([^\\/]+)", line)
    assert match
    digest, name = match.groups()
    assert name not in seen
    seen.add(name)
    assert sha(BASE / name) == digest
assert seen == set(members)

AUDIT.write_text("\n".join([
    "CERTIFICATE_CHECK\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001-MANIFEST-V2",
    f"MANIFEST_SHA256\t{sha(MANIFEST)}",
    f"ENTRIES_CHECKED\t{len(members)}",
    "CORE_ENTRIES\t32",
    "EXCLUSIONS_RECORDS\t1",
    "MISMATCHES\t0",
    "CHECK\tINDEPENDENT_REHASH_SECOND_PASS\tPASS",
    "CHECK\tFAILED_AND_SUPERSEDED_BUILD_LINEAGE_EXCLUDED\tPASS",
    "CHECK\tSEGMENT002_RECOVERY_EXCEPTION_INCLUDED\tPASS",
    "DONE", "",
]), encoding="ascii", newline="\n")
print(f"PASS entries={len(members)} manifest_sha256={sha(MANIFEST)} audit_sha256={sha(AUDIT)}")
