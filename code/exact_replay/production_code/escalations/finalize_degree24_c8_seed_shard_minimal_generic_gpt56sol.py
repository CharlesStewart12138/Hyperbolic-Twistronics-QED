#!/usr/bin/env python3
"""Compute-first minimal closure for one completed degree-24 seed shard."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path


B = Path(__file__).resolve().parent
PLAN = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv"
PROGRESS = B / "GAP_TRANSITIVE_DEGREE24_C8_SEED_PROGRESS_GPT56SOL.tsv"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


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


def pairs(parts: list[str], start: int) -> dict[str, str]:
    assert (len(parts) - start) % 2 == 0
    result: dict[str, str] = {}
    for i in range(start, len(parts), 2):
        assert parts[i] not in result
        result[parts[i]] = parts[i + 1]
    return result


parser = argparse.ArgumentParser()
parser.add_argument("--shard", type=int, required=True)
args = parser.parse_args()
shard = args.shard
tag = f"{shard:03d}"

summary: dict[str, str] | None = None
work: list[dict[str, str]] = []
for line in PLAN.read_text(encoding="ascii").splitlines():
    parts = line.split("\t")
    if parts[:2] == ["SHARD", str(shard)]:
        summary = pairs(parts, 2)
    elif parts[:2] == ["WORK", str(shard)]:
        work.append(pairs(parts, 2))
assert summary is not None and len(work) == int(summary["KEYS_TOUCHED"])
expected: list[tuple[int, int]] = []
expected_raw = 0
for row in work:
    key = int(row["KEY"])
    first = int(row["ALPHA_FIRST"])
    last = int(row["ALPHA_LAST"])
    order = int(row["ORDER"])
    expected.extend((key, alpha) for alpha in range(first, last + 1))
    expected_raw += order * (last - first + 1)
total_units = int(summary["CLASS_UNITS"])
total_raw = int(summary["RAW_PAIRS"])
assert len(expected) == total_units and expected_raw == total_raw

pattern = f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_SEGMENT*_UNIT*_POSTVERIFY_V7_GPT56SOL.txt"
outputs = []
for path in B.glob(pattern):
    match = re.search(r"_SEGMENT([0-9]+)_", path.name)
    assert match
    outputs.append((int(match.group(1)), path))
outputs.sort()
assert outputs and len({segment for segment, _ in outputs}) == len(outputs)

committed: dict[int, tuple[int, int]] = {}
candidates: set[str] = set()
terminal_lines: list[str] = []
output_facts: list[tuple[Path, int, str]] = []
for segment, path in outputs:
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    assert lines and lines[0].startswith("CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD" + tag)
    pending: dict[int, tuple[int, int]] = {}
    for line in lines:
        if line.startswith("ALPHA_DONE\t"):
            values = pairs(line.split("\t"), 1)
            pending[int(values["UNIT"])] = (int(values["KEY"].removeprefix("24T")), int(values["ALPHA"]))
        elif line.startswith("CHECKPOINT_COMMITTED\t"):
            values = pairs(line.split("\t"), 1)
            unit = int(values["UNIT"])
            assert unit in pending
            if unit in committed:
                assert committed[unit] == pending[unit]
            else:
                committed[unit] = pending[unit]
        elif line.startswith("CANDIDATE_NUMERIC\t"):
            candidates.add(line)
        elif line.startswith("TOTAL\t"):
            terminal_lines.append(line)
    output_facts.append((path, len(data), digest(data)))

assert sorted(committed) == list(range(1, total_units + 1))
assert [committed[unit] for unit in range(1, total_units + 1)] == expected
assert len(terminal_lines) == 1
terminal = pairs(terminal_lines[0].split("\t"), 1)
assert int(terminal["LAST_COMPLETE_UNIT"]) == total_units
assert int(terminal["CUM_UNITS"]) == total_units
assert int(terminal["CUM_RAW"]) == total_raw
assert int(terminal["INVARIANT_ALPHA_CLASSES"]) == total_units
assert int(terminal["CANDIDATE_NUMERIC"]) == len(candidates)

checkpoint = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CHECKPOINT_GPT56SOL.txt"
cp_data = checkpoint.read_bytes()
cp_sha = digest(cp_data)
cp_lines = cp_data.decode("ascii").splitlines()
assert len(cp_lines) == 3 and cp_lines[0].endswith("SHARD" + tag) and cp_lines[2] == "DONE"
payload, payload_sha = cp_lines[1].rsplit("\tPAYLOAD_SHA256\t", 1)
assert digest(payload.encode("ascii")) == payload_sha.upper()
cp_parts = payload.split("\t")
assert cp_parts[:2] == ["SHARD", tag]
cp = pairs(cp_parts, 2)
assert int(cp["UNIT"]) == total_units and int(cp["NEXT_UNIT"]) == total_units + 1
assert int(cp["CUM_RAW"]) == total_raw
assert int(cp["CUM_CANDIDATE_NUMERIC"]) == len(candidates)
assert terminal["FINAL_CHECKPOINT_SHA256"].upper() == cp_sha

metrics = {
    "INVARIANT_ALPHA_CLASSES": total_units,
    "BETA_COMPUTATIONS": int(terminal["BETA_COMPUTATIONS"]),
    "INVERSE": int(terminal["INVERSE"]),
    "INVERSE_ODD": int(terminal["INVERSE_ODD"]),
    "ORBIT8": int(terminal["ORBIT8"]),
    "RELATOR": int(terminal["RELATOR"]),
    "B3": int(terminal["B3"]),
    "GENERATING": int(terminal["GENERATE"]),
    "PARITY": int(terminal["PARITY"]),
    "CENTRALIZER_ORBITS": int(terminal["CENTRALIZER_ORBITS"]),
    "CANDIDATES": int(terminal["CANDIDATE_NUMERIC"]),
}
status = "COMPLETE_ZERO_CANDIDATE" if metrics["CANDIDATES"] == 0 else "COMPLETE_WITH_CANDIDATE"
first = f"24T{summary['FIRST_KEY']}:a{summary['FIRST_ALPHA']}"
last = f"24T{summary['LAST_KEY']}:a{summary['LAST_ALPHA']}"
agg_lines = [
    f"CERTIFICATE_NUMERICAL_AGGREGATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD{tag}",
    f"STATUS\t{status}", f"BOUNDARY\t{first}\t{last}",
    f"KEYS_TOUCHED\t{summary['KEYS_TOUCHED']}", f"CLASS_UNITS\t{total_units}",
    f"RAW_PAIRS\t{total_raw}",
]
agg_lines.extend(f"{name}\t{value}" for name, value in metrics.items())
agg_lines.append(f"SEGMENTS\t{len(outputs)}")
for segment, (path, size, sha) in zip((x[0] for x in outputs), output_facts, strict=True):
    agg_lines.append(f"SEGMENT\t{segment:03d}\tFILE\t{path.name}\tBYTES\t{size}\tSHA256\t{sha}")
agg_lines += [f"FINAL_CHECKPOINT_SHA256\t{cp_sha}", "CERTIFICATE_TEXT_CLEANUP_DEFERRED\t1", "DONE", ""]
agg_data = "\n".join(agg_lines).encode("ascii")
agg = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_CANONICAL_NUMERICAL_AGGREGATE_GPT56SOL.txt"
atomic_write(agg, agg_data)
agg_sha = digest(agg_data)

if candidates:
    candidate_file = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_PENDING_CANDIDATES_GPT56SOL.tsv"
    atomic_write(candidate_file, ("\n".join(sorted(candidates)) + "\n").encode("ascii"))

marker_data = (
    f"COMPLETE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD{tag}\n"
    f"STATUS\t{status}\nCLASS_UNITS\t{total_units}\nRAW_PAIRS\t{total_raw}\n"
    f"CANDIDATES\t{metrics['CANDIDATES']}\nNUMERICAL_AGGREGATE_SHA256\t{agg_sha}\n"
    f"ESSENTIAL_OUTPUT_SHA256\t{output_facts[-1][2]}\nFINAL_CHECKPOINT_SHA256\t{cp_sha}\nDONE\n"
).encode("ascii")
marker = B / f"GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD{tag}_COMPLETE_GPT56SOL.txt"
atomic_write(marker, marker_data)

progress = PROGRESS.read_text(encoding="ascii").splitlines()
assert not any(line.startswith(tag + "\t") for line in progress[1:])
progress.append(
    f"{tag}\t{status}\t{first}\t{last}\t{summary['KEYS_TOUCHED']}\t{total_units}\t{total_raw}"
    f"\t{metrics['B3']}\t{metrics['GENERATING']}\t{metrics['CENTRALIZER_ORBITS']}\t{metrics['CANDIDATES']}"
    f"\t{agg_sha}\t{cp_sha}"
)
progress_data = ("\n".join(progress) + "\n").encode("ascii")
atomic_write(PROGRESS, progress_data)

print(f"PASS SHARD={tag} STATUS={status} UNITS={total_units} RAW={total_raw} CANDIDATES={metrics['CANDIDATES']}")
print(f"AGGREGATE={agg.name} SHA256={agg_sha}")
print(f"COMPLETE={marker.name} SHA256={digest(marker_data)}")
print(f"PROGRESS_SHA256={digest(progress_data)}")
