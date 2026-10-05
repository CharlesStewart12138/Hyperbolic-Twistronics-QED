#!/usr/bin/env python3
"""Run the generic minimal finalizer with shard088's sealed-prefix recovery."""

from pathlib import Path


B = Path(__file__).resolve().parent
base = B / "finalize_degree24_c8_seed_shard_minimal_generic_gpt56sol.py"
source = base.read_text(encoding="ascii")
needle = "assert sorted(committed) == list(range(1, total_units + 1))\n"
insert = r'''# Shard088 committed unit2167 atomically before GAP failed to append the
# redundant CHECKPOINT_COMMITTED text record.  Accept that one unit only after
# verifying the sealed prefix, its recovery evidence, and the next-unit hash
# link.  No scientific output is edited or synthesized.
if shard == 88 and 2167 not in committed:
    old_cp_sha = "55D9349A83E248CE47822EF26E86A243D6EA774F1430569C0D0D6B576FBB74AA"
    s1 = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt"
    s2 = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT002_UNIT2168_3662_POSTVERIFY_V7_GPT56SOL.txt"
    evidence = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_APPEND_OPEN_RECOVERY_EVIDENCE_GPT56SOL.txt"
    s1_data = s1.read_bytes()
    evidence_data = evidence.read_bytes()
    assert len(s1_data) == 1609443
    assert digest(s1_data) == "F77F63818B7E403C7B710F8212CDE10053FA82DD3F15B25E178C7D291F83E7C7"
    assert digest(evidence_data) == "FBC45A05C5E486B7275859F237DB9650C72C6E0CB39C80C771E7539543B1B593"
    assert b"LAST_DURABLE_UNIT\t2167\nNEXT_UNIT\t2168\n" in evidence_data
    assert b"PHYSICAL_OUTPUT_EQUALS_SEALED_PREFIX\t1\n" in evidence_data
    assert b"CHECKPOINT_COMMITTED\tUNIT\t2167\t" not in s1_data
    s1_last = s1_data.decode("ascii").splitlines()[-1]
    assert s1_last.startswith("ALPHA_DONE\tUNIT\t2167\tKEY\t24T11606\tALPHA\t714\t")
    s2_lines = s2.read_text(encoding="ascii").splitlines()
    first_recovered = next(line for line in s2_lines if line.startswith("ALPHA_DONE\tUNIT\t2168\t"))
    assert "\tKEY\t24T11606\tALPHA\t715\t" in first_recovered
    assert "\tPREVIOUS_CHECKPOINT_SHA256\t" + old_cp_sha.lower() + "\t" in first_recovered
    assert expected[2166] == (11606, 714)
    committed[2167] = (11606, 714)

assert sorted(committed) == list(range(1, total_units + 1))
'''
assert source.count(needle) == 1
source = source.replace(needle, insert)
namespace = {"__file__": str(base), "__name__": "__main__"}
exec(compile(source, str(base) + "#S088_RECOVERY", "exec"), namespace)
