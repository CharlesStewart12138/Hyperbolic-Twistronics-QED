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
            int(fields["ORDER"]), int(fields["PARITY_MAPS"]),
            int(fields["SOLVABLE"]) if has_solvable else None,
        )
    return result


sol = load("GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt", True)
win = load("GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt", False)
lo, hi = 13929, 14218
parity = sorted(k for k in sol if lo <= k <= hi)
window = sorted(k for k in win if lo <= k <= hi)
solvable = [k for k in parity if sol[k][2] == 1]
nonsolvable = [k for k in parity if sol[k][2] == 0]
excluded = [k for k in window if k not in set(parity)]
assert window == list(range(lo, hi + 1)) and len(window) == 290
assert len(parity) == 287 and len(solvable) == 269
assert nonsolvable == list(range(13985, 14003))
assert excluded == [14050, 14051, 14052]

segments = [
    ("S1", 13929, 13984, "pc", 56, 56, [13950, 13975]),
    ("S2", 13985, 14002, "native", 18, 18, [14000]),
    ("S3", 14003, 14218, "pc", 216, 213, [14025, 14050, 14075, 14100, 14125, 14150, 14175, 14200]),
]
assert segments[0][1] == lo and segments[-1][2] == hi
assert all(segments[i][2] + 1 == segments[i + 1][1] for i in range(len(segments) - 1))
for _, start, end, method, expected_window, expected_parity, scans in segments:
    pkeys = [k for k in parity if start <= k <= end]
    wkeys = [k for k in window if start <= k <= end]
    assert len(pkeys) == expected_parity and len(wkeys) == expected_window
    assert scans == [k for k in range(start, end + 1) if k % 25 == 0]
    assert all(sol[k][2] == (1 if method == "pc" else 0) for k in pkeys)

records = [
    "CERTIFICATE_ROUTING\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD21",
    "STATUS\tSEALED_EXACT_DISJOINT_ROUTING", "DEGREE\t24", "DATABASE\t25000", "RANGE\t13929\t14218",
    "ORDER_WINDOW\t290", "PARITY_KEYS\t287", "SOLVABLE_PARITY_KEYS\t269", "NONSOLVABLE_PARITY_KEYS\t18",
    "SEGMENT\tS1\tRANGE\t13929\t13984\tMETHOD\tpc\tORDER_WINDOW\t56\tPARITY\t56\tSCAN_KEYS\t13950,13975",
    "SEGMENT\tS2\tRANGE\t13985\t14002\tMETHOD\tnative\tORDER_WINDOW\t18\tPARITY\t18\tSCAN_KEYS\t14000",
    "SEGMENT\tS3\tRANGE\t14003\t14218\tMETHOD\tpc\tORDER_WINDOW\t216\tPARITY\t213\tSCAN_KEYS\t14025,14050,14075,14100,14125,14150,14175,14200",
    "NONSOLVABLE_KEYS\t" + ",".join(map(str, nonsolvable)),
    "PARITY_EXCLUDED_WINDOW_KEYS\t14050,14051,14052",
    "SEGMENT_RANGES_DISJOINT_CONTIGUOUS\tPASS", "PARITY_KEY_UNION_EXACT\tPASS",
    "SCOPE\tRouting only; no automorphism group or seed predicate is computed.", "DONE",
]
output = base / "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD21_ROUTING_GPT56SOL.txt"
if output.exists():
    raise FileExistsError(output)
output.write_text("\n".join(records) + "\n", encoding="utf-8", newline="\n")
print("PASS shard21 routing window=290 parity=287 solvable=269 nonsolvable=18 segments=3")
