"""Permit the projectively equivalent overall trace sign in scanner replay."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=(HERE/"finalize_global_candidate_generic.py").read_text(encoding="utf-8")
old='    if int(row["exponent"])!=a[0] or scanner_coeffs!=tuple(a[1:5]): raise RuntimeError("scanner trace mismatch")\n'
new='    canonical_coeffs=tuple(a[1:5]); projective_coeffs={canonical_coeffs,tuple(-value for value in canonical_coeffs)}\n    if int(row["exponent"])!=a[0] or scanner_coeffs not in projective_coeffs: raise RuntimeError("scanner trace mismatch modulo M~-M")\n'
if source.count(old)!=1: raise RuntimeError("generic finalizer repair site mismatch")
source=source.replace(old,new)
(HERE/"finalize_global_candidate_generic_v2.py").write_text(source,encoding="utf-8",newline="\n")
