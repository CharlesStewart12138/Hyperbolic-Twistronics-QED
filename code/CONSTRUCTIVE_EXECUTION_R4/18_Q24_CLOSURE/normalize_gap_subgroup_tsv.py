"""Normalize GAP pretty-printer continuations in the subgroup TSV."""
from __future__ import annotations

import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
source = HERE / "SL2_9_SUBGROUP_CLASSES_RAW.tsv"
backup = HERE / "SL2_9_SUBGROUP_CLASSES_GAP_WRAPPED_ORIGINAL.tsv"
if not backup.exists():
    shutil.copyfile(source, backup)

text = backup.read_text(encoding="utf-8").replace("\\\n", "").replace("\\\r\n", "")
physical = text.splitlines()
header = physical[0]
logical = []
buffer = ""
for line in physical[1:]:
    buffer = buffer + line.lstrip() if buffer else line
    if buffer.count("\t") >= 7:
        logical.append(buffer)
        buffer = ""
if buffer:
    raise RuntimeError("unterminated GAP row")
if len(logical) != 27 or any(row.count("\t") != 7 for row in logical):
    raise RuntimeError(f"normalization failed: rows={len(logical)} tab_counts={[r.count(chr(9)) for r in logical]}")
source.write_text(header + "\n" + "\n".join(logical) + "\n", encoding="utf-8")
print(f"PASS_NORMALIZED rows={len(logical)} backup={backup.name}")
