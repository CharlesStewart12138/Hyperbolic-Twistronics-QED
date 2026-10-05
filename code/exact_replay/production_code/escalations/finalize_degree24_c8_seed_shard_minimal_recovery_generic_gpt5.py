#!/usr/bin/env python3
"""Minimal finalizer with proof of checkpoint-sealed implicit commits."""

import re
from pathlib import Path


B = Path(__file__).resolve().parent
base = B / "finalize_degree24_c8_seed_shard_minimal_generic_gpt56sol.py"
source = base.read_text(encoding="ascii")
needle = "assert sorted(committed) == list(range(1, total_units + 1))\n"
insert = r'''# A process may atomically replace the checkpoint and then fail before
# appending the redundant CHECKPOINT_COMMITTED text line.  Recover such a unit
# only from a generic recovery evidence file and an exact next-unit hash link.
missing_commits = sorted(set(range(1, total_units + 1)) - set(committed))
for missing_unit in missing_commits:
    evidence_paths = list(B.glob(
        f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT*_RECOVERY_FROM_UNIT{missing_unit}_EVIDENCE_GPT5.txt"
    ))
    assert len(evidence_paths) == 1, (missing_unit, evidence_paths)
    evidence_data = evidence_paths[0].read_bytes()
    evidence_lines = evidence_data.decode("ascii").splitlines()
    assert evidence_lines[-1] == "DONE"
    scalar = {}
    source_row = None
    for evidence_line in evidence_lines:
        evidence_parts = evidence_line.split("\t")
        if evidence_parts[0] == "SOURCE_OUTPUT":
            assert len(evidence_parts) == 6
            source_row = evidence_parts
        elif len(evidence_parts) == 2:
            scalar[evidence_parts[0]] = evidence_parts[1]
    assert scalar["STATUS"] == "RECOVERABLE_DURABLE_PREFIX_NOT_TERMINAL_SHARD_RESULT"
    assert scalar["ORIGINAL_FILES_MODIFIED"] == "0"
    assert scalar["SYNTHETIC_SCIENTIFIC_RECORDS_ADDED"] == "0"
    assert int(scalar["LAST_DURABLE_UNIT"]) == missing_unit
    assert int(scalar["NEXT_UNIT"]) == missing_unit + 1
    assert source_row is not None and source_row[2] == "BYTES" and source_row[4] == "SHA256"
    sealed_source = B / source_row[1]
    sealed_data = sealed_source.read_bytes()
    assert len(sealed_data) == int(source_row[3]) and digest(sealed_data) == source_row[5]
    prefix_bytes = int(scalar["OUTPUT_PREFIX_BYTES"])
    prefix = sealed_data[:prefix_bytes]
    assert digest(prefix) == scalar["OUTPUT_PREFIX_SHA256"]
    expected_key, expected_alpha = expected[missing_unit - 1]
    sealed_last = prefix.decode("ascii").splitlines()[-1]
    assert sealed_last.startswith(
        f"ALPHA_DONE\tUNIT\t{missing_unit}\tKEY\t24T{expected_key}\tALPHA\t{expected_alpha}\t"
    )
    cp_sha = scalar["CHECKPOINT_SHA256"].lower()
    linked = False
    for _, recovery_output in outputs:
        for recovery_line in recovery_output.read_text(encoding="ascii").splitlines():
            if recovery_line.startswith(f"ALPHA_DONE\tUNIT\t{missing_unit + 1}\t"):
                assert f"\tPREVIOUS_CHECKPOINT_SHA256\t{cp_sha}\t" in recovery_line
                linked = True
                break
        if linked:
            break
    assert linked
    committed[missing_unit] = (expected_key, expected_alpha)

assert sorted(committed) == list(range(1, total_units + 1))
'''
assert source.count(needle) == 1
source = source.replace(needle, insert)
namespace = {"__file__": str(base), "__name__": "__main__"}
exec(compile(source, str(base) + "#RECOVERY_GENERIC", "exec"), namespace)
