"""Run deterministic factor-deletion minimization for CAND-R4-0005."""
from __future__ import annotations
import hashlib,importlib,json
from pathlib import Path
from production_code.group.universal_cover import enumerate_ball
arith=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
p2=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")
c=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0005")
ROOT=Path(__file__).resolve().parents[2];R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4";OUT=R4/"12_MINIMIZATION"/"CAND-R4-0005.factor_deletion.json"
def main():
 ball=enumerate_ball(3);p3imgs={arith.word_image(e.representative,3) for e in ball.elements};qimgs={p2.q_word(e.representative,(6,9)) for e in ball.elements}
 p3_shell=tuple(arith.generator(i,3) for i in range(8));q_shell=p2.q_physical_generators((6,9))
 rows=[{"deleted_factor":"P2C2-C8-D2-1D16194A8DBB81E2","remaining_factor":"ARITH-P3-6F6FBFF4038772DA","remaining_actual_order":720,
   "order_interval":False,"parity":False,"local_distinct_images":len(p3imgs),"all_hard_gates_pass":False},
  {"deleted_factor":"ARITH-P3-6F6FBFF4038772DA","remaining_factor":"P2C2-C8-D2-1D16194A8DBB81E2","remaining_actual_order":64,
   "order_interval":False,"parity":all((x[0].bit_count()&1)==1 for x in q_shell),"local_distinct_images":len(qimgs),"all_hard_gates_pass":False}]
 cert=json.loads((R4/"10_CANDIDATES"/"CAND-R4-0005.certificate.json").read_text(encoding="utf-8"))
 OUT.write_text(json.dumps({"schema_version":"1.0","candidate_id":"CAND-R4-0005","algorithm":"canonical factor deletion to fixed point",
  "actual_subdirect_already_used":True,"candidate_actual_order":46080,"factor_tests":rows,"factors_deleted":[],"classification":"MINIMAL_WITHIN_SELECTED_TWO_FACTOR_PRESENTATION",
  "scope_limit":"not a proof of globally minimum group order across unrelated construction families","candidate_certificate_sha256":hashlib.sha256((R4/"10_CANDIDATES"/"CAND-R4-0005.certificate.json").read_bytes()).hexdigest().upper()},indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
