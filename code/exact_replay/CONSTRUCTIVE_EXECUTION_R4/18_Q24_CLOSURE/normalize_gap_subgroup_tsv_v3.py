"""Final GAP TSV normalizer preserving leading continuation tabs."""
from __future__ import annotations

import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
backup = HERE / "SL2_9_SUBGROUP_CLASSES_GAP_WRAPPED_ORIGINAL.tsv"
target = HERE / "SL2_9_SUBGROUP_CLASSES_RAW.tsv"
text = backup.read_text(encoding="utf-8").replace("\\\n", "").replace("\\\r\n", "")
physical = text.splitlines()
header = physical[0]
start = re.compile(r"^\d+\t\d+\t\d+\t(?:true|false)\t")
logical: list[str] = []
buffer = ""
for line in physical[1:]:
    if start.match(line):
        if buffer:
            logical.append(buffer)
        buffer = line
    else:
        if not buffer:
            raise RuntimeError(f"continuation before first row: {line!r}")
        buffer += line.lstrip(" ")
if buffer:
    logical.append(buffer)
if len(logical) != 27 or any(row.count("\t") != 7 for row in logical):
    raise RuntimeError(f"normalization failed: rows={len(logical)} tab_counts={[r.count(chr(9)) for r in logical]}")
target.write_text(header + "\n" + "\n".join(logical) + "\n", encoding="utf-8")
print(f"PASS_NORMALIZED_V3 rows={len(logical)}")
