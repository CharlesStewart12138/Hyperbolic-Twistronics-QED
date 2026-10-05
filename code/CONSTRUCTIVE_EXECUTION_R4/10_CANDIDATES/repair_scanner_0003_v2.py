"""Repair the omitted [b2,a2]=[b1,a1] projected cocycle term."""

from pathlib import Path


HERE = Path(__file__).resolve().parent
source = (HERE / "scan_candidate_0003_axis6.cpp").read_text(encoding="utf-8")
old = "  z^=((left&2U)&&(right&1U));\n"
new = "  z^=((left&2U)&&(right&1U));\n  z^=((left&8U)&&(right&4U));  // [b2,a2]=[b1,a1]\n"
if source.count(old) != 1:
    raise RuntimeError("candidate-0003 cocycle repair site did not match")
source = source.replace(old, new)
source = source.replace("CAND-R4-0003-axis6-early-exit", "CAND-R4-0003-axis6-early-exit-v2")
(HERE / "scan_candidate_0003_axis6_v2.cpp").write_text(source, encoding="utf-8", newline="\n")
