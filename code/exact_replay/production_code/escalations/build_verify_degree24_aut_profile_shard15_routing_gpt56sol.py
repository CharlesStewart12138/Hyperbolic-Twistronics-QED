from __future__ import annotations

import re
import sys
from pathlib import Path


base = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def load(name: str, solvability: bool) -> dict[int, tuple[int, int, int | None]]:
    result: dict[int, tuple[int, int, int | None]] = {}
    for line in (base / name).read_text(encoding="utf-8").splitlines():
        match = re.match(r"^ENTRY\t24T(\d+)\t", line)
        if not match:
            continue
        parts = line.split("\t")
        fields = dict(zip(parts[2::2], parts[3::2]))
        key = int(match.group(1))
        result[key] = (int(fields["ORDER"]), int(fields["PARITY_MAPS"]), int(fields["SOLVABLE"]) if solvability else None)
    return result


sol = load("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt", True)
win = load("GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt", False)
lo, hi = 12596, 12887
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
solvable = [k for k in parity if sol[k][2] == 1]
nonsolvable = [k for k in parity if sol[k][2] == 0]
excluded = [k for k in window if k not in set(parity)]
assert len(window) == 292
assert len(parity) == 285
assert len(solvable) == 276
assert nonsolvable == list(range(12613, 12622))
assert excluded == [12598, 12599, 12665, 12733, 12854, 12859, 12860]

segments = [
    ("S1", 12596, 12612, "pc", 17, 15, [12600]),
    ("S2", 12613, 12621, "native", 9, 9, []),
    ("S3", 12622, 12887, "pc", 266, 261, [12625, 12650, 12675, 12700, 12725, 12750, 12775, 12800, 12825, 12850, 12875]),
]
assert segments[0][1] == lo and segments[-1][2] == hi
assert all(segments[i][2] + 1 == segments[i + 1][1] for i in range(len(segments) - 1))
for label, start, end, method, expected_window, expected_parity, scan_keys in segments:
    keys = [k for k in parity if start <= k <= end]
    wkeys = [k for k in window if start <= k <= end]
    assert len(keys) == expected_parity
    assert len(wkeys) == expected_window
    assert [k for k in range(start, end + 1) if k % 25 == 0] == scan_keys
    if method == "pc":
        assert all(sol[k][2] == 1 for k in keys)
    else:
        assert all(sol[k][2] == 0 for k in keys)

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD15",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING",
    "DEGREE\t24",
    "DATABASE\t25000",
    "RANGE\t12596\t12887",
    "ORDER_WINDOW\t292",
    "PARITY_KEYS\t285",
    "SOLVABLE_PARITY_KEYS\t276",
    "NONSOLVABLE_PARITY_KEYS\t9",
    "SEGMENT\tS1\tRANGE\t12596\t12612\tMETHOD\tpc\tORDER_WINDOW\t17\tPARITY\t15\tSCAN_KEYS\t12600",
    "SEGMENT\tS2\tRANGE\t12613\t12621\tMETHOD\tnative\tORDER_WINDOW\t9\tPARITY\t9\tSCAN_KEYS\tnone",
    "SEGMENT\tS3\tRANGE\t12622\t12887\tMETHOD\tpc\tORDER_WINDOW\t266\tPARITY\t261\tSCAN_KEYS\t12625,12650,12675,12700,12725,12750,12775,12800,12825,12850,12875",
    "NONSOLVABLE_KEYS\t12613,12614,12615,12616,12617,12618,12619,12620,12621",
    "PARITY_EXCLUDED_WINDOW_KEYS\t12598,12599,12665,12733,12854,12859,12860",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS",
    "PARITY_KEY_UNION_EXACT\tPASS",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.",
    "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD15_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard15 routing window=292 parity=285 solvable=276 nonsolvable=9 segments=3")
