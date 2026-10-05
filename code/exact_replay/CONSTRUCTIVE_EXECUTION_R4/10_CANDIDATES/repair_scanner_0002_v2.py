"""Repair the radix constant in the preserved candidate-0002 scanner v1."""

from pathlib import Path


HERE = Path(__file__).resolve().parent
source = (HERE / "scan_candidate_0002_axis6.cpp").read_text(encoding="utf-8")
old = "code+=scale*digit;scale*=5;"
if source.count(old) != 1:
    raise RuntimeError("unexpected candidate-0002 radix source")
source = source.replace(old, "code+=scale*digit;scale*=p;")
(HERE / "scan_candidate_0002_axis6_v2.cpp").write_text(source, encoding="utf-8", newline="\n")
