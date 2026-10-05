#!/usr/bin/env python3
"""Independent read-only audit of the sealed degree-24 C8 seed shard003.

This source is intentionally independent of the primary merger/verifier.  It
must be run only after the canonical output, aggregate, and certificate have
been atomically published.  It never writes files and never invokes GAP.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


B = Path(__file__).resolve().parent

PROFILE_SHA = "1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2"
PLAN_SHA = "0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2"
SLICE_SHA = "134DCF5EE79BB438CCCBF54DEC6C52EBD52A868002658683F066B58B9C4F1ECD"
FINAL_CHECKPOINT_SHA = "64DD24035E44833D5712B7E9265A54E66F47882BC86A2E1DA8B90B04C77FF1E9"
INTERRUPTED_CHECKPOINT_SHA = "261556AB596D01304C742D7EA5B55DC7CBBD524B68BCB9DAF03EC59D545E2360"
INTERRUPTED_PREFIX_BYTES = 6_148_317
INTERRUPTED_PREFIX_SHA = "77A95F05B20D2DAF91A477A36CAAF520C4B6DD042E91D5F17642B9B0FA382773"
FINAL_PREFIX_BYTES = 5_030_613
FINAL_PREFIX_SHA = "1A3D0FEB72F4FDFF0712025B2BCE3CA7660244041E1E9B2F66B36A1562700DB7"
INTERRUPTED_TERMINAL = "CHECKPOINT_WRITE_FAILURE_EXCLUDED_UNCOMMITTED_ALPHA"

PLAN_KEYS = 335
PLAN_UNITS = 14_648
PLAN_RAW = 44_998_656
PLAN_PROFILE_MS = 169_845
EXTERNAL_WALL_SECONDS = 1_400.0
VM_BYTES = 51_539_607_552

EXPECTED_TOTALS = {
    "KEYS": 335,
    "CLASS_UNITS": 14_648,
    "RAW_PAIRS": 44_998_656,
    "INVARIANT_ALPHA_CLASSES": 14_648,
    "BETA_COMPUTATIONS": 716,
    "INVERSE": 3_718_096,
    "INVERSE_ODD": 2_542_840,
    "ORBIT8": 533_888,
    "RELATOR": 77_696,
    "B3": 0,
    "GENERATE": 0,
    "PARITY": 0,
    "CENTRALIZER_ORBITS": 0,
    "CANDIDATE_NUMERIC": 0,
}

# Immutable producer inputs and stopped-run evidence.  Final canonical hashes
# are deliberately not hard-coded: they are cross-linked through the final
# aggregate/certificate and printed by this auditor after verification.
PINNED = {
    "profile": (
        "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt",
        PROFILE_SHA,
    ),
    "plan": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv",
        PLAN_SHA,
    ),
    "slice": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_PLAN_SLICE_GPT56SOL.tsv",
        SLICE_SHA,
    ),
    "engine": (
        "gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard003_v7_gpt56sol.g",
        "B5C1CFB76FF04F205846826700BCB6EAE36C96D7C89851B3434BEFDCE6A9BAA7",
    ),
    "wrapper1": (
        "gap_run_degree24_c8_seed_shard003_segment001_unit1_14648_postverify_v7_gpt56sol.g",
        "75CED8E1ECC7EB5B7DEB69E58E36726C2399C5D4F50630DD3B4ED6FC2FA0DD18",
    ),
    "runner1": (
        "run_degree24_c8_seed_shard003_segment001_postverify_v7.sh",
        "B92F2CE6F1E7210DF8C8BBF90D8E34ACF09B7C46099613E95ED56A924DF50C38",
    ),
    "output1": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNIT1_14648_POSTVERIFY_V7_GPT56SOL.txt",
        "6057F218A149B1DA02AD61BEFD315A8FB3575993F6B535010D927258F357DC16",
    ),
    "stdout1": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_RUN_STDOUT_V7_GPT56SOL.txt",
        "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
    ),
    "stderr1": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_RUN_STDERR_V7_GPT56SOL.txt",
        "7C961574C49D09B36471BCBB079CCBEE72BCED0CC2CFCBEC3C1760FC9DDF9099",
    ),
    "postprefix": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_POSTPREFIX_SUFFIX_COMMIT8089_UNCOMMITTED8090_GPT56SOL.txt",
        "326222482A1274D61702AEB610C900B6F63C4BE4DD383FC5450B95A0EBD590D6",
    ),
    "failed_tmp": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_UNCOMMITTED_CHECKPOINT_TMP_UNIT8090_GPT56SOL.txt",
        "1A4655A876AADD4CA6ED21FC7E2F4219A306FD57A0E0CC7AD616E7326ACDE0F8",
    ),
    "failure_evidence": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT001_CHECKPOINT_WRITE_FAILURE_EVIDENCE_GPT56SOL.txt",
        "05ACEE28DA8B95404F3357DAB0618E08B6CAD27636A70DC1BFE7487781F72A3E",
    ),
    "failed_preexec_stdout": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_RUN_STDOUT_FAILED_PREEXEC_V1_GPT56SOL.txt",
        "F9B82C671854AB2D01DA22EC2962CC8CD8F7480E6E9B65FB480F1001A0B35C1A",
    ),
    "failed_preexec_stderr": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_RUN_STDERR_FAILED_PREEXEC_V1_GPT56SOL.txt",
        "2DC5A8CCBD012CA4B3EEC2942ABE31B34B3503DF346A434050D49D2AFC736F5E",
    ),
    "failed_preexec_evidence": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_FAILED_PREEXEC_STALE_TMP_EVIDENCE_GPT56SOL.txt",
        "43D0DEA8E2E62BA2497778DE2A8EAC8A18E79E3D3908C7143B6EDFC355D6491F",
    ),
    "wrapper2": (
        "gap_run_degree24_c8_seed_shard003_segment002_v2_unit8090_14648_postverify_v7_gpt56sol.g",
        "69AAE6746E44F10574004935533820E162916CA66FBE0F06A317B5E47009DFE9",
    ),
    "runner2": (
        "run_degree24_c8_seed_shard003_segment002_v2_postverify_v7.sh",
        "6426B64A910214EEA64D6CF430C66C374435A45D28EE550F6F8D1E300DB662B2",
    ),
    "output2": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_V2_UNIT8090_14648_POSTVERIFY_V7_GPT56SOL.txt",
        "C00253A9B9178926008141204147984465D30EF27B5E984C43556E746DB0A96C",
    ),
    "stdout2": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_V2_RUN_STDOUT_V7_GPT56SOL.txt",
        "927A66F836750379EE68B62C06915AB08115D783EA786764DF1CE8C9931665EC",
    ),
    "stderr2": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_V2_RUN_STDERR_V7_GPT56SOL.txt",
        "9E7E13065B1145D6053594A6C1CCFC934B75C175BE420B938C2C26D43EBB225B",
    ),
    "checkpoint": (
        "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_GPT56SOL.txt",
        FINAL_CHECKPOINT_SHA,
    ),
}

FINAL_NAMES = {
    "canonical": "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_GPT56SOL.txt",
    "aggregate": "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_AGGREGATE_GPT56SOL.txt",
    "certificate": "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_GPT56SOL_CERTIFICATE.md",
    "verifier": "verify_merge_degree24_c8_seed_shard003_gpt56sol.py",
}


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest().upper()


def ascii_lines(blob: bytes, label: str, *, empty_ok: bool = False) -> list[str]:
    if not blob:
        assert empty_ok, f"{label}: unexpectedly empty"
        return []
    assert blob.endswith(b"\n"), f"{label}: missing final LF"
    assert b"\r" not in blob and b"\x00" not in blob, f"{label}: noncanonical bytes"
    return blob.decode("ascii").splitlines()


def pairs(tokens: list[str], start: int = 1) -> dict[str, str]:
    assert (len(tokens) - start) % 2 == 0, tokens
    result: dict[str, str] = {}
    for index in range(start, len(tokens), 2):
        assert tokens[index] not in result, tokens[index]
        result[tokens[index]] = tokens[index + 1]
    return result


def one(lines: list[str], tag: str) -> str:
    selected = [line for line in lines if line.split("\t", 1)[0] == tag]
    assert len(selected) == 1, (tag, len(selected))
    return selected[0]


def checkpoint_payload(blob: bytes, *, terminal_done: bool) -> tuple[dict[str, str], str]:
    lines = ascii_lines(blob, "checkpoint")
    assert lines[0] == "CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD003"
    assert (lines[-1] == "DONE") is terminal_done
    assert len(lines) == (3 if terminal_done else 2)
    marker = "\tPAYLOAD_SHA256\t"
    payload_line = lines[1]
    assert payload_line.count(marker) == 1
    payload, declared = payload_line.rsplit(marker, 1)
    assert digest(payload.encode("ascii")) == declared.upper()
    return pairs(payload.split("\t"), 0), declared.upper()


@dataclass
class OutputAudit:
    lines: list[str]
    tags: list[str]
    alpha: list[dict[str, str]]
    commits: list[dict[str, str]]
    waiting_unit: int | None


def audit_output_prefixes(blob: bytes, label: str) -> OutputAudit:
    """Verify every declared prefix byte count/hash in one streaming pass."""
    assert blob.endswith(b"\n") and b"\r" not in blob and b"\x00" not in blob
    running = hashlib.sha256()
    offset = 0
    lines: list[str] = []
    tags: list[str] = []
    alpha: list[dict[str, str]] = []
    commits: list[dict[str, str]] = []
    waiting: int | None = None
    for raw_line in blob.splitlines(keepends=True):
        assert raw_line.endswith(b"\n")
        line = raw_line[:-1].decode("ascii")
        lines.append(line)
        tokens = line.split("\t")
        tag = tokens[0]
        tags.append(tag)
        if tag == "ALPHA_DONE":
            assert waiting is None, (label, waiting)
            record = pairs(tokens)
            waiting = int(record["UNIT"])
            alpha.append(record)
        elif tag == "CHECKPOINT_COMMITTED":
            record = pairs(tokens)
            assert waiting == int(record["UNIT"]), (label, waiting, record["UNIT"])
            assert int(record["OUTPUT_PREFIX_BYTES"]) == offset
            assert record["OUTPUT_PREFIX_SHA256"].upper() == running.copy().hexdigest().upper()
            commits.append(record)
            waiting = None
        running.update(raw_line)
        offset += len(raw_line)
    assert offset == len(blob)
    return OutputAudit(lines, tags, alpha, commits, waiting)


def elapsed_seconds(stderr: str) -> float:
    match = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([0-9:.]+)", stderr)
    assert match
    parts = match.group(1).split(":")
    if len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    assert len(parts) == 3
    return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])


data: dict[str, bytes] = {}
for label, (name, expected_sha) in PINNED.items():
    blob = (B / name).read_bytes()
    assert digest(blob) == expected_sha, (label, digest(blob), expected_sha)
    ascii_lines(blob, label, empty_ok=(label == "stdout1"))
    data[label] = blob

# The sealed full profile and plan independently determine the exact shard.
profiles: dict[int, dict[str, str]] = {}
for line in data["profile"].decode("ascii").splitlines():
    tokens = line.split("\t")
    if tokens[0] == "ENTRY":
        key = int(tokens[1][3:])
        assert key not in profiles
        profiles[key] = pairs(tokens, 2)
assert len(profiles) == 10_714

plan_summary: dict[str, str] | None = None
plan_work: list[dict[str, str]] = []
for line in data["plan"].decode("ascii").splitlines():
    tokens = line.split("\t")
    if tokens[:2] == ["SHARD", "3"]:
        plan_summary = pairs(tokens, 2)
    elif tokens[:2] == ["WORK", "3"]:
        plan_work.append(pairs(tokens, 2))
assert plan_summary is not None
assert plan_summary == {
    "FIRST_KEY": "6032",
    "FIRST_ALPHA": "1",
    "LAST_KEY": "6440",
    "LAST_ALPHA": "2",
    "KEYS_TOUCHED": "335",
    "CLASS_UNITS": "14648",
    "RAW_PAIRS": "44998656",
    "PROFILE_REBUILD_MS": "169845",
    "PAIR_MODEL_MS": "599983",
    "POINT_MODEL_MS": "769828",
    "FRACTION_INTERNAL_GUARD": "0.583203",
}
assert len(plan_work) == PLAN_KEYS

slice_lines = data["slice"].decode("ascii").splitlines()
assert slice_lines[:5] == [
    "CERTIFICATE_PLAN_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003",
    f"PROFILE_SHA256\t{PROFILE_SHA}",
    f"PLAN_SHA256\t{PLAN_SHA}",
    "FIRST\t24T6032\t1",
    "LAST\t24T6440\t2",
]
assert slice_lines[-3:] == [
    "CHECKSUM\tKEYS\t335\tCLASS_UNITS\t14648\tRAW_PAIRS\t44998656\tPROFILE_REBUILD_MS\t169845\tPAIR_MODEL_MS\t599983\tPOINT_MODEL_MS\t769828\tFRACTION_INTERNAL_GUARD\t0.583203",
    "SEED_PREDICATES\tNOT_RUN_BY_BUILDER",
    "DONE",
]

slice_work = [pairs(line.split("\t")) for line in slice_lines if line.startswith("WORK\t")]
assert len(slice_work) == PLAN_KEYS
expected: list[tuple[int, int, int]] = []
route_totals: dict[str, list[int]] = {}
profile_cost = 0
for index, (planned, sliced) in enumerate(zip(plan_work, slice_work, strict=True)):
    key = int(planned["KEY"])
    first = int(planned["ALPHA_FIRST"])
    last = int(planned["ALPHA_LAST"])
    units = last - first + 1
    profile = profiles[key]
    assert sliced["KEY"] == f"24T{key}"
    assert int(sliced["UNIT_FIRST"]) == len(expected) + 1
    assert int(sliced["UNIT_LAST"]) == len(expected) + units
    assert (sliced["ALPHA_FIRST"], sliced["ALPHA_LAST"]) == (str(first), str(last))
    assert (planned["ORDER"], sliced["ORDER"], profile["ORDER"]) == ("3072", "3072", "3072")
    assert planned["CLASS_UNITS"] == str(units)
    assert int(planned["RAW_PAIRS"]) == 3072 * units
    assert int(profile["RAW_PAIRS"]) == 3072 * int(profile["ORDER8_CLASSES"])
    assert sliced["METHOD"] == profile["ROUTE"]
    assert sliced["REPRESENTATION"] == profile["REPRESENTATION"]
    assert sliced["PC_ORDER"] == profile["PC_ORDER"]
    assert sliced["PROFILE_COST_MS"] == profile["PROFILE_COST_MS"]
    if profile["ROUTE"] == "pc":
        assert profile["REPRESENTATION"] == "legacy_sealed_pc" and profile["PC_ORDER"] == "3072"
    else:
        assert (key, first, last) == (6032, 1, 42)
        assert profile["REPRESENTATION"] == "legacy_original_native" and profile["PC_ORDER"] == "0"
    expected.extend((key, alpha, 3072) for alpha in range(first, last + 1))
    route = profile["ROUTE"]
    tally = route_totals.setdefault(route, [0, 0, 0, 0])
    tally[0] += 1
    tally[1] += units
    tally[2] += 3072 * units
    tally[3] += int(profile["PROFILE_COST_MS"])
    profile_cost += int(profile["PROFILE_COST_MS"])
assert len(expected) == PLAN_UNITS and sum(order for _, _, order in expected) == PLAN_RAW
assert expected[0][:2] == (6032, 1) and expected[-1][:2] == (6440, 2)
assert profile_cost == PLAN_PROFILE_MS
assert route_totals == {
    "native": [1, 42, 129_024, 12_825],
    "pc": [334, 14_606, 44_869_632, 157_020],
}

range_profiles = {key: profiles[key] for key in range(6032, 6441)}
zero_keys = [key for key, value in range_profiles.items() if int(value["ORDER8_CLASSES"]) == 0]
assert len(zero_keys) == 74
assert len(range_profiles) == 409
assert all(int(value["PARITY_MAPS"]) > 0 and int(value["PARITY_MAPS"]) % 2 for value in range_profiles.values())

# Audit both stopped output files and every output-prefix declaration.
out1 = audit_output_prefixes(data["output1"], "segment001")
out2 = audit_output_prefixes(data["output2"], "segment002-v2")
assert [int(row["UNIT"]) for row in out1.alpha] == list(range(1, 8091))
assert [int(row["UNIT"]) for row in out1.commits] == list(range(1, 8090))
assert out1.waiting_unit == 8090
assert [int(row["UNIT"]) for row in out2.alpha] == list(range(8090, PLAN_UNITS + 1))
assert [int(row["UNIT"]) for row in out2.commits] == list(range(8090, PLAN_UNITS + 1))
assert out2.waiting_unit is None

assert len(data["output1"]) == 6_149_074
assert digest(data["output1"][:INTERRUPTED_PREFIX_BYTES]) == INTERRUPTED_PREFIX_SHA
assert data["output1"][INTERRUPTED_PREFIX_BYTES:] == data["postprefix"]
assert len(data["postprefix"]) == 757
assert len(data["output2"]) == 5_031_402
assert digest(data["output2"][:FINAL_PREFIX_BYTES]) == FINAL_PREFIX_SHA
assert int(out1.commits[-1]["OUTPUT_PREFIX_BYTES"]) == INTERRUPTED_PREFIX_BYTES
assert out1.commits[-1]["OUTPUT_PREFIX_SHA256"].upper() == INTERRUPTED_PREFIX_SHA
assert int(out2.commits[-1]["OUTPUT_PREFIX_BYTES"]) == FINAL_PREFIX_BYTES
assert out2.commits[-1]["OUTPUT_PREFIX_SHA256"].upper() == FINAL_PREFIX_SHA

failure_evidence = data["failure_evidence"].decode("ascii")
assert "LAST_DURABLE_UNIT\t8089" in failure_evidence
assert "NEXT_UNIT\t8090" in failure_evidence
assert "LAST_DURABLE_KEY_ALPHA\t24T6257\t15" in failure_evidence
assert f"CHECKPOINT_SHA256\t{INTERRUPTED_CHECKPOINT_SHA}" in failure_evidence
assert f"OUTPUT_PREFIX_BYTES\t{INTERRUPTED_PREFIX_BYTES}" in failure_evidence
assert f"OUTPUT_PREFIX_SHA256\t{INTERRUPTED_PREFIX_SHA}" in failure_evidence
assert "EXCLUSION\tUncommitted ALPHA_DONE unit8090 and failed TMP payload are evidence only and excluded from scientific totals" in failure_evidence
assert "RECOVERY\tSTART_UNIT8090 recomputes 24T6257 alpha16; committed units1..8089 are not replayed" in failure_evidence

tmp_fields, tmp_payload_sha = checkpoint_payload(data["failed_tmp"], terminal_done=False)
assert tmp_fields["UNIT"] == "8090" and tmp_fields["KEY"] == "24T6257" and tmp_fields["ALPHA"] == "16"
assert tmp_fields["OUTPUT_PREFIX_BYTES"] == str(len(data["output1"]))
assert tmp_fields["OUTPUT_PREFIX_SHA256"].upper() == digest(data["output1"])
assert tmp_fields["PREVIOUS_CHECKPOINT_SHA256"].upper() == INTERRUPTED_CHECKPOINT_SHA
assert tmp_payload_sha == "6B209F16190E322F772BB864EAE1BA3014E49C6EAA42A7B143ED1F8B445EAE37"

preexec = data["failed_preexec_evidence"].decode("ascii")
assert "STATUS\tFAILED_PREEXEC_SUPERSEDED_EXCLUDED" in preexec
assert "SCIENTIFIC_UNITS_EXECUTED\t0" in preexec
assert "OUTPUT_FILE_CREATED\t0" in preexec
assert "CHECKPOINT_MODIFIED\t0" in preexec
assert "Engine correctly rejected stale canonical checkpoint TMP" in preexec
assert not (B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_UNIT8090_14648_POSTVERIFY_V7_GPT56SOL.txt").exists()
assert not (B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_CHECKPOINT_TMP_GPT56SOL.txt").exists()

# Unit 8090 was physically evaluated twice, but its uncommitted copy is not
# scientific evidence.  The V2 recomputation must agree in every scientific
# field; only elapsed process time may differ.
scientific_fields = set(out1.alpha[-1]) - {"MS"}
assert scientific_fields == set(out2.alpha[0]) - {"MS"}
assert all(out1.alpha[-1][field] == out2.alpha[0][field] for field in scientific_fields)
cache = one(out2.lines, "CACHE_REBUILT").split("\t")
assert cache == [
    "CACHE_REBUILT", "24T6257", "ALPHA_FIRST", "1", "ALPHA_LAST", "15",
    "DISTINCT_BETA", "1", "SEED_PREDICATES_REPLAYED", "0",
]

scientific = out1.alpha[:8089] + out2.alpha
commits = out1.commits + out2.commits
assert len(scientific) == len(commits) == PLAN_UNITS
assert [(int(row["KEY"][3:]), int(row["ALPHA"]), expected[index][2])
        for index, row in enumerate(scientific)] == expected

running = {
    "RAW": 0,
    "INVERSE": 0,
    "INVERSE_ODD": 0,
    "ORBIT8": 0,
    "RELATOR": 0,
    "B3": 0,
    "GENERATE": 0,
    "PARITY": 0,
    "CENTRALIZER_ORBITS": 0,
}
previous_checkpoint = "NONE_FRESH_START"
previous_beta = 0
for unit, (row, commit, (_, _, order)) in enumerate(zip(scientific, commits, expected, strict=True), 1):
    assert int(row["UNIT"]) == unit and int(row["NEXT_UNIT"]) == unit + 1
    assert row["PREVIOUS_CHECKPOINT_SHA256"].upper() == previous_checkpoint.upper()
    previous_checkpoint = commit["CHECKPOINT_SHA256"]
    running["RAW"] += order
    running["INVERSE"] += int(row["INVERSE_LOCUS"])
    running["INVERSE_ODD"] += int(row["INVERSE_ODD"])
    running["ORBIT8"] += int(row["ORBIT8"])
    running["RELATOR"] += int(row["RELATOR"])
    running["B3"] += int(row["B3"])
    running["GENERATE"] += int(row["GENERATE"])
    running["PARITY"] += int(row["PARITY"])
    running["CENTRALIZER_ORBITS"] += int(row["CENTRALIZER_ORBITS"])
    assert int(row["CUM_UNITS"]) == int(row["CUM_INVARIANT_ALPHA"]) == unit
    assert int(row["CUM_RAW"]) == running["RAW"]
    assert int(row["CUM_INVERSE"]) == running["INVERSE"]
    assert int(row["CUM_INVERSE_ODD"]) == running["INVERSE_ODD"]
    assert int(row["CUM_ORBIT8"]) == running["ORBIT8"]
    assert int(row["CUM_RELATOR"]) == running["RELATOR"]
    assert int(row["CUM_B3"]) == running["B3"]
    assert int(row["CUM_GENERATE"]) == running["GENERATE"]
    assert int(row["CUM_CENTRALIZER_ORBITS"]) == running["CENTRALIZER_ORBITS"]
    assert int(row["CUM_CANDIDATE_NUMERIC"]) == 0
    beta = int(row["CUM_BETA"])
    assert previous_beta <= beta <= previous_beta + 1
    previous_beta = beta
    assert order >= int(row["INVERSE_LOCUS"]) >= int(row["INVERSE_ODD"])
    assert int(row["INVERSE_ODD"]) >= int(row["ORBIT8"]) >= int(row["RELATOR"])
    assert int(row["RELATOR"]) >= int(row["B3"]) >= int(row["GENERATE"])
assert previous_checkpoint.upper() == FINAL_CHECKPOINT_SHA
assert running == {
    "RAW": PLAN_RAW,
    "INVERSE": 3_718_096,
    "INVERSE_ODD": 2_542_840,
    "ORBIT8": 533_888,
    "RELATOR": 77_696,
    "B3": 0,
    "GENERATE": 0,
    "PARITY": 0,
    "CENTRALIZER_ORBITS": 0,
}
assert previous_beta == 716

assert out1.alpha[8088]["KEY"] == "24T6257" and out1.alpha[8088]["ALPHA"] == "15"
assert out1.alpha[8088]["CUM_RAW"] == "24849408"
assert out1.alpha[-1]["KEY"] == "24T6257" and out1.alpha[-1]["ALPHA"] == "16"
assert out2.alpha[0]["KEY"] == "24T6257" and out2.alpha[0]["ALPHA"] == "16"
assert out2.alpha[-1]["KEY"] == "24T6440" and out2.alpha[-1]["ALPHA"] == "2"
assert out1.alpha[-1]["PREVIOUS_CHECKPOINT_SHA256"].upper() == INTERRUPTED_CHECKPOINT_SHA
assert out2.alpha[0]["PREVIOUS_CHECKPOINT_SHA256"].upper() == INTERRUPTED_CHECKPOINT_SHA
assert out1.tags.count("CANDIDATE_NUMERIC") == out2.tags.count("CANDIDATE_NUMERIC") == 0
assert out1.tags.count("TOTAL") == out1.tags.count("TOTAL_PARTIAL") == out1.tags.count("DONE") == 0
assert out2.tags.count("TOTAL") == out2.tags.count("DONE") == 1
assert out2.tags[-1] == "DONE"

total2 = pairs(one(out2.lines, "TOTAL").split("\t"))
segment2_expected = {
    "START_UNIT": 8090,
    "LAST_COMPLETE_UNIT": 14648,
    "SEGMENT_UNITS": 6559,
    "SEGMENT_RAW": 20149248,
    "CUM_UNITS": 14648,
    "CUM_RAW": 44998656,
    "INVARIANT_ALPHA_CLASSES": 14648,
    "BETA_COMPUTATIONS": 716,
    "INVERSE": 3718096,
    "INVERSE_ODD": 2542840,
    "ORBIT8": 533888,
    "RELATOR": 77696,
    "B3": 0,
    "GENERATE": 0,
    "PARITY": 0,
    "CENTRALIZER_ORBITS": 0,
    "CANDIDATE_NUMERIC": 0,
    "PROFILE_KEYS_REBUILT": 144,
    "PROFILE_ACTUAL_MS": 84044,
    "GAP_MS": 431019,
}
for field, expected_value in segment2_expected.items():
    assert int(total2[field]) == expected_value, (field, total2[field])
assert total2["FINAL_CHECKPOINT_SHA256"].upper() == FINAL_CHECKPOINT_SHA

# Final checkpoint is complete, linked to the last V2 prefix, and byte-equal to
# the final commit hash.
checkpoint_fields, checkpoint_payload_sha = checkpoint_payload(data["checkpoint"], terminal_done=True)
assert checkpoint_fields["SHARD"] == "003"
assert checkpoint_fields["UNIT"] == "14648" and checkpoint_fields["NEXT_UNIT"] == "14649"
assert checkpoint_fields["KEY"] == "24T6440" and checkpoint_fields["ALPHA"] == "2"
assert checkpoint_fields["CUM_RAW"] == "44998656"
assert checkpoint_fields["CUM_BETA"] == "716"
assert checkpoint_fields["CUM_CANDIDATE_NUMERIC"] == "0"
assert checkpoint_fields["OUTPUT_PREFIX_BYTES"] == str(FINAL_PREFIX_BYTES)
assert checkpoint_fields["OUTPUT_PREFIX_SHA256"].upper() == FINAL_PREFIX_SHA
assert checkpoint_fields["PREVIOUS_CHECKPOINT_SHA256"].upper() == out2.commits[-2]["CHECKPOINT_SHA256"].upper()
assert checkpoint_fields["PROFILE_SHA256"] == PROFILE_SHA and checkpoint_fields["PLAN_SHA256"] == PLAN_SHA
assert checkpoint_payload_sha == "5D6D571D6F9833D72A26C69FAA0C6FB63C555BEFD2BF3813F4E463A9A35BB066"

# Resource streams: segment001 terminates at the checkpoint PrintTo failure;
# the stale-temp launch performs no scientific work; V2 terminates normally.
assert data["stdout1"] == b""
stderr1 = data["stderr1"].decode("ascii")
assert stderr1.count("Syntax warning: Unbound global variable") == 3
assert "Error, Could not write to file descriptor" in stderr1
assert "checkpoint PrintTo" in failure_evidence

stderr2 = data["stderr2"].decode("ascii")
assert stderr2.count("Syntax warning: Unbound global variable") == 3
assert "Error," not in stderr2
assert "Exit status: 0" in stderr2 and "Swaps: 0" in stderr2
assert elapsed_seconds(stderr2) <= EXTERNAL_WALL_SECONDS
rss_match = re.search(r"Maximum resident set size \(kbytes\): ([0-9]+)", stderr2)
assert rss_match and int(rss_match.group(1)) == 160_896
assert int(rss_match.group(1)) * 1024 <= VM_BYTES
assert data["stdout2"].decode("ascii") == (
    "WROTE /mnt/d/work/revise/production_code/escalations/"
    "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD003_SEGMENT002_V2_UNIT8090_14648_POSTVERIFY_V7_GPT56SOL.txt\n"
)

# The remainder requires the atomically published final seal.
final_data: dict[str, bytes] = {}
for label in ("canonical", "aggregate", "certificate", "verifier"):
    path = B / FINAL_NAMES[label]
    assert path.is_file(), f"run only after final seal: missing {path.name}"
    blob = path.read_bytes()
    ascii_lines(blob, label)
    final_data[label] = blob

canonical_lines = final_data["canonical"].decode("ascii").splitlines()
assert canonical_lines[0] == "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003-MERGED"
assert canonical_lines[1:13] == [
    "GAP_VERSION\t4.12.1",
    "DEGREE\t24",
    "DATABASE\t25000",
    "PLAN_FIRST\t24T6032\t1",
    "PLAN_LAST\t24T6440\t2",
    "PLAN_KEYS\t335",
    "PLAN_CLASS_UNITS\t14648",
    "PLAN_RAW_PAIRS\t44998656",
    f"PROFILE_SHA256\t{PROFILE_SHA}",
    f"PLAN_SHA256\t{PLAN_SHA}",
    "SOURCE_SEGMENTS\t2",
    "NORMALIZATION\tOne PROFILE_OK per unique key; all ALPHA_DONE and CHECKPOINT_COMMITTED records retained in unit order; KEY_DONE rebuilt from the sealed plan.",
]
canonical_alpha = [pairs(line.split("\t")) for line in canonical_lines if line.startswith("ALPHA_DONE\t")]
canonical_commits = [pairs(line.split("\t")) for line in canonical_lines if line.startswith("CHECKPOINT_COMMITTED\t")]
assert canonical_alpha == scientific
assert canonical_commits == commits
assert sum(line.startswith("PROFILE_OK\t") for line in canonical_lines) == PLAN_KEYS
assert sum(line.startswith("KEY_DONE\t") for line in canonical_lines) == PLAN_KEYS
assert sum(line.startswith("SOURCE_SEGMENT_BEGIN\t") for line in canonical_lines) == 2
assert sum(line.startswith("SOURCE_SEGMENT_END\t") for line in canonical_lines) == 2
assert any(f"SOURCE_SEGMENT_END\t001\tLAST_UNIT\t8089\tTERMINAL\t{INTERRUPTED_TERMINAL}\t" in line
           for line in canonical_lines)
assert any("SOURCE_SEGMENT_END\t002\tLAST_UNIT\t14648\tTERMINAL\tDONE\t" in line
           for line in canonical_lines)
assert any(line.startswith("INTERRUPTION_EVIDENCE\tSEGMENT\t001\t") and
           INTERRUPTED_TERMINAL in line and "EXCLUDED_PHYSICAL_ALPHA_DONE_UNIT\t8090" in line
           for line in canonical_lines)
canonical_total = pairs(one(canonical_lines, "TOTAL").split("\t"))
for field, expected_value in EXPECTED_TOTALS.items():
    assert int(canonical_total[field]) == expected_value
assert canonical_lines[-1] == "DONE"
assert "shard002" not in final_data["canonical"].decode("ascii").lower()

canonical_sha = digest(final_data["canonical"])
aggregate_sha = digest(final_data["aggregate"])
certificate_sha = digest(final_data["certificate"])
verifier_sha = digest(final_data["verifier"])
aggregate_lines = final_data["aggregate"].decode("ascii").splitlines()
aggregate_text = final_data["aggregate"].decode("ascii")
assert aggregate_lines[0] == "CERTIFICATE_AGGREGATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD003"
assert f"VERIFIER_SOURCE_SHA256\t{verifier_sha}" in aggregate_lines
assert f"PROFILE_SHA256\t{PROFILE_SHA}" in aggregate_lines
assert f"PLAN_SHA256\t{PLAN_SHA}" in aggregate_lines
assert f"CANONICAL_OUTPUT\t{FINAL_NAMES['canonical']}\tSHA256\t{canonical_sha}\tBYTES\t{len(final_data['canonical'])}" in aggregate_lines
assert any(line.startswith(f"CHECKPOINT_FILE\t{PINNED['checkpoint'][0]}\tSHA256\t{FINAL_CHECKPOINT_SHA}\t") and
           f"PAYLOAD_SHA256\t{checkpoint_payload_sha}" in line for line in aggregate_lines)
assert any(line.startswith("SOURCE_SEGMENT\t001\t") and
           "\tLAST_UNIT\t8089\t" in line and f"\tTERMINAL\t{INTERRUPTED_TERMINAL}\t" in line and
           "\tSEGMENT_UNITS\t8089\tSEGMENT_RAW\t24849408\t" in line for line in aggregate_lines)
assert any(line.startswith("SOURCE_SEGMENT\t002\t") and
           "\tSTART_UNIT\t8090\tLAST_UNIT\t14648\tTERMINAL\tDONE\t" in line and
           "\tSEGMENT_UNITS\t6559\tSEGMENT_RAW\t20149248\t" in line and
           "\tWALL\t9:01.60\tMAX_RSS_KIB\t160896\tEXIT_STATUS\t0\t" in line
           for line in aggregate_lines)
assert any(line.startswith("INTERRUPTION_EVIDENCE\tSEGMENT\t001\t") and
           INTERRUPTED_TERMINAL in line and "\tLAST_COMMITTED_UNIT\t8089\t" in line and
           f"\tCHECKPOINT_SHA256\t{INTERRUPTED_CHECKPOINT_SHA}\t" in line and
           "\tEXCLUDED_PHYSICAL_ALPHA_DONE_UNIT\t8090\t" in line and
           "\tTOTAL_SYNTHESIZED\tNO\tTERMINAL_SYNTHESIZED\tNO\t" in line and
           "\tRESOURCE_TELEMETRY\tUNAVAILABLE_PROCESS_FAILURE" in line
           for line in aggregate_lines)
aggregate_total = pairs(one(aggregate_lines, "TOTAL").split("\t"))
for field, expected_value in EXPECTED_TOTALS.items():
    assert int(aggregate_total[field]) == expected_value
assert "CHECK\tZERO_CANDIDATES\tPASS" in aggregate_lines
assert aggregate_lines[-1] == "DONE"
assert "shard002" not in aggregate_text.lower()
assert "external_wall" not in aggregate_text.lower() and "external-wall" not in aggregate_text.lower()

certificate_text = final_data["certificate"].decode("ascii")
assert "Status: PASS" in certificate_text
assert "shard 003" in certificate_text.lower()
assert "24T6032" in certificate_text and "24T6440" in certificate_text
assert "14,648" in certificate_text and "44,998,656" in certificate_text
assert "unit 8090" in certificate_text.lower() and "uncommitted" in certificate_text.lower()
assert INTERRUPTED_TERMINAL in certificate_text
assert PROFILE_SHA in certificate_text and PLAN_SHA in certificate_text
assert verifier_sha in certificate_text and canonical_sha in certificate_text
assert aggregate_sha in certificate_text and FINAL_CHECKPOINT_SHA in certificate_text
assert "shard 002" not in certificate_text.lower() and "shard002" not in certificate_text.lower()
assert "external-wall" not in certificate_text.lower()

source_sha = digest(Path(__file__).read_bytes())
print("PASS independent_audit=1 shard=003 segments=2 keys=335 units=14648 raw=44998656")
print("GATES invariant=14648 beta=716 inverse=3718096 inverse_odd=2542840 orbit8=533888 relator=77696 B3=0 generate=0 centralizer=0 candidates=0")
print(f"RECOVERY segment001={INTERRUPTED_TERMINAL} durable=8089 excluded=8090 segment002_start=8090 no_replay=PASS final_checkpoint={FINAL_CHECKPOINT_SHA}")
print(f"HASH canonical={canonical_sha} aggregate={aggregate_sha} certificate={certificate_sha} checkpoint={FINAL_CHECKPOINT_SHA} auditor={source_sha}")
