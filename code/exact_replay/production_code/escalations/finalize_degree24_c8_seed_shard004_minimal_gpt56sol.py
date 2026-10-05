#!/usr/bin/env python3
"""Minimal compute-first numerical closure for degree-24 seed shard004."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


B = Path(__file__).resolve().parent
S1 = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_UNIT1_14031_POSTVERIFY_V7_GPT56SOL.txt"
S2 = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT002_UNIT11897_14031_POSTVERIFY_V7_GPT56SOL.txt"
S2ERR = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT002_RUN_STDERR_V7_GPT56SOL.txt"
CP = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CHECKPOINT_GPT56SOL.txt"
RECOVERY = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_SEGMENT001_EXTERNAL_WALL_RECOVERY_EVIDENCE_GPT56SOL.txt"
AGG = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_CANONICAL_NUMERICAL_AGGREGATE_GPT56SOL.txt"
COMPLETE = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD004_COMPLETE_GPT56SOL.txt"
PROGRESS = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_PROGRESS_GPT56SOL.tsv"

S1_SHA = "4580fdd32dece25f022dbfb369b31cb0b84ff16d3fc6ae1d35dc939681604550"
S1_BYTES = 9_066_383
PREFIX_BYTES = 9_065_618
PREFIX_SHA = "d8addbd6fe7afcc9507da0794e5761bfc44e40ab0aad46a71816bfb65e784898"
S2_SHA = "8ba2cfc7226abe4707db9a4890afb4277b91855cc61cb7368381dd1cf9b1ddff"
S2_BYTES = 1_641_151
CP_SHA = "c05a1927bcf02de55cd3f8079f6b9b466b2a2a70d78f8422991cb3fbe32a29be"
COUNTERS = {
    "CUM_UNITS": 14031, "CUM_RAW": 43103232,
    "INVARIANT_ALPHA_CLASSES": 14031, "BETA_COMPUTATIONS": 700,
    "INVERSE": 3681152, "INVERSE_ODD": 2795440, "ORBIT8": 857184,
    "RELATOR": 142240, "B3": 0, "GENERATE": 0, "PARITY": 0,
    "CENTRALIZER_ORBITS": 0, "CANDIDATE_NUMERIC": 0,
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    temp = path.with_name(path.name + ".tmp")
    if temp.exists():
        raise RuntimeError(f"stale temp {temp}")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    assert not temp.exists() and path.read_bytes() == data


def record(line: str) -> dict[str, str]:
    parts = line.split("\t")
    assert len(parts) % 2 == 1
    return dict(zip(parts[1::2], parts[2::2], strict=True))


s1 = S1.read_bytes()
s2 = S2.read_bytes()
assert len(s1) == S1_BYTES and digest(s1) == S1_SHA
assert len(s2) == S2_BYTES and digest(s2) == S2_SHA
assert digest(s1[:PREFIX_BYTES]) == PREFIX_SHA
prefix_lines = s1[:PREFIX_BYTES].decode("ascii").splitlines()
s2_lines = s2.decode("ascii").splitlines()
alpha1 = [line for line in prefix_lines if line.startswith("ALPHA_DONE\t")]
alpha2 = [line for line in s2_lines if line.startswith("ALPHA_DONE\t")]
assert [int(record(line)["UNIT"]) for line in alpha1] == list(range(1, 11897))
assert [int(record(line)["UNIT"]) for line in alpha2] == list(range(11897, 14032))
assert sum(line.startswith("CANDIDATE_NUMERIC\t") for line in prefix_lines + s2_lines) == 0
totals = [line for line in s2_lines if line.startswith("TOTAL\t")]
assert len(totals) == 1 and s2_lines[-1] == "DONE"
total = record(totals[0])
assert total["START_UNIT"] == "11897" and total["LAST_COMPLETE_UNIT"] == "14031"
assert total["SEGMENT_UNITS"] == "2135" and total["SEGMENT_RAW"] == "6558720"
for name, value in COUNTERS.items():
    assert int(total[name]) == value, (name, total[name], value)
assert total["FINAL_CHECKPOINT_SHA256"] == CP_SHA

cp = CP.read_bytes()
assert digest(cp) == CP_SHA
cp_lines = cp.decode("ascii").splitlines()
assert len(cp_lines) == 3 and cp_lines[2] == "DONE"
payload, payload_sha = cp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert digest(payload.encode("ascii")) == payload_sha
cp_fields = payload.split("\t")
cp_values = dict(zip(cp_fields[2::2], cp_fields[3::2], strict=True))
assert cp_values["UNIT"] == "14031" and cp_values["NEXT_UNIT"] == "14032"
assert cp_values["CUM_RAW"] == "43103232" and cp_values["CUM_CANDIDATE_NUMERIC"] == "0"

stderr = S2ERR.read_bytes()
assert b"Exit status: 0" in stderr and b"Elapsed (wall clock) time (h:mm:ss or m:ss): 2:01.09" in stderr
assert b"Maximum resident set size (kbytes): 146688" in stderr
recovery_sha = digest(RECOVERY.read_bytes())

agg = (
    "CERTIFICATE_NUMERICAL_AGGREGATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD004\n"
    "STATUS\tCOMPLETE_ZERO_CANDIDATE\n"
    "BOUNDARY\t24T6440:a3\t24T6769:a90\n"
    "KEYS_TOUCHED\t302\nCLASS_UNITS\t14031\nRAW_PAIRS\t43103232\n"
    "INVARIANT_ALPHA_CLASSES\t14031\nBETA_COMPUTATIONS\t700\n"
    "INVERSE\t3681152\nINVERSE_ODD\t2795440\nORBIT8\t857184\nRELATOR\t142240\n"
    "B3\t0\nGENERATING\t0\nPARITY\t0\nCENTRALIZER_ORBITS\t0\nCANDIDATES\t0\n"
    "SEGMENT001_LAST_DURABLE_UNIT\t11896\nSEGMENT002_START_UNIT\t11897\nNO_REPLAY\tPASS\n"
    f"SEGMENT001_PHYSICAL_SHA256\t{S1_SHA.upper()}\nSEGMENT001_PREFIX_BYTES\t{PREFIX_BYTES}\nSEGMENT001_PREFIX_SHA256\t{PREFIX_SHA.upper()}\n"
    f"SEGMENT002_SHA256\t{S2_SHA.upper()}\nFINAL_CHECKPOINT_SHA256\t{CP_SHA.upper()}\n"
    f"RECOVERY_EVIDENCE_SHA256\t{recovery_sha.upper()}\n"
    "SEGMENT001_WALL\tEXTERNAL_1400S_BOUNDARY\nSEGMENT002_WALL\t2:01.09\n"
    "MAX_RSS_KIB\t146688\nCERTIFICATE_TEXT_CLEANUP_DEFERRED\t1\nDONE\n"
).encode("ascii")
atomic_write(AGG, agg)
agg_sha = digest(agg).upper()

marker = (
    "COMPLETE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD004\n"
    "STATUS\tCOMPLETE_ZERO_CANDIDATE\n"
    "CLASS_UNITS\t14031\nRAW_PAIRS\t43103232\nCANDIDATES\t0\n"
    f"NUMERICAL_AGGREGATE_SHA256\t{agg_sha}\nESSENTIAL_OUTPUT_SHA256\t{S2_SHA.upper()}\n"
    f"FINAL_CHECKPOINT_SHA256\t{CP_SHA.upper()}\nDONE\n"
).encode("ascii")
atomic_write(COMPLETE, marker)

progress = PROGRESS.read_text(encoding="ascii").splitlines()
assert progress[0].startswith("SHARD\tSTATUS\t")
assert not any(line.startswith("004\t") for line in progress[1:])
progress.append(
    "004\tCOMPLETE_ZERO_CANDIDATE\t24T6440:a3\t24T6769:a90\t302\t14031\t43103232"
    f"\t0\t0\t0\t0\t{agg_sha}\t{CP_SHA.upper()}"
)
progress_data = ("\n".join(progress) + "\n").encode("ascii")
atomic_write(PROGRESS, progress_data)

print("PASS SHARD004 COMPLETE UNITS=14031 RAW=43103232 CANDIDATES=0")
print(f"AGGREGATE\t{AGG.name}\tSHA256\t{agg_sha}")
print(f"COMPLETE\t{COMPLETE.name}\tSHA256\t{digest(marker).upper()}")
print(f"PROGRESS\t{PROGRESS.name}\tSHA256\t{digest(progress_data).upper()}")
