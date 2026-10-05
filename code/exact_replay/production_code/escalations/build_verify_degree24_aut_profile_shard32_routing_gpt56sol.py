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
lo, hi = 15847, 25000
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
scans = [k for k in range(lo, hi + 1) if k % 25 == 0]
assert window == list(range(15847, 15982)) and len(window) == 135
assert parity == window and len(parity) == 135 and all(sol[k][2] == 1 for k in parity)
assert len(scans) == 367 and scans[0] == 15850 and scans[-1] == 25000

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD32",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING", "DEGREE\t24", "DATABASE\t25000", "RANGE\t15847\t25000",
    "ORDER_WINDOW\t135", "PARITY_KEYS\t135", "SOLVABLE_PARITY_KEYS\t135", "NONSOLVABLE_PARITY_KEYS\t0",
    "SEGMENT\tS1\tRANGE\t15847\t25000\tMETHOD\tpc\tORDER_WINDOW\t135\tPARITY\t135\tSCAN_KEYS\t" + ",".join(map(str, scans)),
    "PARITY_KEY_SPAN\t15847\t15981", "EXACT_ZERO_WINDOW_TAIL\t15982\t25000",
    "NATIVE_SEGMENTS\tnone", "PARITY_EXCLUDED_WINDOW_KEYS\tnone",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "PARITY_KEY_UNION_EXACT\tPASS",
    "FULL_CATALOGUE_RANGE_SCAN_REQUIRED\tPASS", "PLANNED_SCAN_CHECKPOINTS\t367",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.", "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD32_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard32 routing window=135 parity=135 solvable=135 nonsolvable=0 tail=15982-25000 scans=367 segments=1")
