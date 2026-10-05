"""Add the xcolor dependency to the already sanitized clean PDF master."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "tmp" / "pdfs" / "r5_theorem_clean"
source = (BUILD / "R5_OPERATOR_CLOSURE_THEOREM.tex").read_text(encoding="utf-8")
source = source.replace(
    r"\usepackage{amsmath,amssymb,amsthm,booktabs,array,hyperref,microtype}",
    r"\usepackage{xcolor}" + "\n" +
    r"\usepackage{amsmath,amssymb,amsthm,booktabs,array,hyperref,microtype}",
)
(BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V2.tex").write_text(source, encoding="utf-8")
print(BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V2.tex")
