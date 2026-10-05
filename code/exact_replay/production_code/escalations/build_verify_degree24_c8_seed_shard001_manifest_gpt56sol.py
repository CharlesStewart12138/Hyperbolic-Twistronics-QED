from __future__ import annotations

import hashlib
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent
MANIFEST = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL_MANIFEST.sha256"
EXCLUSIONS = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_EXCLUSIONS_GPT56SOL.txt"
AUDIT = BASE / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_MANIFEST_CHECK_GPT56SOL.txt"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require_file(name: str) -> Path:
    path = BASE / name
    assert path.is_file(), name
    return path


assert not MANIFEST.exists() and not EXCLUSIONS.exists() and not AUDIT.exists()

canonical = require_file("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL.txt")
aggregate = require_file("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_AGGREGATE_GPT56SOL.txt")
certificate = require_file("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL_CERTIFICATE.md")
checkpoint = require_file("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_GPT56SOL.txt")
verifier_stdout = require_file("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDOUT_V2_GPT56SOL.txt")
verifier_stderr = require_file("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDERR_V2_GPT56SOL.txt")

canonical_text = canonical.read_text(encoding="ascii")
assert canonical_text.count("\nTOTAL\t") == 1
assert canonical_text.endswith("\nDONE\n")
assert not any(line.startswith("CANDIDATE_NUMERIC\t") for line in canonical_text.splitlines())
expected_total = (
    "TOTAL\tKEYS\t466\tCLASS_UNITS\t14622\tRAW_PAIRS\t43149024"
    "\tINVARIANT_ALPHA_CLASSES\t14622\tBETA_COMPUTATIONS\t1422"
    "\tINVERSE\t3921464\tINVERSE_ODD\t2362652\tORBIT8\t800992"
    "\tRELATOR\t352448\tB3\t0\tGENERATE\t0\tPARITY\t0"
    "\tCENTRALIZER_ORBITS\t0\tCANDIDATE_NUMERIC\t0"
)
assert expected_total in canonical_text.splitlines()
assert verifier_stderr.read_bytes() == b""
verifier_line = verifier_stdout.read_text(encoding="ascii").strip()
assert verifier_line.startswith("PASS shard=001 segments=3 units=14622 raw=43149024 candidates=0 ")
for expected in (
    f"canonical_sha256={sha(canonical)}",
    f"aggregate_sha256={sha(aggregate)}",
    f"checkpoint_sha256={sha(checkpoint)}",
):
    assert expected in verifier_line

aggregate_text = aggregate.read_text(encoding="ascii")
assert aggregate_text.endswith("DONE\n")
assert "SOURCE_SEGMENTS\t3" in aggregate_text
assert expected_total in aggregate_text.splitlines()
assert f"CANONICAL_OUTPUT\t{canonical.name}\tSHA256\t{sha(canonical)}" in aggregate_text
assert f"CHECKPOINT_FILE\t{checkpoint.name}\tSHA256\t{sha(checkpoint)}" in aggregate_text
certificate_text = certificate.read_text(encoding="ascii")
assert certificate_text.endswith("DONE\n")
for digest in (sha(canonical), sha(aggregate), sha(checkpoint)):
    assert digest in certificate_text

excluded_names = [
    "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_gpt56sol.g",
    "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v2_gpt56sol.g",
    "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v3_gpt56sol.g",
    "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v4_gpt56sol.g",
    "gap_run_degree24_c8_seed_shard001_gpt56sol.g",
    "gap_run_degree24_c8_seed_shard001_v2_gpt56sol.g",
    "gap_run_degree24_c8_seed_shard001_v3_gpt56sol.g",
    "gap_run_degree24_c8_seed_shard001_segment001_unit1_v4_gpt56sol.g",
    "run_degree24_c8_seed_shard001_segment001_v4.sh",
    "gap_run_degree24_c8_seed_shard001_segment003_unit8115_14622_retry_v6_gpt56sol.g",
    "run_degree24_c8_seed_shard001_segment003_retry_v6.sh",
    "gap_degree24_c8_seed_incremental_sha256_v6_DRAFT_NOT_RUN_gpt56sol.g",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_INCREMENTAL_SHA256_V6_STATIC_AUDIT_DRAFT_NOT_RUN_GPT56SOL.txt",
    "gap_probe_sha256_incremental_copy_gpt56sol.g",
    "GAP_SHA256_INCREMENTAL_COPY_PROBE_STDOUT_GPT56SOL.txt",
    "GAP_SHA256_INCREMENTAL_COPY_PROBE_STDERR_GPT56SOL.txt",
    "gap_probe_sha256_structural_copy_gpt56sol.g",
    "GAP_SHA256_STRUCTURAL_COPY_PROBE_STDOUT_GPT56SOL.txt",
    "GAP_SHA256_STRUCTURAL_COPY_PROBE_STDERR_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_RUN_STDOUT_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT001_RUN_STDERR_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CONTINUATION_BUILD_STDOUT_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CONTINUATION_BUILD_STDERR_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_BUILD_STDOUT_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_BUILD_STDERR_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDOUT_FAILED_V1_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDERR_FAILED_V1_GPT56SOL.txt",
]
excluded_lines = [
    "CERTIFICATE\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001-EXCLUSIONS",
    "RULE\tThese files are preserved but excluded from the canonical production manifest; none contributes a sealed unit.",
]
for name in excluded_names:
    path = require_file(name)
    status = "FAILED_EVIDENCE" if "FAILED" in name or "PROBE" in name else "SUPERSEDED_OR_DRAFT_NOT_RUN"
    excluded_lines.append(f"EXCLUDED\t{status}\t{name}\tSHA256\t{sha(path)}")
excluded_lines.extend([
    "EXCEPTION\tThe segment002 failed output/stdout/stderr, failed temporary checkpoint, and failure note ARE canonical recovery evidence and are included in the manifest.",
    "DONE",
    "",
])
EXCLUSIONS.write_text("\n".join(excluded_lines), encoding="ascii", newline="\n")

included_names = [
    "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_PLAN_SLICE_GPT56SOL.tsv",
    "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v5_gpt56sol.g",
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
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_CHECKPOINT_TMP_FAILED_AT_UNIT8115_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT002_FAILED_ATOMIC_RENAME_EVIDENCE_GPT56SOL.txt",
    "build_degree24_c8_seed_shard001_segment003_retry_gpt56sol.py",
    "run_build_degree24_c8_seed_shard001_segment003_retry_v2_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_BUILD_STDOUT_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_BUILD_STDERR_V2_GPT56SOL.txt",
    "build_degree24_c8_seed_shard001_segment003_postverify_v7_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_POSTVERIFY_BUILD_STDOUT_V7_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_POSTVERIFY_BUILD_STDERR_V7_GPT56SOL.txt",
    "gap_probe_io_rename_retry_override_gpt56sol.g",
    "GAP_IO_RENAME_RETRY_OVERRIDE_PROBE_STDOUT_GPT56SOL.txt",
    "GAP_IO_RENAME_RETRY_OVERRIDE_PROBE_STDERR_GPT56SOL.txt",
    "GAP_IO_RENAME_RETRY_PROBE_TARGET_GPT56SOL.txt",
    "gap_parse_smoke_degree24_c8_seed_shard001_segment003_postverify_v7_gpt56sol.g",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_PARSE_STDOUT_V7_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_PARSE_STDERR_V7_GPT56SOL.txt",
    "gap_run_degree24_c8_seed_shard001_segment003_unit8115_14622_postverify_v7_gpt56sol.g",
    "run_degree24_c8_seed_shard001_segment003_postverify_v7.sh",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_UNIT8115_14622_POSTVERIFY_V7_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_RUN_STDOUT_V7_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_RUN_STDERR_V7_GPT56SOL.txt",
    "verify_merge_degree24_c8_seed_shard001_gpt56sol.py",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDOUT_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_VERIFIER_STDERR_V2_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_CHECKPOINT_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_AGGREGATE_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_GPT56SOL_CERTIFICATE.md",
    EXCLUSIONS.name,
    Path(__file__).name,
]
assert len(included_names) == len(set(included_names))
manifest_lines = []
for name in included_names:
    path = require_file(name)
    manifest_lines.append(f"{sha(path)}  {name}")
MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="ascii", newline="\n")

# Independent second pass: parse, enforce canonical syntax, and rehash every entry.
seen: set[str] = set()
for number, line in enumerate(MANIFEST.read_text(encoding="ascii").splitlines(), 1):
    match = re.fullmatch(r"([0-9A-F]{64})  ([^\\/]+)", line)
    assert match, (number, line)
    digest, name = match.groups()
    assert name not in seen
    seen.add(name)
    assert sha(require_file(name)) == digest
assert seen == set(included_names)
audit_lines = [
    "CERTIFICATE_CHECK\tPF-GRP-001-C8-DEGREE24-SEED-SHARD001-MANIFEST",
    f"MANIFEST\t{MANIFEST.name}",
    f"MANIFEST_SHA256\t{sha(MANIFEST)}",
    f"ENTRIES_CHECKED\t{len(included_names)}",
    "MISMATCHES\t0",
    f"CANONICAL_SHA256\t{sha(canonical)}",
    f"AGGREGATE_SHA256\t{sha(aggregate)}",
    f"CERTIFICATE_SHA256\t{sha(certificate)}",
    f"CHECKPOINT_SHA256\t{sha(checkpoint)}",
    "CHECK\tUNIQUE_TOTAL_DONE_ZERO_CANDIDATE\tPASS",
    "CHECK\tVERIFIER_PASS_AND_EMPTY_STDERR\tPASS",
    "CHECK\tAGGREGATE_CERTIFICATE_HASH_CROSS_LINKS\tPASS",
    "CHECK\tMANIFEST_REHASH_SECOND_PASS\tPASS",
    "DONE",
    "",
]
AUDIT.write_text("\n".join(audit_lines), encoding="ascii", newline="\n")
print(f"PASS entries={len(included_names)} manifest_sha256={sha(MANIFEST)} audit_sha256={sha(AUDIT)}")
