"""Final PDF layout refinements in the disposable clean build tree."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "tmp" / "pdfs" / "r5_theorem_clean"

double_coset = (BUILD / "R5_DOUBLE_COSET_THEOREM.tex").read_text(encoding="utf-8")
double_coset = double_coset.replace(
    r"R5\_COMMENSURATOR\_THEOREM", "the commensurator theorem below"
).replace(r"R5\_GENERIC\_CASE", "the generic-case theorem below")
(BUILD / "R5_DOUBLE_COSET_THEOREM.tex").write_text(double_coset, encoding="utf-8")

periodicity = (BUILD / "R5_PERIODICITY_THEOREM.tex").read_text(encoding="utf-8")
periodicity = periodicity.replace(
    r"R5\_NORMALIZER\_THEOREM", "the normalizer theorem above"
).replace(
    r"\begin{tabular}{ll}",
    r"\begin{tabular}{p{0.37\linewidth}p{0.56\linewidth}}",
)
(BUILD / "R5_PERIODICITY_THEOREM.tex").write_text(periodicity, encoding="utf-8")

master = (BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V3.tex").read_text(encoding="utf-8")
(BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V4.tex").write_text(master, encoding="utf-8")
print(BUILD / "R5_OPERATOR_CLOSURE_THEOREM_V4.tex")
