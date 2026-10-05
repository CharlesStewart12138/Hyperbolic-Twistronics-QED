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
        result[int(match.group(1))] = (
            int(fields["ORDER"]),
            int(fields["PARITY_MAPS"]),
            int(fields["SOLVABLE"]) if has_solvable else None,
        )
    return result


sol = load("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt", True)
win = load("GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt", False)
lo, hi = 13517, 13721
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
excluded = [k for k in window if k not in set(parity)]
scans = [k for k in range(lo, hi + 1) if k % 25 == 0]
assert window == list(range(lo, hi + 1)) and len(window) == 205
assert parity == window and len(parity) == 205
assert all(sol[k][2] == 1 for k in parity)
assert excluded == []
assert scans == [13525, 13550, 13575, 13600, 13625, 13650, 13675, 13700]

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD19",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING",
    "DEGREE\t24",
    "DATABASE\t25000",
    "RANGE\t13517\t13721",
    "ORDER_WINDOW\t205",
    "PARITY_KEYS\t205",
    "SOLVABLE_PARITY_KEYS\t205",
    "NONSOLVABLE_PARITY_KEYS\t0",
    "SEGMENT\tS1\tRANGE\t13517\t13721\tMETHOD\tpc\tORDER_WINDOW\t205\tPARITY\t205\tSCAN_KEYS\t13525,13550,13575,13600,13625,13650,13675,13700",
    "NATIVE_SEGMENTS\tnone",
    "PARITY_EXCLUDED_WINDOW_KEYS\tnone",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS",
    "PARITY_KEY_UNION_EXACT\tPASS",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.",
    "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD19_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard19 routing window=205 parity=205 solvable=205 nonsolvable=0 segments=1")
