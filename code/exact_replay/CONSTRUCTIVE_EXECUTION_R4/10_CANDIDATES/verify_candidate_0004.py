"""Independent pre-global replay of CAND-R4-0004."""

from __future__ import annotations

import csv, hashlib, importlib, json
from pathlib import Path
from production_code.group.universal_cover import enumerate_ball

c = importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_0004")
ROOT=Path(__file__).resolve().parents[2]; R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4"; CERT=R4/"10_CANDIDATES"/"CAND-R4-0004.certificate.json"
W=R4/"09_CEGAR"/"WITNESS_LEDGER.tsv"; RESULT=R4/"11_CERTIFICATES"/"CAND-R4-0004.local_independent_replay.json"

def it(x,n):
    for _ in range(n): x=c.phi(x)
    return x

def main():
    data=CERT.read_bytes(); cert=json.loads(data); elements=c.enumerate_image(); shell=tuple(c.generator(i) for i in range(8)); ball=enumerate_ball(3)
    with W.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h,delimiter="\t"))
    rel=tuple(f"g{i}" for i in (0,5,2,7,4,1,6,3))
    checks={"certificate_sha256":hashlib.sha256(data).hexdigest().upper(),"actual_order_46080":len(elements)==cert["actual_order"]==46080,
      "surface_relation":c.word_image(rel)==c.identity(),"physical_shell":len(set(shell))==8 and c.identity() not in shell,
      "C8_covariance":all(c.phi(shell[i])==shell[(i+1)%8] for i in range(8)),"C8_eighth":all(it(x,8)==x for x in elements),
      "C8_exact_eight":any(it(x,4)!=x for x in elements),"parity":all((x[8].bit_count()&1)==1 for x in shell),
      "complete_local_B3":len({c.word_image(e.representative) for e in ball.elements})==457,
      "all_accumulated_witnesses":all(c.word_image(tuple(row["Canonical word"].split()))!=c.identity() for row in rows)}
    if not all(v for k,v in checks.items() if k!="certificate_sha256"): raise RuntimeError(f"candidate0004 replay failed: {checks}")
    RESULT.write_text(json.dumps({"schema_version":"1.0","task_id":"CAND-R4-0004-LOCAL-INDEPENDENT-REPLAY","classification":"PASS","checks":checks},indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
