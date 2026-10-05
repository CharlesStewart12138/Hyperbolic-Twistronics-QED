"""Independent replay for a standard-named globally rejected R4 candidate."""
from __future__ import annotations
import csv,hashlib,importlib,json,sys
from pathlib import Path
import sympy as sp
from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX,enumerate_ball,field_to_sympy,matrix_from_word
ROOT=Path(__file__).resolve().parents[2]
R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4"

def main(cid):
 serial=cid.rsplit("-",1)[1]
 c=importlib.import_module(f"CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_{serial}")
 path=R4/"10_CANDIDATES"/f"{cid}.certificate.json"
 data=path.read_bytes(); cert=json.loads(data); w=cert["global_failure_witness"]; word=tuple(w["canonical_word"])
 geom=matrix_from_word(word); payload=json.dumps(projective_key(geom),separators=(",",":"))
 tr=sp.re(field_to_sympy(geom[0])).expand(); delta=sp.expand(tr**2-(2405+1700*sp.sqrt(2))**2)
 elements=c.enumerate_image(); ball=enumerate_ball(3)
 D=R4/"02_DANGEROUS_SETS"/"DANGEROUS_SET_REGISTRY.tsv"; W=R4/"09_CEGAR"/"WITNESS_LEDGER.tsv"
 with D.open(encoding="utf-8",newline="") as h: dr=list(csv.DictReader(h,delimiter="\t"))
 with W.open(encoding="utf-8",newline="") as h: wr=list(csv.DictReader(h,delimiter="\t"))
 checks={"certificate_sha256":hashlib.sha256(data).hexdigest().upper(),"classification":cert["classification"]=="REJECTED_GLOBAL_WITNESS",
  "actual_order":len(elements)==cert["actual_order"],"complete_local_B3":len({c.word_image(e.representative) for e in ball.elements})==457,
  "candidate_kernel_identity":c.word_image(word)==c.identity(),"Gamma_B_nonidentity":projective_key(geom)!=projective_key(IDENTITY_MATRIX),
  "exact_key":payload==w["exact_group_key"],"strict_cutoff":delta.is_negative is True,"delta":str(delta)==w["squared_cutoff_delta"],
  "danger_registered":any(x["witness_id"]==w["witness_id"] for x in dr),"witness_registered":any(x["Witness ID"]==w["witness_id"] for x in wr)}
 if not all(v for k,v in checks.items() if k!="certificate_sha256"): raise RuntimeError(f"global replay failed: {checks}")
 out=R4/"11_CERTIFICATES"/f"{cid}.global_independent_replay.json"
 out.write_text(json.dumps({"schema_version":"1.0","task_id":f"{cid}-GLOBAL-INDEPENDENT-REPLAY","classification":"PASS_REJECTION_CONFIRMED","checks":checks,"exact_half_trace":str(tr),"exact_squared_delta":str(delta)},indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main(sys.argv[1])
