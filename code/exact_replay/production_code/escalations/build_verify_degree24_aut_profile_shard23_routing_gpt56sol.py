from __future__ import annotations

import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def load(name: str, has_solvable: bool) -> dict[int, tuple[int, int, int | None]]:
    result = {}
    for line in (base / name).read_text(encoding="utf-8").splitlines():
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        parts = line.split("\t")
        fields = dict(zip(parts[2::2], parts[3::2]))
        result[int(match.group(1))] = (int(fields["ORDER"]), int(fields["PARITY_MAPS"]), int(fields["SOLVABLE"]) if has_solvable else None)
    return result


sol = load("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt", True)
win = load("GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt", False)
lo, hi = 14516, 14765
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
solvable = [k for k in parity if sol[k][2] == 1]
nonsolvable = [k for k in parity if sol[k][2] == 0]
excluded = [k for k in window if k not in set(parity)]
assert window == list(range(lo, hi + 1)) and len(window) == 250
assert len(parity) == 248 and len(solvable) == 220
assert nonsolvable == list(range(14607, 14635))
assert excluded == [14519, 14537]
segments = [
    ("S1", 14516, 14606, "pc", 91, 89, [14525, 14550, 14575, 14600]),
    ("S2", 14607, 14634, "native", 28, 28, [14625]),
    ("S3", 14635, 14765, "pc", 131, 131, [14650, 14675, 14700, 14725, 14750]),
]
assert segments[0][1] == lo and segments[-1][2] == hi
assert all(segments[i][2] + 1 == segments[i + 1][1] for i in range(2))
for _, start, end, method, expected_window, expected_parity, scans in segments:
    pkeys = [k for k in parity if start <= k <= end]
    wkeys = [k for k in window if start <= k <= end]
    assert len(pkeys) == expected_parity and len(wkeys) == expected_window
    assert scans == [k for k in range(start, end + 1) if k % 25 == 0]
    assert all(sol[k][2] == (1 if method == "pc" else 0) for k in pkeys)

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD23",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING", "DEGREE\t24", "DATABASE\t25000", "RANGE\t14516\t14765",
    "ORDER_WINDOW\t250", "PARITY_KEYS\t248", "SOLVABLE_PARITY_KEYS\t220", "NONSOLVABLE_PARITY_KEYS\t28",
    "SEGMENT\tS1\tRANGE\t14516\t14606\tMETHOD\tpc\tORDER_WINDOW\t91\tPARITY\t89\tSCAN_KEYS\t14525,14550,14575,14600",
    "SEGMENT\tS2\tRANGE\t14607\t14634\tMETHOD\tnative\tORDER_WINDOW\t28\tPARITY\t28\tSCAN_KEYS\t14625",
    "SEGMENT\tS3\tRANGE\t14635\t14765\tMETHOD\tpc\tORDER_WINDOW\t131\tPARITY\t131\tSCAN_KEYS\t14650,14675,14700,14725,14750",
    "NONSOLVABLE_KEYS\t" + ",".join(map(str, nonsolvable)), "PARITY_EXCLUDED_WINDOW_KEYS\t14519,14537",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "PARITY_KEY_UNION_EXACT\tPASS",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.", "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD23_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard23 routing window=250 parity=248 solvable=220 nonsolvable=28 segments=3")
