#!/usr/bin/env python3
"""Apply exact exclusions-lineage corrections to the sealed V2 manifest builder."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path(__file__).with_name(
    "build_verify_degree24_c8_seed_shard002_manifest_v2_gpt56sol.py"
)
SOURCE_SHA256 = "C2D0D192A88C406203DA3D1B9497151152E2C7611BCB791CC547648A1E045EB7"


source_bytes = SOURCE.read_bytes()
assert hashlib.sha256(source_bytes).hexdigest().upper() == SOURCE_SHA256
source = source_bytes.decode("ascii")


def replace_once(old: str, new: str) -> None:
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)


definitions = '''
FAILED_EXTERNAL_MANIFEST_CHECK = [
    ("STDOUT", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_MANIFEST_EXTERNAL_CHECK_STDOUT_FAILED_V1_GPT56SOL.txt",
     "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
    ("STDERR", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_MANIFEST_EXTERNAL_CHECK_STDERR_FAILED_V1_GPT56SOL.txt",
     "2BBF75C2E074A96B6EFCA27ED17C6432405A2C1C3ECF9712BC1A1FB549A153AF"),
]

SUPERSEDED_RACE_PRODUCTS = [
    ("CANONICAL", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL_SUPERSEDED_RACE_V1.txt",
     "DC477D3834DD75E1E4487B0D3FFC4A9677965B8D10FC0AAAB90447D3202F5069"),
    ("AGGREGATE", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_AGGREGATE_SUPERSEDED_RACE_V1.txt",
     "E3DFA1ADB1431A8BD090C3CC568F8F5C3AE70DBCE6D65E03D3C9DE7057C838C6"),
    ("CERTIFICATE", "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL_CERTIFICATE_SUPERSEDED_RACE_V1.md",
     "902591ED5A7F7F3066E6A6F00755748FC337565BB00781DA396FF4652210A309"),
]

SUPERSEDED_UNEXECUTED = [
    ("SOURCE", "build_verify_degree24_c8_seed_shard002_manifest_gpt56sol.py",
     "4D788FD0B292FA39F3A576D99E3CA484E42675F7ECB8341D6259C8D8064A735C"),
]

'''
replace_once(
    'MANIFEST_RE = re.compile(r"([0-9A-F]{64})  ([^\\\\/]+)")',
    definitions + 'MANIFEST_RE = re.compile(r"([0-9A-F]{64})  ([^\\\\/]+)")',
)

replace_once(
    '        *((name, sha) for _kind, name, sha in FAILED_INDEPENDENT_AUDIT),\n'
    '    ]',
    '        *((name, sha) for _kind, name, sha in FAILED_INDEPENDENT_AUDIT),\n'
    '        *((name, sha) for _kind, name, sha in FAILED_EXTERNAL_MANIFEST_CHECK),\n'
    '        *((name, sha) for _kind, name, sha in SUPERSEDED_RACE_PRODUCTS),\n'
    '        *((name, sha) for _kind, name, sha in SUPERSEDED_UNEXECUTED),\n'
    '    ]',
)

replace_once(
    '''    for kind, name, sha in FAILED_INDEPENDENT_AUDIT:
        lines.append(
            f"EXCLUDED\\tFAILED_INDEPENDENT_AUDIT_RUN_V1\\t{kind}\\t{name}"
            f"\\tSHA256\\t{sha}\\tREASON\\tCRLF_BYTE_ASSERTION"
        )
    lines.extend([
''',
    '''    for kind, name, sha in FAILED_INDEPENDENT_AUDIT:
        lines.append(
            f"EXCLUDED\\tFAILED_INDEPENDENT_AUDIT_RUN_V1\\t{kind}\\t{name}"
            f"\\tSHA256\\t{sha}\\tREASON\\tEMPTY_OR_CRLF_STREAM_CANONICALITY_ASSERTION"
        )
    for kind, name, sha in FAILED_EXTERNAL_MANIFEST_CHECK:
        lines.append(
            f"EXCLUDED\\tFAILED_EXTERNAL_MANIFEST_CHECK_V1\\t{kind}\\t{name}"
            f"\\tSHA256\\t{sha}\\tREASON\\tSTART_PROCESS_BASH_LC_ARGUMENT_SPLITTING_MANIFEST_NOT_FOUND"
        )
    for kind, name, sha in SUPERSEDED_RACE_PRODUCTS:
        lines.append(
            f"EXCLUDED\\tSUPERSEDED_RACE_AMBIGUOUS_VERIFIER_PRODUCT_V1\\t{kind}\\t{name}"
            f"\\tSHA256\\t{sha}\\tREASON\\tSOURCE_MUTATION_WINDOW_NO_IMMUTABLE_SOURCE_SNAPSHOT"
        )
    for kind, name, sha in SUPERSEDED_UNEXECUTED:
        lines.append(
            f"EXCLUDED\\tSUPERSEDED_UNEXECUTED\\t{kind}\\t{name}"
            f"\\tSHA256\\t{sha}\\tREASON\\tFINALIZED_V2_SOURCE_REPLACEMENT"
        )
    lines.extend([
''',
)

replace_once(
    '        "FAILED_INDEPENDENT_AUDIT_STREAMS_EXCLUDED\\t2",',
    '        "FAILED_INDEPENDENT_AUDIT_STREAMS_EXCLUDED\\t2",\n'
    '        "FAILED_EXTERNAL_MANIFEST_CHECK_STREAMS_EXCLUDED\\t2",\n'
    '        "SUPERSEDED_RACE_PRODUCTS_EXCLUDED\\t3",\n'
    '        "SUPERSEDED_UNEXECUTED_SOURCES_EXCLUDED\\t1",',
)

replace_once(
    '        "CHECK\\tFAILED_V1_AUDIT_STREAMS_EXCLUDED\\tPASS",',
    '        "CHECK\\tFAILED_V1_AUDIT_STREAMS_EXCLUDED\\tPASS",\n'
    '        "CHECK\\tFAILED_EXTERNAL_MANIFEST_CHECK_STREAMS_EXCLUDED\\tPASS",\n'
    '        "CHECK\\tRACE_AMBIGUOUS_VERIFIER_PRODUCTS_EXCLUDED\\tPASS",\n'
    '        "CHECK\\tSUPERSEDED_UNEXECUTED_DRAFT_EXCLUDED\\tPASS",',
)

replace_once(
    '        *(name for _kind, name, _sha in FAILED_INDEPENDENT_AUDIT),\n'
    '    }',
    '        *(name for _kind, name, _sha in FAILED_INDEPENDENT_AUDIT),\n'
    '        *(name for _kind, name, _sha in FAILED_EXTERNAL_MANIFEST_CHECK),\n'
    '        *(name for _kind, name, _sha in SUPERSEDED_RACE_PRODUCTS),\n'
    '        *(name for _kind, name, _sha in SUPERSEDED_UNEXECUTED),\n'
    '    }',
)

namespace = {"__file__": str(SOURCE), "__name__": "__main__"}
exec(compile(source, str(SOURCE) + "#V3_EXCLUSIONS_LINEAGE", "exec"), namespace)
