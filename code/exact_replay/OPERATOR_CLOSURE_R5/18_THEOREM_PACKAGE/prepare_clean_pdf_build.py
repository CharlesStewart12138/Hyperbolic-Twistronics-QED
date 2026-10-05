"""Prepare a clean TeX build tree without modifying frozen theorem modules."""

from __future__ import annotations

import shutil
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent.parent
BUILD = ROOT / "tmp" / "pdfs" / "r5_theorem_clean"
OUTPUT = ROOT / "output" / "pdf"
BUILD.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)

modules = (
    "R5_DEFINITIONS.tex", "R5_MAIN_THEOREM.tex",
    "R5_DOUBLE_COSET_THEOREM.tex", "R5_NORMALIZER_THEOREM.tex",
    "R5_COMMENSURATOR_THEOREM.tex", "R5_GENERIC_CASE.tex",
    "R5_EXISTENCE_ATTAINMENT.tex", "R5_FINITE_ALGORITHM.tex",
    "R5_TIE_REGULARITY.tex", "R5_C2_PARAMETER_THEOREM.tex",
    "R5_OPERATOR_DESCENT.tex", "R5_PERIODICITY_THEOREM.tex",
    "R5_COUNTEREXAMPLES.tex", "R5_PRIOR_ART.tex",
)

text_replacements = {
    "01_OPERATOR_SEMANTICS/FROZEN_OPERATOR_SEMANTICS.md": r"01\_OPERATOR\_SEMANTICS/FROZEN\_OPERATOR\_SEMANTICS.md",
    "R5_DEFINITIONS": r"R5\_DEFINITIONS",
    "R5_COMMENSURATOR_THEOREM": r"R5\_COMMENSURATOR\_THEOREM",
    "R5_GENERIC_CASE": r"R5\_GENERIC\_CASE",
    "R5_NORMALIZER_THEOREM": r"R5\_NORMALIZER\_THEOREM",
    "GLOBAL_INTERLAYER_SUPPORT_R5": r"GLOBAL\_INTERLAYER\_SUPPORT\_R5",
    "GLOBAL_OPERATOR_R5": r"GLOBAL\_OPERATOR\_R5",
}

for name in modules:
    text = (PACKAGE / name).read_text(encoding="utf-8")
    for old, new in text_replacements.items():
        text = text.replace(old, new)
    (BUILD / name).write_text(text, encoding="utf-8")

master = r"""\documentclass[11pt]{article}
\usepackage[a4paper,margin=24mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,booktabs,array,hyperref,microtype}
\hypersetup{colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!55!black}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}
\title{R5 Global Operator Closure:\\Double Cosets, Descent, and the Generic No-Go Theorem}
\author{}
\date{15 September 2026}
\begin{document}
\maketitle
\begin{abstract}
We audit the frozen two-sided lift minimum for the Bolza bilayer. Same-cover
descent is equivalent to normalization, a finite common cover is equivalent to
commensuration, and every noncommensurator double coset is dense. The generic
nearest-image infimum is zero and generally not attained. This rules out the
fixed same-quotient periodic operator and its parameter Hessians while leaving
the infinite and certified local models intact.
\end{abstract}
\tableofcontents
\input{R5_DEFINITIONS.tex}
\input{R5_MAIN_THEOREM.tex}
\input{R5_DOUBLE_COSET_THEOREM.tex}
\input{R5_NORMALIZER_THEOREM.tex}
\input{R5_COMMENSURATOR_THEOREM.tex}
\input{R5_GENERIC_CASE.tex}
\input{R5_EXISTENCE_ATTAINMENT.tex}
\input{R5_FINITE_ALGORITHM.tex}
\input{R5_TIE_REGULARITY.tex}
\input{R5_C2_PARAMETER_THEOREM.tex}
\input{R5_OPERATOR_DESCENT.tex}
\input{R5_PERIODICITY_THEOREM.tex}
\input{R5_COUNTEREXAMPLES.tex}
\input{R5_PRIOR_ART.tex}
\begin{thebibliography}{9}
\bibitem{Moore1966} C. C. Moore, \emph{Ergodicity of flows on homogeneous spaces},
Amer. J. Math. 88 (1966), 154--178, doi:10.2307/2373052.
\bibitem{Ratner1991} M. Ratner, \emph{Raghunathan's topological conjecture and
distributions of unipotent flows}, Duke Math. J. 63 (1991), 235--280,
doi:10.1215/S0012-7094-91-06311-8.
\bibitem{KSV} M. Katz, M. Schaps, and U. Vishne, \emph{Bolza quaternion order
and asymptotics of systoles along congruence subgroups}, J. Number Theory 144
(2014), 410--432; arXiv:1405.5454.
\end{thebibliography}
\end{document}
"""
(BUILD / "R5_OPERATOR_CLOSURE_THEOREM.tex").write_text(master, encoding="utf-8")
print(BUILD)
print(OUTPUT)
