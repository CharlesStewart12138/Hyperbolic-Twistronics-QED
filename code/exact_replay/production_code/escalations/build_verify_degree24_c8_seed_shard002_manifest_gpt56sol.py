#!/usr/bin/env python3
"""Build or independently check the normalized shard002 SHA-256 manifest.

The default mode publishes three new files only after the shard verifier has
published its canonical output, aggregate, certificate, and V2 resource
streams.  ``--check-only`` performs the same semantic and byte-level checks
without writing anything.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Iterable


BASE = Path(__file__).resolve().parent

MANIFEST_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL_MANIFEST.sha256"
EXCLUSIONS_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_EXCLUSIONS_GPT56SOL.txt"
AUDIT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_MANIFEST_CHECK_GPT56SOL.txt"

PROFILE_NAME = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SLICE_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_PLAN_SLICE_GPT56SOL.tsv"
ENGINE_NAME = "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard002_v7_gpt56sol.g"

SEGMENT001_WRAPPER = (
    "gap_run_degree24_c8_seed_shard002_segment001_unit1_14513_postverify_v7_gpt56sol.g"
)
SEGMENT001_RUNNER = "run_degree24_c8_seed_shard002_segment001_postverify_v7.sh"
SEGMENT001_OUTPUT = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_"
    "UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt"
)
SEGMENT001_STDOUT = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt"
)
SEGMENT001_STDERR = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt"
)
INTERRUPTION_EVIDENCE = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_"
    "SEGMENT001_INTERRUPTED_EOF_EVIDENCE_GPT56SOL.txt"
)

SEGMENT002_WRAPPER = (
    "gap_run_degree24_c8_seed_shard002_segment002_"
    "unit12358_14513_postverify_v7_gpt56sol.g"
)
SEGMENT002_RUNNER = "run_degree24_c8_seed_shard002_segment002_postverify_v7.sh"
SEGMENT002_OUTPUT = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_"
    "UNIT12358_14513_POSTVERIFY_V7_GPT56SOL.txt"
)
SEGMENT002_STDOUT = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_RUN_STDOUT_V7_GPT56SOL.txt"
)
SEGMENT002_STDERR = (
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_RUN_STDERR_V7_GPT56SOL.txt"
)

VERIFIER_SOURCE = "verify_merge_degree24_c8_seed_shard002_gpt56sol.py"
VERIFIER_STDOUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDOUT_V2_GPT56SOL.txt"
VERIFIER_STDERR = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDERR_V2_GPT56SOL.txt"
CHECKPOINT_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt"
CANONICAL_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL.txt"
AGGREGATE_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_AGGREGATE_GPT56SOL.txt"
CERTIFICATE_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL_CERTIFICATE.md"

# The normalized core follows the sealed shard001 convention: immutable inputs,
# exact producer wrappers/runners, primary outputs and resource streams, explicit
# recovery evidence, verifier source/resources, and final sealed products only.
CORE_NAMES = [
    ENGINE_NAME,
    PROFILE_NAME,
    PLAN_NAME,
    SLICE_NAME,
    SEGMENT001_WRAPPER,
    SEGMENT001_RUNNER,
    SEGMENT001_OUTPUT,
    SEGMENT001_STDOUT,
    SEGMENT001_STDERR,
    INTERRUPTION_EVIDENCE,
    SEGMENT002_WRAPPER,
    SEGMENT002_RUNNER,
    SEGMENT002_OUTPUT,
    SEGMENT002_STDOUT,
    SEGMENT002_STDERR,
    VERIFIER_SOURCE,
    VERIFIER_STDOUT,
    VERIFIER_STDERR,
    CHECKPOINT_NAME,
    CANONICAL_NAME,
    AGGREGATE_NAME,
    CERTIFICATE_NAME,
]

# Exact immutable hashes known before final manifest publication.  Final
# segment002/verifier products are hashed only after the verifier has sealed them.
FIXED_CORE_SHA256 = {
    ENGINE_NAME: "49D42E9354E24511EED3682FD5020608A470ED4DF1F1CC8DED417DD119924248",
    PROFILE_NAME: "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2",
    PLAN_NAME: "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2",
    SLICE_NAME: "87B78417B903A6F19680DE6F9A20B1A705C3600F892539A6198FA548FA4CF495",
    SEGMENT001_WRAPPER: "22BC0E6E2A1DC32690844761B00AFCC1B34C41869D46AE1FF4AF7E498F5F7CAE",
    SEGMENT001_RUNNER: "7F293FF84B2D098ED7696DDECBFD0B3923BE43BB8923566D613C832551B95E1B",
    SEGMENT001_OUTPUT: "C1C900594FB8E367BF0EFE21EE03EA905A9A9DE2B85CA1442340A62A0B0F82C3",
    SEGMENT001_STDOUT: "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    SEGMENT001_STDERR: "7B93A10F1024EFC3B93B6700EF28E29C5525FC1DAE430E838C2D3E525A4F3290",
    INTERRUPTION_EVIDENCE: "B04F3E594F9F0655AC174DEB5EFE8648D8054DD6696490227C4BB2ACCC472D88",
    SEGMENT002_WRAPPER: "04C92069FAFF3A0C848F126A4C6CA7E93B95C408438849E973E0D30881539967",
    SEGMENT002_RUNNER: "7DE373B0E32E6E44084CE1395DBB50E01F0D981E85655D14C233BF2F3AA8B0BD",
    VERIFIER_SOURCE: "68464E56FAAF34EA2931150D8073A62E8E31BB9FA1BE838C260D46EF5B97B214",
}

# Failed builders and their separated build streams are preserved, but only
# their hashes appear inside the canonical exclusions record.
FAILED_LINEAGE = [
    (
        "V1",
        "SOURCE",
        "build_degree24_c8_seed_shard002_segment002_recovery_v7_gpt56sol.py",
        "14E08EFDAE2D015E7B23D7CD5352465920CE8BE026AD93F67A02638E6A453E73",
    ),
    (
        "V1",
        "STDOUT",
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDOUT_FAILED_V1_GPT56SOL.txt",
        "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    ),
    (
        "V1",
        "STDERR",
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDERR_FAILED_V1_GPT56SOL.txt",
        "7E37178CA0B939184CED6FB21C74EF2A4856D3ED4FF46C780D54078ECF4F452B",
    ),
    (
        "V2",
        "SOURCE",
        "build_degree24_c8_seed_shard002_segment002_recovery_v7_v2_gpt56sol.py",
        "2710EBB0475F3030366F57201AF4B0075B6260B2A66C070BBB54DDB0BC97384A",
    ),
    (
        "V2",
        "STDOUT",
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDOUT_FAILED_V2_GPT56SOL.txt",
        "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    ),
    (
        "V2",
        "STDERR",
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDERR_FAILED_V2_GPT56SOL.txt",
        "EA4F7AEAAA2B79A76A68514DF7ED0984BE6FCDCD8B769FE44FD1F43D6F030A85",
    ),
]

SUCCESS_LINEAGE = [
    (
        "SOURCE",
        "build_degree24_c8_seed_shard002_segment002_recovery_v7_v3_gpt56sol.py",
        "6A11B963E34F6D383E7FF2F4F377DFA58791D0AB184335FBBD62D571F8DAD198",
    ),
    (
        "STDOUT",
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDOUT_V3_GPT56SOL.txt",
        "289DF852B110BB7E6BA8AA7E02B3C7D3CA2A54B424F1C983667EBA6F614493EB",
    ),
    (
        "STDERR",
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDERR_V3_GPT56SOL.txt",
        "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    ),
]

SHA_LINE_RE = re.compile(r"([0-9A-F]{64})  ([^\\/]+)")


class ManifestError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def require_file(name: str) -> Path:
    path = BASE / name
    require(path.is_file(), f"missing file: {name}")
    return path


def ascii_bytes(name: str) -> bytes:
    data = require_file(name).read_bytes()
    try:
        data.decode("ascii")
    except UnicodeDecodeError as error:
        raise ManifestError(f"non-ASCII file: {name}") from error
    return data


def parse_fields(line: str, tag: str) -> dict[str, str]:
    fields = line.split("\t")
    require(fields[0] == tag, f"expected {tag} record")
    require(len(fields) >= 3 and len(fields) % 2 == 1, f"malformed {tag} record")
    names = fields[1::2]
    values = fields[2::2]
    require(len(names) == len(set(names)), f"duplicate {tag} field")
    return dict(zip(names, values, strict=True))


def validate_fixed_hashes(hashes: dict[str, str]) -> None:
    for name, expected in FIXED_CORE_SHA256.items():
        require(hashes[name] == expected, f"fixed core hash mismatch: {name}")
    for _version, _kind, name, expected in FAILED_LINEAGE:
        require(sha256_bytes(require_file(name).read_bytes()) == expected,
                f"failed-lineage hash mismatch: {name}")
    for _kind, name, expected in SUCCESS_LINEAGE:
        require(sha256_bytes(require_file(name).read_bytes()) == expected,
                f"successful-lineage hash mismatch: {name}")


def validate_interruption_evidence(data: bytes) -> None:
    text = data.decode("ascii")
    required_lines = {
        "CERTIFICATE_EVIDENCE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD002-SEGMENT001-INTERRUPTED-EOF",
        "STATUS\tRECOVERABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT",
        "END_STATE\tINTERRUPTED_EOF_AFTER_COMMIT",
        "PRODUCER_TERMINAL_MARKER\tNONE",
        "LAST_COMMITTED_UNIT\t12357",
        "NEXT_UNIT\t12358",
        "LAST_COMMITTED_KEY_ALPHA\t24T5940\t18",
        "RECOVERY_KEY_ALPHA\t24T5940\t19",
        "NO_REPLAY\tCommitted units1..12357 excluded from successor segment",
        "CACHE_RULE\tRecovery rebuilds 24T5940 alpha1..18 beta cache only; SEED_PREDICATES_REPLAYED=0",
        "DONE",
    }
    lines = set(text.splitlines())
    require(required_lines <= lines, "interruption evidence semantic mismatch")
    require(text.endswith("DONE\n"), "interruption evidence lacks LF DONE terminator")
    require(
        f"OUTPUT\t{SEGMENT001_OUTPUT}\tBYTES\t9402079\tSHA256\t"
        f"{FIXED_CORE_SHA256[SEGMENT001_OUTPUT]}\tLINES\t25159" in lines,
        "interruption evidence output identity mismatch",
    )
    require(
        "CHECKPOINT_SHA256\tF9BBA393686F0035FC9E248A9741A9E51A7B79F64D94DA2BA89E1CF9AEC2D5A3"
        in lines,
        "interruption evidence checkpoint mismatch",
    )
    require(
        "OUTPUT_PREFIX_BYTES\t9401850" in lines and
        "OUTPUT_PREFIX_SHA256\t7E5750670227D6FBA370DE06F2D420A64AD59040E3104D4EAE2EE6B34D231E22"
        in lines,
        "interruption evidence prefix mismatch",
    )


def validate_checkpoint(data: bytes) -> None:
    lines = data.decode("ascii").splitlines()
    require(len(lines) == 3, "final checkpoint line count")
    require(
        lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002",
        "final checkpoint certificate",
    )
    require(lines[2] == "DONE", "final checkpoint DONE")
    values = parse_fields(lines[1], "SHARD")
    expected = {
        "002": "UNIT",
    }
    del expected  # The SHARD value is represented as the first field value.
    require(lines[1].startswith("SHARD\t002\t"), "final checkpoint shard")
    for key, value in {
        "UNIT": "14513",
        "KEY": "24T6031",
        "ALPHA": "8",
        "NEXT_UNIT": "14514",
        "CUM_UNITS": "14513",
        "CUM_RAW": "44583936",
        "CUM_INVARIANT_ALPHA": "14513",
        "CUM_B3": "0",
        "CUM_GENERATE": "0",
        "CUM_CENTRALIZER_ORBITS": "0",
        "CUM_CANDIDATE_NUMERIC": "0",
    }.items():
        require(values.get(key) == value, f"final checkpoint {key}")
    require(re.fullmatch(r"[0-9a-f]{64}", values.get("OUTPUT_PREFIX_SHA256", "")) is not None,
            "final checkpoint output-prefix SHA")
    require(re.fullmatch(r"[0-9a-f]{64}", values.get("PAYLOAD_SHA256", "")) is not None,
            "final checkpoint payload SHA")


def validate_total(text: str, label: str) -> str:
    total_lines = [line for line in text.splitlines() if line.startswith("TOTAL\t")]
    require(len(total_lines) == 1, f"{label}: unique TOTAL")
    values = parse_fields(total_lines[0], "TOTAL")
    for key, value in {
        "KEYS": "297",
        "CLASS_UNITS": "14513",
        "RAW_PAIRS": "44583936",
        "INVARIANT_ALPHA_CLASSES": "14513",
        "B3": "0",
        "GENERATE": "0",
        "PARITY": "0",
        "CENTRALIZER_ORBITS": "0",
        "CANDIDATE_NUMERIC": "0",
    }.items():
        require(values.get(key) == value, f"{label}: TOTAL {key}")
    return total_lines[0]


def validate_core() -> dict[str, str]:
    require(len(CORE_NAMES) == 22 and len(CORE_NAMES) == len(set(CORE_NAMES)),
            "normalized core membership")
    excluded_names = {name for _v, _k, name, _h in FAILED_LINEAGE}
    require(excluded_names.isdisjoint(CORE_NAMES), "failed attempts entered normalized core")

    hashes = {name: sha256_bytes(require_file(name).read_bytes()) for name in CORE_NAMES}
    validate_fixed_hashes(hashes)
    validate_interruption_evidence(ascii_bytes(INTERRUPTION_EVIDENCE))

    segment001 = ascii_bytes(SEGMENT001_OUTPUT)
    require(len(segment001) == 9_402_079, "segment001 physical byte count")
    require(segment001.count(b"\nTOTAL\t") == 0, "segment001 synthesized TOTAL")
    require(not segment001.endswith(b"DONE\n"), "segment001 synthesized terminal marker")
    require(b"\nCANDIDATE_NUMERIC\t" not in segment001, "segment001 candidate")

    segment002_text = ascii_bytes(SEGMENT002_OUTPUT).decode("ascii")
    require(segment002_text.endswith("\nDONE\n"), "segment002 terminal DONE")
    require(not any(line.startswith("CANDIDATE_NUMERIC\t")
                    for line in segment002_text.splitlines()), "segment002 candidate")
    validate_total(segment002_text, "segment002")

    canonical_text = ascii_bytes(CANONICAL_NAME).decode("ascii")
    require(canonical_text.endswith("\nDONE\n"), "canonical terminal DONE")
    require(not any(line.startswith("CANDIDATE_NUMERIC\t")
                    for line in canonical_text.splitlines()), "canonical candidate")
    total_line = validate_total(canonical_text, "canonical")
    for required in (
        "SOURCE_SEGMENTS\t2",
        "SOURCE_SEGMENT_END\t001\tLAST_UNIT\t12357\tTERMINAL\tINTERRUPTED_EOF_AFTER_COMMIT",
        f"SOURCE_SEGMENT_BEGIN\t002\tFILE\t{SEGMENT002_OUTPUT}\tSTART_UNIT\t12358",
        "INTERRUPTION_EVIDENCE\tSEGMENT\t001\tSTATUS\tINTERRUPTED_EOF_AFTER_COMMIT",
        f"PROFILE_SHA256\t{FIXED_CORE_SHA256[PROFILE_NAME]}",
        f"PLAN_SHA256\t{FIXED_CORE_SHA256[PLAN_NAME]}",
        f"FINAL_CHECKPOINT\t{CHECKPOINT_NAME}\tSHA256\t{hashes[CHECKPOINT_NAME]}",
    ):
        require(required in canonical_text, f"canonical cross-link: {required}")

    validate_checkpoint(ascii_bytes(CHECKPOINT_NAME))
    require(ascii_bytes(VERIFIER_STDERR) == b"", "verifier stderr is not empty")
    verifier_lines = ascii_bytes(VERIFIER_STDOUT).decode("ascii").splitlines()
    require(len(verifier_lines) == 1, "verifier stdout must be one line")
    verifier_line = verifier_lines[0]
    require(
        verifier_line.startswith(
            "PASS shard=002 segments=2 units=14513 raw=44583936 candidates=0 "
        ),
        "verifier PASS prefix",
    )
    for expected in (
        f"canonical_sha256={hashes[CANONICAL_NAME]}",
        f"aggregate_sha256={hashes[AGGREGATE_NAME]}",
        f"checkpoint_sha256={hashes[CHECKPOINT_NAME]}",
    ):
        require(expected in verifier_line, f"verifier cross-link: {expected}")

    aggregate_text = ascii_bytes(AGGREGATE_NAME).decode("ascii")
    require(aggregate_text.endswith("DONE\n"), "aggregate terminal DONE")
    require("SOURCE_SEGMENTS\t2" in aggregate_text, "aggregate segment count")
    require(total_line in aggregate_text.splitlines(), "aggregate TOTAL differs")
    for required in (
        f"VERIFIER_SOURCE_SHA256\t{hashes[VERIFIER_SOURCE]}",
        f"CHECKPOINT_FILE\t{CHECKPOINT_NAME}\tSHA256\t{hashes[CHECKPOINT_NAME]}",
        f"CANONICAL_OUTPUT\t{CANONICAL_NAME}\tSHA256\t{hashes[CANONICAL_NAME]}",
        "CHECK\tPINNED_SEGMENT001_INTERRUPTED_EOF_AFTER_COMMIT_LINEAGE\tPASS",
    ):
        require(required in aggregate_text, f"aggregate cross-link: {required}")

    certificate_text = ascii_bytes(CERTIFICATE_NAME).decode("ascii")
    require(certificate_text.endswith("DONE\n"), "certificate terminal DONE")
    for digest in (
        hashes[CANONICAL_NAME], hashes[AGGREGATE_NAME], hashes[CHECKPOINT_NAME],
        hashes[VERIFIER_SOURCE], FIXED_CORE_SHA256[INTERRUPTION_EVIDENCE],
    ):
        require(digest in certificate_text, f"certificate omits hash: {digest}")
    require("INTERRUPTED_EOF_AFTER_COMMIT" in certificate_text,
            "certificate omits interruption status")
    return hashes


def exclusions_bytes(hashes: dict[str, str]) -> bytes:
    lines = [
        "CERTIFICATE\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002-EXCLUSIONS",
        "RULE\tOnly the 22 normalized core artifacts plus this exclusions record enter the canonical manifest.",
        "RULE\tFailed recovery builder attempts V1/V2 are preserved but are not canonical producers and do not contribute a sealed work unit.",
        f"INTERRUPTION_EVIDENCE\tCANONICAL\t{INTERRUPTION_EVIDENCE}\tSHA256\t"
        f"{hashes[INTERRUPTION_EVIDENCE]}\tEND_STATE\tINTERRUPTED_EOF_AFTER_COMMIT"
        "\tLAST_COMMITTED_UNIT\t12357\tNEXT_UNIT\t12358",
    ]
    for version, kind, name, digest in FAILED_LINEAGE:
        reason = (
            "CHECKPOINT_SCHEMA_ASSERTION"
            if version == "V1" else "PHYSICAL_OUTPUT_VS_COMMITTED_PREFIX_ASSERTION"
        )
        lines.append(
            f"EXCLUDED\tFAILED_RECOVERY_BUILDER_ATTEMPT_{version}\t{kind}\t{name}"
            f"\tSHA256\t{digest}\tREASON\t{reason}"
        )
    for kind, name, digest in SUCCESS_LINEAGE:
        lines.append(
            f"RECOVERY_SUCCESS\tATTEMPT\tV3\t{kind}\t{name}\tSHA256\t{digest}"
        )
    lines.extend([
        f"RECOVERY_SUCCESS\tCANONICAL_WRAPPER\t{SEGMENT002_WRAPPER}\tSHA256\t"
        f"{hashes[SEGMENT002_WRAPPER]}",
        f"RECOVERY_SUCCESS\tCANONICAL_RUNNER\t{SEGMENT002_RUNNER}\tSHA256\t"
        f"{hashes[SEGMENT002_RUNNER]}",
        f"RECOVERY_SUCCESS\tCANONICAL_OUTPUT\t{SEGMENT002_OUTPUT}\tSHA256\t"
        f"{hashes[SEGMENT002_OUTPUT]}\tSTART_UNIT\t12358\tPREVIOUS_UNIT\t12357",
        "RECOVERY_RULE\tCommitted units 1..12357 were not replayed; cache reconstruction for 24T5940 alpha1..18 ran zero seed predicates.",
        "EXCEPTION\tThe explicit segment001 INTERRUPTED_EOF evidence is canonical recovery lineage and is included directly in the manifest.",
        "DONE",
        "",
    ])
    return "\n".join(lines).encode("ascii")


def manifest_bytes(hashes: dict[str, str], exclusions: bytes) -> bytes:
    members = CORE_NAMES + [EXCLUSIONS_NAME]
    member_hashes = dict(hashes)
    member_hashes[EXCLUSIONS_NAME] = sha256_bytes(exclusions)
    return ("\n".join(f"{member_hashes[name]}  {name}" for name in members) + "\n").encode("ascii")


def audit_bytes(hashes: dict[str, str], manifest: bytes, exclusions: bytes) -> bytes:
    return ("\n".join([
        "CERTIFICATE_CHECK\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002-MANIFEST",
        f"MANIFEST\t{MANIFEST_NAME}",
        f"MANIFEST_SHA256\t{sha256_bytes(manifest)}",
        "ENTRIES_CHECKED\t23",
        "CORE_ENTRIES\t22",
        "EXCLUSIONS_RECORDS\t1",
        "EXCLUDED_FAILED_RECOVERY_ARTIFACTS\t6",
        "MISMATCHES\t0",
        f"CANONICAL_SHA256\t{hashes[CANONICAL_NAME]}",
        f"AGGREGATE_SHA256\t{hashes[AGGREGATE_NAME]}",
        f"CERTIFICATE_SHA256\t{hashes[CERTIFICATE_NAME]}",
        f"CHECKPOINT_SHA256\t{hashes[CHECKPOINT_NAME]}",
        f"INTERRUPTION_EVIDENCE_SHA256\t{hashes[INTERRUPTION_EVIDENCE]}",
        f"EXCLUSIONS_SHA256\t{sha256_bytes(exclusions)}",
        "CHECK\tINDEPENDENT_REHASH_SECOND_PASS\tPASS",
        "CHECK\tFAILED_V1_V2_RECOVERY_BUILDERS_EXCLUDED\tPASS",
        "CHECK\tSUCCESSFUL_V3_RECOVERY_LINEAGE_CROSS_LINKED\tPASS",
        "CHECK\tINTERRUPTED_EOF_EVIDENCE_INCLUDED\tPASS",
        "CHECK\tVERIFIER_PASS_AND_EMPTY_STDERR\tPASS",
        "CHECK\tCANONICAL_AGGREGATE_CERTIFICATE_CHECKPOINT_LINKS\tPASS",
        "DONE",
        "",
    ])).encode("ascii")


def parse_and_rehash_manifest(manifest: bytes, exclusions: bytes) -> None:
    try:
        lines = manifest.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise ManifestError("manifest is not ASCII") from error
    require(len(lines) == 23, "manifest entry count")
    expected_names = CORE_NAMES + [EXCLUSIONS_NAME]
    seen: set[str] = set()
    parsed_names: list[str] = []
    for number, line in enumerate(lines, 1):
        match = SHA_LINE_RE.fullmatch(line)
        require(match is not None, f"manifest syntax line {number}")
        digest, name = match.groups()
        require(name not in seen, f"duplicate manifest member: {name}")
        seen.add(name)
        parsed_names.append(name)
        actual = sha256_bytes(exclusions) if name == EXCLUSIONS_NAME else sha256_bytes(require_file(name).read_bytes())
        require(actual == digest, f"manifest hash mismatch: {name}")
    require(parsed_names == expected_names, "manifest membership or order")
    failed_names = {name for _v, _k, name, _h in FAILED_LINEAGE}
    require(failed_names.isdisjoint(seen), "failed builder entered manifest")


def stage_new(path: Path, data: bytes) -> Path:
    temporary = path.with_name("." + path.name + ".tmp")
    require(not path.exists(), f"refusing to overwrite: {path.name}")
    require(not temporary.exists(), f"stale temp file: {temporary.name}")
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    require(temporary.read_bytes() == data, f"staged byte mismatch: {path.name}")
    return temporary


def publish_new(items: Iterable[tuple[Path, bytes]]) -> None:
    pairs = list(items)
    staged: list[tuple[Path, Path]] = []
    published: list[Path] = []
    try:
        for destination, data in pairs:
            staged.append((stage_new(destination, data), destination))
        for temporary, destination in staged:
            os.replace(temporary, destination)
            published.append(destination)
        for destination, data in pairs:
            require(destination.read_bytes() == data, f"published byte mismatch: {destination.name}")
    except Exception:
        for temporary, _destination in staged:
            if temporary.exists():
                temporary.unlink()
        for destination in reversed(published):
            if destination.exists():
                destination.unlink()
        raise


def expected_artifacts() -> tuple[dict[str, str], bytes, bytes, bytes]:
    hashes = validate_core()
    exclusions = exclusions_bytes(hashes)
    manifest = manifest_bytes(hashes, exclusions)
    parse_and_rehash_manifest(manifest, exclusions)
    audit = audit_bytes(hashes, manifest, exclusions)
    return hashes, exclusions, manifest, audit


def check_published(expected_exclusions: bytes, expected_manifest: bytes, expected_audit: bytes) -> None:
    actual_exclusions = require_file(EXCLUSIONS_NAME).read_bytes()
    actual_manifest = require_file(MANIFEST_NAME).read_bytes()
    actual_audit = require_file(AUDIT_NAME).read_bytes()
    require(actual_exclusions == expected_exclusions, "exclusions byte mismatch")
    require(actual_manifest == expected_manifest, "manifest byte mismatch")
    require(actual_audit == expected_audit, "audit byte mismatch")
    parse_and_rehash_manifest(actual_manifest, actual_exclusions)


def run(check_only: bool) -> int:
    _hashes, exclusions, manifest, audit = expected_artifacts()
    if check_only:
        check_published(exclusions, manifest, audit)
        mode = "check"
    else:
        for name in (EXCLUSIONS_NAME, MANIFEST_NAME, AUDIT_NAME):
            require(not (BASE / name).exists(), f"refusing to overwrite: {name}")
        publish_new([
            (BASE / EXCLUSIONS_NAME, exclusions),
            (BASE / MANIFEST_NAME, manifest),
            (BASE / AUDIT_NAME, audit),
        ])
        check_published(exclusions, manifest, audit)
        mode = "build"
    print(
        f"PASS mode={mode} entries=23 manifest_sha256={sha256_bytes(manifest)} "
        f"audit_sha256={sha256_bytes(audit)} exclusions_sha256={sha256_bytes(exclusions)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="rehash and validate existing manifest artifacts without writing",
    )
    arguments = parser.parse_args()
    try:
        return run(arguments.check_only)
    except ManifestError as error:
        parser.exit(1, f"FAIL {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
