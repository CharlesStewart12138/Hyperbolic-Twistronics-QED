from __future__ import annotations

import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def load(names: list[str], has_solvable: bool) -> dict[int, tuple[int, int, int | None]]:
    result: dict[int, tuple[int, int, int | None]] = {}
    for name in names:
        for line in (base / name).read_text(encoding="utf-8").splitlines():
            match = re.match(r"^ENTRY\t24T(\d+)\t", line)
            if not match:
                continue
            key = int(match.group(1))
            parts = line.split("\t")
            fields = dict(zip(parts[2::2], parts[3::2]))
            if key in result:
                raise AssertionError(f"duplicate sealed key 24T{key}")
            result[key] = (int(fields["ORDER"]), int(fields["PARITY_MAPS"]), int(fields["SOLVABLE"]) if has_solvable else None)
    return result


sol = load([
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt",
], True)
win = load([
    "GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt",
    "GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt",
], False)
lo, hi = 13098, 13302
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
scans = [k for k in range(lo, hi + 1) if k % 25 == 0]
assert parity == list(range(lo, hi + 1))
assert window == parity
assert len(parity) == 205
assert all(sol[k][2] == 1 for k in parity)
assert scans == [13100, 13125, 13150, 13175, 13200, 13225, 13250, 13275, 13300]

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD17",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING", "DEGREE\t24", "DATABASE\t25000", "RANGE\t13098\t13302",
    "ORDER_WINDOW\t205", "PARITY_KEYS\t205", "SOLVABLE_PARITY_KEYS\t205", "NONSOLVABLE_PARITY_KEYS\t0",
    "SEGMENT\tS1\tRANGE\t13098\t13302\tMETHOD\tpc\tORDER_WINDOW\t205\tPARITY\t205\tSCAN_KEYS\t13100,13125,13150,13175,13200,13225,13250,13275,13300",
    "NATIVE_SEGMENTS\tnone", "PARITY_EXCLUDED_WINDOW_KEYS\tnone",
    "SEALED_MAP_SPLICE\t10568..13274 plus 13275..25000; disjoint at 13274/13275",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "PARITY_KEY_UNION_EXACT\tPASS",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.", "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD17_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard17 routing window=205 parity=205 solvable=205 nonsolvable=0 segments=1 mapSlices=2")
