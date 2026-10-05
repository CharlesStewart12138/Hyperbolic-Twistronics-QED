"""Certify the first nonnested D2 branch covering all current global witnesses."""
from __future__ import annotations
import csv,hashlib,importlib,json
from pathlib import Path
p2=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")
ROOT=Path(__file__).resolve().parents[2]; R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4"; ROWS=(6,9)
CERT=R4/"05_P_QUOTIENT"/"P2C2_C8_D2_BRANCH_0005.certificate.json"; W=R4/"09_CEGAR"/"WITNESS_LEDGER.tsv"
LIB=R4/"03_SEPARATOR_LIBRARY"/"SEPARATOR_LIBRARY.tsv"; MAT=R4/"03_SEPARATOR_LIBRARY"/"SEPARATOR_MATRIX.tsv"
def write(path,fields,rows):
 with path.open("w",encoding="utf-8",newline="") as h: w=csv.DictWriter(h,delimiter="\t",fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(rows)
def main():
 elements,rotation=p2.enumerate_q(ROWS)
 if rotation is None: raise RuntimeError("D2 branch rotation is inconsistent")
 with W.open(encoding="utf-8",newline="") as h: wr=list(csv.DictReader(h,delimiter="\t"))
 coverage={r["Witness ID"]:int(p2.q_word(tuple(r["Canonical word"].split()),ROWS)!=(0,0)) for r in wr}
 global_ids=[r["Witness ID"] for r in wr if r["Type"]=="D_global(6a_B)"]
 payload={"family":"C8-stable class2 D2 nonnested branch","rows":ROWS,"physical":p2.q_physical_generators(ROWS),"elements":sorted(elements)}
 mh=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode("ascii")).hexdigest().upper(); fid=f"P2C2-C8-D2-{mh[:16]}"
 checks={"C8_stable":p2.stable(ROWS,p2.phi_central_columns()),"actual_order_64":len(elements)==64,
  "complete_normal_form":set(elements)=={(v,z) for v in range(16) for z in range(4)},
  "rotation_eighth":all(iterate(rotation,x,8)==x for x in elements),"rotation_exact_eight":any(iterate(rotation,x,4)!=x for x in elements),
  "all_current_global_witnesses":all(coverage[x]==1 for x in global_ids)}
 if not all(checks.values()): raise RuntimeError(f"D2 branch failed: {checks}")
 cert={"schema_version":"1.0","factor_id":fid,"family":"C8-stable lower-exponent-2 class-2 D2 nonnested branch","actual_order":64,
  "marked_quotient_hash":mh,"construction":{"central_basis":list(p2.CENTRAL_BASIS),"selected_dual_row_space_integers":list(ROWS),
  "selected_dual_row_space_bits_lsb_first":[format(r,"09b")[::-1] for r in ROWS],"selection_rule":"lexicographically first D2 space covering every current global witness"},
  "proof_rows":checks,"global_witness_ids":global_ids,"witness_coverage":coverage,"classification":"PASS"}
 CERT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
 with LIB.open(encoding="utf-8",newline="") as h: rd=csv.DictReader(h,delimiter="\t"); fields=list(rd.fieldnames or []); rows=list(rd)
 rows.append({"factor_id":fid,"family":cert["family"],"parameters":"p=2; class=2; marginal_dimension=2; nonnested branch rows=6,9","actual_order":"64",
  "marked_quotient_hash":mh,"coverage_count":str(sum(coverage.values())),"C8_cost":"0","parity_cost":"0","subdirect_marginal_order_increase":"4",
  "resource_marginal_increase":"64","certificate_path":"05_P_QUOTIENT/P2C2_C8_D2_BRANCH_0005.certificate.json","certificate_sha256":hashlib.sha256(CERT.read_bytes()).hexdigest().upper(),"status":"AVAILABLE"})
 write(LIB,fields,rows)
 with MAT.open(encoding="utf-8",newline="") as h: rd=csv.DictReader(h,delimiter="\t"); fields=list(rd.fieldnames or []); rows=list(rd)
 fields.append(fid)
 for r in rows: r[fid]=str(coverage[r["witness_id"]])
 write(MAT,fields,rows)
def iterate(mapping,x,n):
 for _ in range(n): x=mapping[x]
 return x
if __name__=="__main__": main()
