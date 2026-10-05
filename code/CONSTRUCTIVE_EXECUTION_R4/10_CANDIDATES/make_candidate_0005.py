"""Generate candidate 0005 from the audited D2 candidate template."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=(HERE/"build_candidate_0004.py").read_text(encoding="utf-8")
source=source.replace("CAND-R4-0004","CAND-R4-0005").replace("candidate 0004","candidate 0005").replace("candidate0004","candidate0005")
source=source.replace("ROWS = (15, 19)","ROWS = (6, 9)")
source=source.replace("P2C2-C8-D2-358B92D9F5CC8E4B","P2C2-C8-D2-1D16194A8DBB81E2")
source=source.replace('"Parent Candidate": "CAND-R4-0003_STRICT_REFINEMENT"','"Parent Candidate": "CAND-R4-0002_NONNESTED_D2_RESTART"')
source=source.replace('"parent_candidate": "CAND-R4-0003"','"parent_candidate": "CAND-R4-0002"')
source=source.replace("strict kernel refinement induced by the D2 row space containing the D1 row space","nonnested strict refinement of CAND-R4-0002 using D2 row space <6,9>")
source=source.replace("C8-stable class-2 p=2 D2 extension","C8-stable class-2 p=2 nonnested D2 branch")
source=source.replace("C8-stable class-2 D2 separator","C8-stable class-2 nonnested D2 separator")
(HERE/"build_candidate_0005.py").write_text(source,encoding="utf-8",newline="\n")

verify=(HERE/"verify_candidate_0004.py").read_text(encoding="utf-8").replace("0004","0005")
(HERE/"verify_candidate_0005.py").write_text(verify,encoding="utf-8",newline="\n")
