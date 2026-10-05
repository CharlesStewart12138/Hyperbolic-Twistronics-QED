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
lo, hi = 15441, 15576
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
scans = [k for k in range(lo, hi + 1) if k % 25 == 0]
assert window == list(range(lo, hi + 1)) and len(window) == 136
assert parity == [k for k in window if k != 15574] and len(parity) == 135
assert all(sol[k][2] == 1 for k in parity)
assert scans == [15450, 15475, 15500, 15525, 15550, 15575]

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD29",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING", "DEGREE\t24", "DATABASE\t25000", "RANGE\t15441\t15576",
    "ORDER_WINDOW\t136", "PARITY_KEYS\t135", "SOLVABLE_PARITY_KEYS\t135", "NONSOLVABLE_PARITY_KEYS\t0",
    "SEGMENT\tS1\tRANGE\t15441\t15576\tMETHOD\tpc\tORDER_WINDOW\t136\tPARITY\t135\tSCAN_KEYS\t15450,15475,15500,15525,15550,15575",
    "NATIVE_SEGMENTS\tnone", "PARITY_EXCLUDED_WINDOW_KEYS\t15574",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "PARITY_KEY_UNION_EXACT\tPASS",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.", "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD29_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard29 routing window=136 parity=135 solvable=135 nonsolvable=0 excluded=15574 segments=1")
