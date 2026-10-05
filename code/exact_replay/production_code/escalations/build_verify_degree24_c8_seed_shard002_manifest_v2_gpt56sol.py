#!/usr/bin/env python3
"""Build/check the normalized 27-entry shard002 SHA-256 manifest.

Default mode atomically publishes the exclusions record, manifest, and manifest
check after all scientific artifacts already exist.  ``--check-only`` is a
strict read-only rehash.  This source never runs GAP or the scientific verifier.
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
CHECK_NAME = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_MANIFEST_CHECK_GPT56SOL.txt"

PROFILE = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
PLAN = "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
SLICE = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_PLAN_SLICE_GPT56SOL.tsv"
ENGINE = "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard002_v7_gpt56sol.g"

S1_WRAPPER = "gap_run_degree24_c8_seed_shard002_segment001_unit1_14513_postverify_v7_gpt56sol.g"
S1_RUNNER = "run_degree24_c8_seed_shard002_segment001_postverify_v7.sh"
S1_OUTPUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt"
S1_STDOUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt"
S1_STDERR = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt"
INTERRUPTION = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_INTERRUPTED_EOF_EVIDENCE_GPT56SOL.txt"

S2_WRAPPER = "gap_run_degree24_c8_seed_shard002_segment002_unit12358_14513_postverify_v7_gpt56sol.g"
S2_RUNNER = "run_degree24_c8_seed_shard002_segment002_postverify_v7.sh"
S2_OUTPUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_UNIT12358_14513_POSTVERIFY_V7_GPT56SOL.txt"
S2_STDOUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_RUN_STDOUT_V7_GPT56SOL.txt"
S2_STDERR = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_RUN_STDERR_V7_GPT56SOL.txt"

VERIFIER = "verify_merge_degree24_c8_seed_shard002_gpt56sol.py"
VERIFIER_STDOUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDOUT_V3_GPT56SOL.txt"
VERIFIER_STDERR = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDERR_V3_GPT56SOL.txt"
INDEPENDENT_AUDIT = "independent_audit_degree24_c8_seed_shard002_gpt56sol.py"
INDEPENDENT_AUDIT_V2 = "independent_audit_degree24_c8_seed_shard002_v2_gpt56sol.py"
INDEPENDENT_AUDIT_STDOUT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_INDEPENDENT_AUDIT_STDOUT_V2_GPT56SOL.txt"
INDEPENDENT_AUDIT_STDERR = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_INDEPENDENT_AUDIT_STDERR_V2_GPT56SOL.txt"

CHECKPOINT = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt"
CANONICAL = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL.txt"
AGGREGATE = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_AGGREGATE_GPT56SOL.txt"
CERTIFICATE = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL_CERTIFICATE.md"

# Twenty-six normalized scientific/core artifacts plus EXCLUSIONS_NAME = 27.
CORE_NAMES = [
    ENGINE,
    PROFILE,
    PLAN,
    SLICE,
    S1_WRAPPER,
    S1_RUNNER,
    S1_OUTPUT,
    S1_STDOUT,
    S1_STDERR,
    INTERRUPTION,
    S2_WRAPPER,
    S2_RUNNER,
    S2_OUTPUT,
    S2_STDOUT,
    S2_STDERR,
    VERIFIER,
    VERIFIER_STDOUT,
    VERIFIER_STDERR,
    INDEPENDENT_AUDIT,
    INDEPENDENT_AUDIT_V2,
    INDEPENDENT_AUDIT_STDOUT,
    INDEPENDENT_AUDIT_STDERR,
    CHECKPOINT,
    CANONICAL,
    AGGREGATE,
    CERTIFICATE,
]

CORE_SHA256 = {
    ENGINE: "49D42E9354E24511EED3682FD5020608A470ED4DF1F1CC8DED417DD119924248",
    PROFILE: "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2",
    PLAN: "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2",
    SLICE: "87B78417B903A6F19680DE6F9A20B1A705C3600F892539A6198FA548FA4CF495",
    S1_WRAPPER: "22BC0E6E2A1DC32690844761B00AFCC1B34C41869D46AE1FF4AF7E498F5F7CAE",
    S1_RUNNER: "7F293FF84B2D098ED7696DDECBFD0B3923BE43BB8923566D613C832551B95E1B",
    S1_OUTPUT: "C1C900594FB8E367BF0EFE21EE03EA905A9A9DE2B85CA1442340A62A0B0F82C3",
    S1_STDOUT: "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    S1_STDERR: "7B93A10F1024EFC3B93B6700EF28E29C5525FC1DAE430E838C2D3E525A4F3290",
    INTERRUPTION: "B04F3E594F9F0655AC174DEB5EFE8648D8054DD6696490227C4BB2ACCC472D88",
    S2_WRAPPER: "04C92069FAFF3A0C848F126A4C6CA7E93B95C408438849E973E0D30881539967",
    S2_RUNNER: "7DE373B0E32E6E44084CE1395DBB50E01F0D981E85655D14C233BF2F3AA8B0BD",
    S2_OUTPUT: "B6A0303ABBF77EC96F1F1CE8440E7EC8873E32222B9034D14F17B77D8A4E29CB",
    S2_STDOUT: "0C763EC3910EA53BC1C55DEB6FE4986A6DD382DD3FAAF875AFA8BC07651E74A4",
    S2_STDERR: "D6927FC32DFB260C4A5ACAB6B3E72CBC91D00BFC8385709E0C4378B60B88AD44",
    VERIFIER: "C6CAF50F617BD6730445063758BEFA13A928735184E70CDA4D7C0E6F38F533F3",
    VERIFIER_STDOUT: "9628A291A2835248029F7D6A930355D5C34C5AC3F7D33F03F0DE3EDDD90F1B1F",
    VERIFIER_STDERR: "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    INDEPENDENT_AUDIT: "63EB3484523D80E6EBC076B6A405881545BCD63E3861DFE45DD40AF98394C027",
    INDEPENDENT_AUDIT_V2: "40A406683F3CE64178683B60435C197521928DF68C601A062E7B2C72BD271274",
    INDEPENDENT_AUDIT_STDOUT: "F960E1D14C9999F40D8E334310ED915BF027BF5628F732765728DCD5C2B5E56E",
    INDEPENDENT_AUDIT_STDERR: "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    CHECKPOINT: "4B380758E80EDD46B1C22BA96B9FA27A2BF5AF90D4712FDBEB731AC9055F1AEA",
    CANONICAL: "DC477D3834DD75E1E4487B0D3FFC4A9677965B8D10FC0AAAB90447D3202F5069",
    AGGREGATE: "E3DFA1ADB1431A8BD090C3CC568F8F5C3AE70DBCE6D65E03D3C9DE7057C838C6",
    CERTIFICATE: "902591ED5A7F7F3066E6A6F00755748FC337565BB00781DA396FF4652210A309",
}

FAILED_RECOVERY = [
    ("V1", "SOURCE", "build_degree24_c8_seed_shard002_segment002_recovery_v7_gpt56sol.py",
     "14E08EFDAE2D015E7B23D7CD5352465920CE8BE026AD93F67A02638E6A453E73"),
    ("V1", "STDOUT", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDOUT_FAILED_V1_GPT56SOL.txt",
     "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
    ("V1", "STDERR", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDERR_FAILED_V1_GPT56SOL.txt",
     "7E37178CA0B939184CED6FB21C74EF2A4856D3ED4FF46C780D54078ECF4F452B"),
    ("V2", "SOURCE", "build_degree24_c8_seed_shard002_segment002_recovery_v7_v2_gpt56sol.py",
     "2710EBB0475F3030366F57201AF4B0075B6260B2A66C070BBB54DDB0BC97384A"),
    ("V2", "STDOUT", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDOUT_FAILED_V2_GPT56SOL.txt",
     "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
    ("V2", "STDERR", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDERR_FAILED_V2_GPT56SOL.txt",
     "EA4F7AEAAA2B79A76A68514DF7ED0984BE6FCDCD8B769FE44FD1F43D6F030A85"),
]

SUCCESSFUL_RECOVERY = [
    ("SOURCE", "build_degree24_c8_seed_shard002_segment002_recovery_v7_v3_gpt56sol.py",
     "6A11B963E34F6D383E7FF2F4F377DFA58791D0AB184335FBBD62D571F8DAD198"),
    ("STDOUT", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDOUT_V3_GPT56SOL.txt",
     "289DF852B110BB7E6BA8AA7E02B3C7D3CA2A54B424F1C983667EBA6F614493EB"),
    ("STDERR", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_BUILD_STDERR_V3_GPT56SOL.txt",
     "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
]

SUPERSEDED_VERIFIER = [
    ("STDOUT", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDOUT_SUPERSEDED_RACE_V1_GPT56SOL.txt",
     "9628A291A2835248029F7D6A930355D5C34C5AC3F7D33F03F0DE3EDDD90F1B1F"),
    ("STDERR", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDERR_SUPERSEDED_RACE_V1_GPT56SOL.txt",
     "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
]

FAILED_INDEPENDENT_AUDIT = [
    ("STDOUT", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_INDEPENDENT_AUDIT_STDOUT_FAILED_V1_GPT56SOL.txt",
     "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
    ("STDERR", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_INDEPENDENT_AUDIT_STDERR_FAILED_V1_GPT56SOL.txt",
     "92DE9A8A44577EADDA2E781F315C61ADF36025DBBF01BCAB27A2FA70408AF2A5"),
]

MANIFEST_RE = re.compile(r"([0-9A-F]{64})  ([^\\/]+)")


class ManifestError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def file_bytes(name: str) -> bytes:
    path = BASE / name
    require(path.is_file(), f"missing file: {name}")
    return path.read_bytes()


def ascii_text(name: str) -> str:
    try:
        return file_bytes(name).decode("ascii")
    except UnicodeDecodeError as error:
        raise ManifestError(f"non-ASCII file: {name}") from error


def keyed_fields(line: str, tag: str) -> dict[str, str]:
    fields = line.split("\t")
    require(fields[0] == tag and len(fields) >= 3 and len(fields) % 2 == 1,
            f"malformed {tag}")
    keys = fields[1::2]
    require(len(keys) == len(set(keys)), f"duplicate {tag} field")
    return dict(zip(keys, fields[2::2], strict=True))


def verify_pinned_files() -> None:
    require(len(CORE_NAMES) == 26 and len(CORE_NAMES) == len(set(CORE_NAMES)),
            "normalized core membership")
    require(set(CORE_NAMES) == set(CORE_SHA256), "core/hash key mismatch")
    for name in CORE_NAMES:
        require(digest(file_bytes(name)) == CORE_SHA256[name], f"core hash mismatch: {name}")
    lineage = [
        *((name, sha) for _v, _kind, name, sha in FAILED_RECOVERY),
        *((name, sha) for _kind, name, sha in SUCCESSFUL_RECOVERY),
        *((name, sha) for _kind, name, sha in SUPERSEDED_VERIFIER),
        *((name, sha) for _kind, name, sha in FAILED_INDEPENDENT_AUDIT),
    ]
    for name, expected in lineage:
        require(name not in CORE_NAMES, f"excluded lineage entered core: {name}")
        require(digest(file_bytes(name)) == expected, f"lineage hash mismatch: {name}")


def checkpoint_fields() -> dict[str, str]:
    lines = ascii_text(CHECKPOINT).splitlines()
    require(len(lines) == 3, "checkpoint line count")
    require(lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002",
            "checkpoint certificate")
    require(lines[2] == "DONE", "checkpoint DONE")
    fields = lines[1].split("\t")
    require(fields[:2] == ["SHARD", "002"] and len(fields[2:]) % 2 == 0,
            "checkpoint shard/fields")
    keys = fields[2::2]
    require(len(keys) == len(set(keys)), "checkpoint duplicate field")
    values = dict(zip(keys, fields[3::2], strict=True))
    for key, expected in {
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
        require(values.get(key) == expected, f"checkpoint {key}")
    for key in ("OUTPUT_PREFIX_SHA256", "PREVIOUS_CHECKPOINT_SHA256", "PAYLOAD_SHA256"):
        require(re.fullmatch(r"[0-9a-f]{64}", values.get(key, "")) is not None,
                f"checkpoint {key}")
    return values


def unique_total(text: str, label: str) -> tuple[str, dict[str, str]]:
    lines = [line for line in text.splitlines() if line.startswith("TOTAL\t")]
    require(len(lines) == 1, f"{label}: unique TOTAL")
    return lines[0], keyed_fields(lines[0], "TOTAL")


def verify_semantics() -> None:
    interruption = ascii_text(INTERRUPTION)
    require(interruption.endswith("DONE\n"), "interruption evidence DONE/LF")
    for line in (
        "STATUS\tRECOVERABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT",
        "END_STATE\tINTERRUPTED_EOF_AFTER_COMMIT",
        "PRODUCER_TERMINAL_MARKER\tNONE",
        "LAST_COMMITTED_UNIT\t12357",
        "NEXT_UNIT\t12358",
        "LAST_COMMITTED_KEY_ALPHA\t24T5940\t18",
        "RECOVERY_KEY_ALPHA\t24T5940\t19",
        "NO_REPLAY\tCommitted units1..12357 excluded from successor segment",
        "CACHE_RULE\tRecovery rebuilds 24T5940 alpha1..18 beta cache only; SEED_PREDICATES_REPLAYED=0",
    ):
        require(line in interruption.splitlines(), f"interruption evidence: {line}")
    require(
        f"OUTPUT\t{S1_OUTPUT}\tBYTES\t9402079\tSHA256\t{CORE_SHA256[S1_OUTPUT]}\tLINES\t25159"
        in interruption.splitlines(), "interruption output identity")

    s1 = file_bytes(S1_OUTPUT)
    require(len(s1) == 9_402_079, "segment001 bytes")
    require(b"\nTOTAL\t" not in s1 and not s1.endswith(b"DONE\n"),
            "segment001 terminal synthesis")
    require(b"\nCANDIDATE_NUMERIC\t" not in s1, "segment001 candidate")

    s2 = ascii_text(S2_OUTPUT)
    require(s2.endswith("\nDONE\n"), "segment002 DONE")
    s2_total, s2_values = unique_total(s2, "segment002")
    del s2_total
    for key, expected in {
        "START_UNIT": "12358",
        "LAST_COMPLETE_UNIT": "14513",
        "SEGMENT_UNITS": "2156",
        "SEGMENT_RAW": "6623232",
        "CUM_UNITS": "14513",
        "CUM_RAW": "44583936",
        "INVARIANT_ALPHA_CLASSES": "14513",
        "B3": "0",
        "GENERATE": "0",
        "PARITY": "0",
        "CENTRALIZER_ORBITS": "0",
        "CANDIDATE_NUMERIC": "0",
        "PROFILE_KEYS_REBUILT": "84",
        "FINAL_CHECKPOINT_SHA256": CORE_SHA256[CHECKPOINT].lower(),
    }.items():
        require(s2_values.get(key) == expected, f"segment002 TOTAL {key}")

    checkpoint_fields()
    canonical = ascii_text(CANONICAL)
    require(canonical.endswith("\nDONE\n"), "canonical DONE")
    require(not any(line.startswith("CANDIDATE_NUMERIC\t") for line in canonical.splitlines()),
            "canonical candidate")
    total_line, total = unique_total(canonical, "canonical")
    for key, expected in {
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
        require(total.get(key) == expected, f"canonical TOTAL {key}")
    for fragment in (
        "SOURCE_SEGMENTS\t2",
        "SOURCE_SEGMENT_END\t001\tLAST_UNIT\t12357\tTERMINAL\tINTERRUPTED_EOF_AFTER_COMMIT",
        f"SOURCE_SEGMENT_BEGIN\t002\tFILE\t{S2_OUTPUT}\tSTART_UNIT\t12358",
        "INTERRUPTION_EVIDENCE\tSEGMENT\t001\tSTATUS\tINTERRUPTED_EOF_AFTER_COMMIT",
        f"PROFILE_SHA256\t{CORE_SHA256[PROFILE]}",
        f"PLAN_SHA256\t{CORE_SHA256[PLAN]}",
        f"FINAL_CHECKPOINT\t{CHECKPOINT}\tSHA256\t{CORE_SHA256[CHECKPOINT]}",
    ):
        require(fragment in canonical, f"canonical cross-link: {fragment}")

    require(file_bytes(VERIFIER_STDERR) == b"", "verifier stderr")
    verifier_lines = ascii_text(VERIFIER_STDOUT).splitlines()
    require(verifier_lines == [
        "PASS shard=002 segments=2 units=14513 raw=44583936 candidates=0 "
        f"canonical_sha256={CORE_SHA256[CANONICAL]} "
        f"aggregate_sha256={CORE_SHA256[AGGREGATE]} "
        f"checkpoint_sha256={CORE_SHA256[CHECKPOINT]}"
    ], "verifier stdout")

    require(file_bytes(INDEPENDENT_AUDIT_STDERR) == b"", "independent audit stderr")
    audit_lines = ascii_text(INDEPENDENT_AUDIT_STDOUT).splitlines()
    require(audit_lines == [
        "PASS independent_audit=1 shard=002 segments=2 keys=297 units=14513 raw=44583936",
        "GATES invariant=14513 beta=838 inverse=3192448 inverse_odd=1837420 orbit8=487264 relator=57568 B3=0 generate=0 centralizer=0 candidates=0",
        "RECOVERY segment001=INTERRUPTED_EOF_AFTER_COMMIT last=12357 segment002_start=12358 no_replay=PASS "
        f"final_checkpoint={CORE_SHA256[CHECKPOINT]}",
    ], "independent audit stdout")

    aggregate = ascii_text(AGGREGATE)
    require(aggregate.endswith("DONE\n") and "SOURCE_SEGMENTS\t2" in aggregate,
            "aggregate terminal/segments")
    require(total_line in aggregate.splitlines(), "aggregate/canonical TOTAL")
    for fragment in (
        f"VERIFIER_SOURCE_SHA256\t{CORE_SHA256[VERIFIER]}",
        f"CHECKPOINT_FILE\t{CHECKPOINT}\tSHA256\t{CORE_SHA256[CHECKPOINT]}",
        f"CANONICAL_OUTPUT\t{CANONICAL}\tSHA256\t{CORE_SHA256[CANONICAL]}",
        "CHECK\tPINNED_SEGMENT001_INTERRUPTED_EOF_AFTER_COMMIT_LINEAGE\tPASS",
    ):
        require(fragment in aggregate, f"aggregate cross-link: {fragment}")

    certificate = ascii_text(CERTIFICATE)
    require(certificate.endswith("DONE\n") and "INTERRUPTED_EOF_AFTER_COMMIT" in certificate,
            "certificate terminal/interruption")
    for expected in (
        CORE_SHA256[CANONICAL], CORE_SHA256[AGGREGATE], CORE_SHA256[CHECKPOINT],
        CORE_SHA256[VERIFIER], CORE_SHA256[ENGINE],
    ):
        require(expected in certificate, f"certificate hash: {expected}")


def exclusions_data() -> bytes:
    lines = [
        "CERTIFICATE\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002-EXCLUSIONS",
        "RULE\tOnly the 26 normalized core artifacts plus this exclusions record enter the 27-entry canonical manifest.",
        "RULE\tFailed or race-ambiguous streams are preserved but are not canonical evidence and contribute no sealed work unit.",
        f"INTERRUPTION_EVIDENCE\tCANONICAL\t{INTERRUPTION}\tSHA256\t{CORE_SHA256[INTERRUPTION]}"
        "\tEND_STATE\tINTERRUPTED_EOF_AFTER_COMMIT\tLAST_COMMITTED_UNIT\t12357\tNEXT_UNIT\t12358",
    ]
    for version, kind, name, sha in FAILED_RECOVERY:
        reason = "CHECKPOINT_SCHEMA_ASSERTION" if version == "V1" else "PHYSICAL_OUTPUT_VS_COMMITTED_PREFIX_ASSERTION"
        lines.append(
            f"EXCLUDED\tFAILED_RECOVERY_BUILDER_ATTEMPT_{version}\t{kind}\t{name}"
            f"\tSHA256\t{sha}\tREASON\t{reason}"
        )
    for kind, name, sha in SUCCESSFUL_RECOVERY:
        lines.append(f"RECOVERY_SUCCESS\tATTEMPT\tV3\t{kind}\t{name}\tSHA256\t{sha}")
    lines.extend([
        f"RECOVERY_SUCCESS\tCANONICAL_WRAPPER\t{S2_WRAPPER}\tSHA256\t{CORE_SHA256[S2_WRAPPER]}",
        f"RECOVERY_SUCCESS\tCANONICAL_RUNNER\t{S2_RUNNER}\tSHA256\t{CORE_SHA256[S2_RUNNER]}",
        f"RECOVERY_SUCCESS\tCANONICAL_OUTPUT\t{S2_OUTPUT}\tSHA256\t{CORE_SHA256[S2_OUTPUT]}"
        "\tSTART_UNIT\t12358\tPREVIOUS_UNIT\t12357",
    ])
    for kind, name, sha in SUPERSEDED_VERIFIER:
        lines.append(
            f"EXCLUDED\tSUPERSEDED_RACE_AMBIGUOUS_VERIFIER_RUN_V1\t{kind}\t{name}"
            f"\tSHA256\t{sha}\tREASON\tSOURCE_MUTATION_WINDOW_NO_IMMUTABLE_SOURCE_SNAPSHOT"
        )
    for kind, name, sha in FAILED_INDEPENDENT_AUDIT:
        lines.append(
            f"EXCLUDED\tFAILED_INDEPENDENT_AUDIT_RUN_V1\t{kind}\t{name}"
            f"\tSHA256\t{sha}\tREASON\tCRLF_BYTE_ASSERTION"
        )
    lines.extend([
        "RECOVERY_RULE\tCommitted units 1..12357 were not replayed; cache reconstruction for 24T5940 alpha1..18 ran zero seed predicates.",
        "EXCEPTION\tThe explicit segment001 INTERRUPTED_EOF evidence is canonical recovery lineage and is included directly in the manifest.",
        "DONE",
        "",
    ])
    return "\n".join(lines).encode("ascii")


def manifest_data(exclusions: bytes) -> bytes:
    lines = [f"{CORE_SHA256[name]}  {name}" for name in CORE_NAMES]
    lines.append(f"{digest(exclusions)}  {EXCLUSIONS_NAME}")
    return ("\n".join(lines) + "\n").encode("ascii")


def check_data(manifest: bytes, exclusions: bytes) -> bytes:
    return ("\n".join([
        "CERTIFICATE_CHECK\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002-MANIFEST",
        f"MANIFEST\t{MANIFEST_NAME}",
        f"MANIFEST_SHA256\t{digest(manifest)}",
        "ENTRIES_CHECKED\t27",
        "CORE_ENTRIES\t26",
        "EXCLUSIONS_RECORDS\t1",
        "FAILED_RECOVERY_ARTIFACTS_EXCLUDED\t6",
        "SUPERSEDED_VERIFIER_STREAMS_EXCLUDED\t2",
        "FAILED_INDEPENDENT_AUDIT_STREAMS_EXCLUDED\t2",
        "MISMATCHES\t0",
        f"CANONICAL_SHA256\t{CORE_SHA256[CANONICAL]}",
        f"AGGREGATE_SHA256\t{CORE_SHA256[AGGREGATE]}",
        f"CERTIFICATE_SHA256\t{CORE_SHA256[CERTIFICATE]}",
        f"CHECKPOINT_SHA256\t{CORE_SHA256[CHECKPOINT]}",
        f"INTERRUPTION_EVIDENCE_SHA256\t{CORE_SHA256[INTERRUPTION]}",
        f"EXCLUSIONS_SHA256\t{digest(exclusions)}",
        "CHECK\tINDEPENDENT_REHASH_SECOND_PASS\tPASS",
        "CHECK\tFAILED_V1_V2_RECOVERY_BUILDERS_EXCLUDED\tPASS",
        "CHECK\tSUCCESSFUL_V3_RECOVERY_LINEAGE_CROSS_LINKED\tPASS",
        "CHECK\tRACE_AMBIGUOUS_VERIFIER_STREAMS_EXCLUDED\tPASS",
        "CHECK\tFAILED_V1_AUDIT_STREAMS_EXCLUDED\tPASS",
        "CHECK\tINDEPENDENT_AUDIT_V2_PASS_AND_EMPTY_STDERR\tPASS",
        "CHECK\tINTERRUPTED_EOF_EVIDENCE_INCLUDED\tPASS",
        "CHECK\tVERIFIER_V3_PASS_AND_EMPTY_STDERR\tPASS",
        "CHECK\tCANONICAL_AGGREGATE_CERTIFICATE_CHECKPOINT_LINKS\tPASS",
        "DONE",
        "",
    ])).encode("ascii")


def parse_rehash(manifest: bytes, exclusions: bytes) -> None:
    try:
        lines = manifest.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise ManifestError("manifest non-ASCII") from error
    require(len(lines) == 27, "manifest entries")
    expected_names = CORE_NAMES + [EXCLUSIONS_NAME]
    seen: set[str] = set()
    parsed: list[str] = []
    for number, line in enumerate(lines, 1):
        match = MANIFEST_RE.fullmatch(line)
        require(match is not None, f"manifest syntax line {number}")
        expected_sha, name = match.groups()
        require(name not in seen, f"duplicate manifest member: {name}")
        seen.add(name)
        parsed.append(name)
        actual = digest(exclusions) if name == EXCLUSIONS_NAME else digest(file_bytes(name))
        require(actual == expected_sha, f"manifest rehash: {name}")
    require(parsed == expected_names, "manifest membership/order")
    all_excluded = {
        *(name for _v, _kind, name, _sha in FAILED_RECOVERY),
        *(name for _kind, name, _sha in SUPERSEDED_VERIFIER),
        *(name for _kind, name, _sha in FAILED_INDEPENDENT_AUDIT),
    }
    require(all_excluded.isdisjoint(seen), "excluded evidence entered manifest")


def stage(destination: Path, data: bytes) -> Path:
    temporary = destination.with_name("." + destination.name + ".tmp")
    require(not destination.exists(), f"refusing overwrite: {destination.name}")
    require(not temporary.exists(), f"stale temp: {temporary.name}")
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    require(temporary.read_bytes() == data, f"staged bytes: {destination.name}")
    return temporary


def publish(items: Iterable[tuple[Path, bytes]]) -> None:
    pairs = list(items)
    staged: list[tuple[Path, Path]] = []
    published: list[Path] = []
    try:
        for destination, data in pairs:
            staged.append((stage(destination, data), destination))
        for temporary, destination in staged:
            os.replace(temporary, destination)
            published.append(destination)
        for destination, data in pairs:
            require(destination.read_bytes() == data, f"published bytes: {destination.name}")
    except Exception:
        for temporary, _destination in staged:
            if temporary.exists():
                temporary.unlink()
        for destination in reversed(published):
            if destination.exists():
                destination.unlink()
        raise


def expected() -> tuple[bytes, bytes, bytes]:
    verify_pinned_files()
    verify_semantics()
    exclusions = exclusions_data()
    manifest = manifest_data(exclusions)
    parse_rehash(manifest, exclusions)
    check = check_data(manifest, exclusions)
    return exclusions, manifest, check


def check_existing(exclusions: bytes, manifest: bytes, check: bytes) -> None:
    require(file_bytes(EXCLUSIONS_NAME) == exclusions, "published exclusions bytes")
    require(file_bytes(MANIFEST_NAME) == manifest, "published manifest bytes")
    require(file_bytes(CHECK_NAME) == check, "published check bytes")
    parse_rehash(manifest, exclusions)


def run(check_only: bool) -> int:
    exclusions, manifest, check = expected()
    if check_only:
        check_existing(exclusions, manifest, check)
        mode = "check"
    else:
        for name in (EXCLUSIONS_NAME, MANIFEST_NAME, CHECK_NAME):
            require(not (BASE / name).exists(), f"refusing overwrite: {name}")
        publish([
            (BASE / EXCLUSIONS_NAME, exclusions),
            (BASE / MANIFEST_NAME, manifest),
            (BASE / CHECK_NAME, check),
        ])
        check_existing(exclusions, manifest, check)
        mode = "build"
    print(
        f"PASS mode={mode} entries=27 manifest_sha256={digest(manifest)} "
        f"check_sha256={digest(check)} exclusions_sha256={digest(exclusions)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true",
                        help="read-only rehash of already-published manifest artifacts")
    arguments = parser.parse_args()
    try:
        return run(arguments.check_only)
    except ManifestError as error:
        parser.exit(1, f"FAIL {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
