#!/usr/bin/env python3
"""Independent, non-importing audit of the sealed degree-24 seed shard002."""

from __future__ import annotations

import hashlib
from pathlib import Path


B = Path(__file__).resolve().parent
FILES = {
    "profile": ("GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt", "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"),
    "plan": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv", "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"),
    "slice": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_PLAN_SLICE_GPT56SOL.tsv", "87B78417B903A6F19680DE6F9A20B1A705C3600F892539A6198FA548FA4CF495"),
    "engine": ("gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard002_v7_gpt56sol.g", "49D42E9354E24511EED3682FD5020608A470ED4DF1F1CC8DED417DD119924248"),
    "wrapper1": ("gap_run_degree24_c8_seed_shard002_segment001_unit1_14513_postverify_v7_gpt56sol.g", "22BC0E6E2A1DC32690844761B00AFCC1B34C41869D46AE1FF4AF7E498F5F7CAE"),
    "runner1": ("run_degree24_c8_seed_shard002_segment001_postverify_v7.sh", "7F293FF84B2D098ED7696DDECBFD0B3923BE43BB8923566D613C832551B95E1B"),
    "output1": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_UNIT1_14513_POSTVERIFY_V7_GPT56SOL.txt", "C1C900594FB8E367BF0EFE21EE03EA905A9A9DE2B85CA1442340A62A0B0F82C3"),
    "stdout1": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt", "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
    "stderr1": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt", "7B93A10F1024EFC3B93B6700EF28E29C5525FC1DAE430E838C2D3E525A4F3290"),
    "evidence1": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT001_INTERRUPTED_EOF_EVIDENCE_GPT56SOL.txt", "B04F3E594F9F0655AC174DEB5EFE8648D8054DD6696490227C4BB2ACCC472D88"),
    "wrapper2": ("gap_run_degree24_c8_seed_shard002_segment002_unit12358_14513_postverify_v7_gpt56sol.g", "04C92069FAFF3A0C848F126A4C6CA7E93B95C408438849E973E0D30881539967"),
    "runner2": ("run_degree24_c8_seed_shard002_segment002_postverify_v7.sh", "7DE373B0E32E6E44084CE1395DBB50E01F0D981E85655D14C233BF2F3AA8B0BD"),
    "output2": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_UNIT12358_14513_POSTVERIFY_V7_GPT56SOL.txt", "B6A0303ABBF77EC96F1F1CE8440E7EC8873E32222B9034D14F17B77D8A4E29CB"),
    "stdout2": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_RUN_STDOUT_V7_GPT56SOL.txt", "0C763EC3910EA53BC1C55DEB6FE4986A6DD382DD3FAAF875AFA8BC07651E74A4"),
    "stderr2": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_SEGMENT002_RUN_STDERR_V7_GPT56SOL.txt", "D6927FC32DFB260C4A5ACAB6B3E72CBC91D00BFC8385709E0C4378B60B88AD44"),
    "checkpoint": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_CHECKPOINT_GPT56SOL.txt", "4B380758E80EDD46B1C22BA96B9FA27A2BF5AF90D4712FDBEB731AC9055F1AEA"),
    "verifier": ("verify_merge_degree24_c8_seed_shard002_gpt56sol.py", "C6CAF50F617BD6730445063758BEFA13A928735184E70CDA4D7C0E6F38F533F3"),
    "verify_stdout": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDOUT_V3_GPT56SOL.txt", "9628A291A2835248029F7D6A930355D5C34C5AC3F7D33F03F0DE3EDDD90F1B1F"),
    "verify_stderr": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_VERIFIER_STDERR_V3_GPT56SOL.txt", "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"),
    "canonical": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL.txt", "DC477D3834DD75E1E4487B0D3FFC4A9677965B8D10FC0AAAB90447D3202F5069"),
    "aggregate": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_AGGREGATE_GPT56SOL.txt", "E3DFA1ADB1431A8BD090C3CC568F8F5C3AE70DBCE6D65E03D3C9DE7057C838C6"),
    "certificate": ("GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD002_GPT56SOL_CERTIFICATE.md", "902591ED5A7F7F3066E6A6F00755748FC337565BB00781DA396FF4652210A309"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def pairs(tokens: list[str], start: int = 1) -> dict[str, str]:
    assert (len(tokens) - start) % 2 == 0
    return dict(zip(tokens[start::2], tokens[start + 1::2], strict=True))


data: dict[str, bytes] = {}
for label, (name, expected_hash) in FILES.items():
    blob = (B / name).read_bytes()
    assert digest(blob) == expected_hash, (label, digest(blob), expected_hash)
    if blob:
        assert blob.endswith(b"\n") and b"\r" not in blob
        blob.decode("ascii")
    data[label] = blob

expected: list[tuple[int, int, int]] = []
expected_keys: list[int] = []
for line in data["slice"].decode("ascii").splitlines():
    tokens = line.split("\t")
    if tokens[0] != "WORK":
        continue
    fields = pairs(tokens)
    key = int(fields["KEY"][3:])
    first, last, order = int(fields["ALPHA_FIRST"]), int(fields["ALPHA_LAST"]), int(fields["ORDER"])
    expected_keys.append(key)
    expected.extend((key, alpha, order) for alpha in range(first, last + 1))
assert len(expected_keys) == len(set(expected_keys)) == 297
assert len(expected) == 14513
assert sum(item[2] for item in expected) == 44583936
assert expected[0][:2] == (5715, 67) and expected[-1][:2] == (6031, 8)


def alpha_records(blob: bytes) -> tuple[list[dict[str, str]], list[str], list[str]]:
    records: list[dict[str, str]] = []
    commits: list[str] = []
    tags: list[str] = []
    waiting_unit: int | None = None
    for line in blob.decode("ascii").splitlines():
        tokens = line.split("\t")
        tag = tokens[0]
        tags.append(tag)
        if tag == "ALPHA_DONE":
            assert waiting_unit is None
            record = pairs(tokens)
            waiting_unit = int(record["UNIT"])
            records.append(record)
        elif tag == "CHECKPOINT_COMMITTED":
            assert waiting_unit == int(tokens[2])
            commits.append(tokens[4])
            waiting_unit = None
    assert waiting_unit is None
    return records, commits, tags


r1, c1, t1 = alpha_records(data["output1"])
r2, c2, t2 = alpha_records(data["output2"])
records, commits = r1 + r2, c1 + c2
assert len(r1) == len(c1) == 12357
assert len(r2) == len(c2) == 2156
assert len(records) == len(commits) == 14513
assert [(int(r["KEY"][3:]), int(r["ALPHA"]), expected[index][2]) for index, r in enumerate(records)] == expected
assert [int(r["UNIT"]) for r in records] == list(range(1, 14514))
running_raw = 0
previous_checkpoint = "NONE_FRESH_START"
for index, (record, commit, (_, _, order)) in enumerate(zip(records, commits, expected, strict=True), 1):
    running_raw += order
    assert int(record["CUM_UNITS"]) == index
    assert int(record["CUM_RAW"]) == running_raw
    assert int(record["NEXT_UNIT"]) == index + 1
    assert record["PREVIOUS_CHECKPOINT_SHA256"].lower() == previous_checkpoint.lower()
    assert int(record["INVERSE_LOCUS"]) >= int(record["INVERSE_ODD"]) >= int(record["ORBIT8"])
    assert int(record["ORBIT8"]) >= int(record["RELATOR"]) >= int(record["B3"]) >= int(record["GENERATE"])
    assert int(record["CUM_B3"]) == int(record["CUM_GENERATE"]) == 0
    assert int(record["CUM_CENTRALIZER_ORBITS"]) == int(record["CUM_CANDIDATE_NUMERIC"]) == 0
    previous_checkpoint = commit
assert previous_checkpoint.upper() == FILES["checkpoint"][1]

assert len(data["output1"]) == 9402079 and len(t1) == 25159
assert t1.count("PROFILE_OK") == 214 and t1.count("KEY_SEGMENT_DONE") == 213
assert "TOTAL" not in t1 and "TOTAL_PARTIAL" not in t1 and "DONE" not in t1
assert data["output1"][:9401850] and digest(data["output1"][:9401850]) == "7E5750670227D6FBA370DE06F2D420A64AD59040E3104D4EAE2EE6B34D231E22"
assert len(data["output1"][9401850:]) == 229 and data["output1"][9401850:].startswith(b"CHECKPOINT_COMMITTED\tUNIT\t12357\t")
assert t2.count("CACHE_REBUILT") == 1 and t2.count("TOTAL") == 1 and t2[-1] == "DONE"
assert not any(tag == "CANDIDATE_NUMERIC" for tag in t1 + t2)

canonical_records, canonical_commits, canonical_tags = alpha_records(data["canonical"])
assert canonical_records == records and canonical_commits == commits
assert canonical_tags.count("PROFILE_OK") == canonical_tags.count("KEY_DONE") == 297
assert canonical_tags.count("SOURCE_SEGMENT_BEGIN") == canonical_tags.count("SOURCE_SEGMENT_END") == 2
assert canonical_tags.count("TOTAL") == 1 and canonical_tags[-1] == "DONE"
total_line = next(line for line in data["canonical"].decode("ascii").splitlines() if line.startswith("TOTAL\t"))
total = pairs(total_line.split("\t"))
assert (total["KEYS"], total["CLASS_UNITS"], total["RAW_PAIRS"]) == ("297", "14513", "44583936")
for name in ("B3", "GENERATE", "PARITY", "CENTRALIZER_ORBITS", "CANDIDATE_NUMERIC"):
    assert total[name] == "0"

checkpoint_lines = data["checkpoint"].decode("ascii").splitlines()
assert checkpoint_lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD002"
assert checkpoint_lines[-1] == "DONE" and "\tUNIT\t14513\t" in checkpoint_lines[1]
assert "\tNEXT_UNIT\t14514\t" in checkpoint_lines[1]
assert "\tCUM_RAW\t44583936\t" in checkpoint_lines[1]

aggregate = data["aggregate"].decode("ascii")
certificate = data["certificate"].decode("ascii")
assert "TERMINAL\tINTERRUPTED_EOF_AFTER_COMMIT" in aggregate
assert "WALL\tUNAVAILABLE\tMAX_RSS_KIB\tUNAVAILABLE\tEXIT_STATUS\tUNAVAILABLE" in aggregate
assert "TOTAL_SYNTHESIZED\tNO\tTERMINAL_SYNTHESIZED\tNO" in aggregate
assert "WALL\t4:03.85\tMAX_RSS_KIB\t201984\tEXIT_STATUS\t0" in aggregate
assert "Status: PASS -- complete zero-candidate run" in certificate
assert "does not synthesize TOTAL_PARTIAL" in certificate

print("PASS independent_audit=1 shard=002 segments=2 keys=297 units=14513 raw=44583936")
print("GATES invariant=14513 beta=838 inverse=3192448 inverse_odd=1837420 orbit8=487264 relator=57568 B3=0 generate=0 centralizer=0 candidates=0")
print("RECOVERY segment001=INTERRUPTED_EOF_AFTER_COMMIT last=12357 segment002_start=12358 no_replay=PASS final_checkpoint=4B380758E80EDD46B1C22BA96B9FA27A2BF5AF90D4712FDBEB731AC9055F1AEA")
