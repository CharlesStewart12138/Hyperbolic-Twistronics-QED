"""Prepare the final layout master with controlled emergency line stretch."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "tmp" / "pdfs" / "r5_theorem_clean"
source = (BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V2.tex").read_text(encoding="utf-8")
source = source.replace(
    r"\setlength{\parskip}{0.45em}",
    r"\setlength{\parskip}{0.45em}" + "\n" +
    r"\setlength{\emergencystretch}{3em}",
)
(BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V3.tex").write_text(source, encoding="utf-8")
print(BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V3.tex")
