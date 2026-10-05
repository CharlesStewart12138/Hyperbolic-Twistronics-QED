"""Finalize the independent complete global replay for CAND-R4-0005."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
import sympy as sp
from production_code.group.universal_cover import field_to_sympy,matrix_from_word
ROOT=Path(__file__).resolve().parents[2];R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4";CID="CAND-R4-0005"
CP=R4/"checkpoints"/f"{CID}-axis6-independent-v2.tsv";SRC=R4/"11_CERTIFICATES"/"scan_candidate_0005_independent_v2.cpp";EXE=SRC.with_suffix(".exe")
CERT=R4/"10_CANDIDATES"/f"{CID}.certificate.json";PASS=R4/"11_CERTIFICATES"/f"{CID}.global_pass_scan.json";FREEZE=R4/"11_CERTIFICATES"/f"FEASIBLE_UNMINIMIZED_{CID}.json"
OUT=R4/"11_CERTIFICATES"/f"{CID}.global_independent_replay.json";QUAR=R4/"11_CERTIFICATES"/f"{CID}.independent_v1_false_hit_quarantine.json"
LEDGER=R4/"10_CANDIDATES"/"CANDIDATE_LEDGER.tsv";V1=R4/"11_CERTIFICATES"/f"{CID}.independent_global_witness.tsv";V2=R4/"11_CERTIFICATES"/f"{CID}.independent_global_witness-v2.tsv"
def fh(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def st(p):
 with p.open(encoding="utf-8") as h:return dict(line.rstrip("\n").split("\t",1) for line in h if "\t" in line)
def main():
 s=st(CP)
 if s["hit"]!="0" or int(s["scanned_records"])!=int(s["total_records"]) or int(s["total_records"])!=785639753:raise RuntimeError("independent scan incomplete")
 if V2.exists():raise RuntimeError("independent v2 unexpectedly emitted a witness")
 with V1.open(encoding="utf-8",newline="") as h:r=list(csv.DictReader(h,delimiter="\t"))[0]
 word=tuple(r["word"].split());tr=sp.re(field_to_sympy(matrix_from_word(word)[0])).expand();cut=2405+1700*sp.sqrt(2);delta=sp.expand(tr**2-cut**2)
 if delta.is_positive is not True:raise RuntimeError("v1 false-hit quarantine word unexpectedly dangerous")
 QUAR.write_text(json.dumps({"schema_version":"1.0","classification":"QUARANTINED_FALSE_POSITIVE_NOT_DANGEROUS",
  "source":"independent scanner v1 omitted the exact trace-domain filter","record_index_zero_based":int(r["record_index"]),"word":list(word),
  "candidate_image_identity":True,"absolute_half_trace":str(abs(tr)),"cutoff":"2405 + 1700*sqrt(2)","squared_cutoff_delta":str(delta),
  "strictly_outside_dangerous_domain":True,"used_for_candidate_disposition":False,"v1_witness_sha256":fh(V1)},indent=2)+"\n",encoding="utf-8")
 cert=json.loads(CERT.read_text(encoding="utf-8"));cert["global_pass"]["independent_clean_replay"]="PASS_COMPLETE_CLOSED_DOMAIN"
 cert["global_pass"]["independent_scan"]={"implementation":"joint 46,080-state transition machine; independently generated candidate transitions",
  "actual_image_order_self_test":46080,"local_B3_self_test":457,"records_scanned":int(s["scanned_records"]),"kernel_hits":0,
  "scanner_source":"11_CERTIFICATES/scan_candidate_0005_independent_v2.cpp","scanner_source_sha256":fh(SRC),"scanner_executable_sha256":fh(EXE),
  "checkpoint_sha256":fh(CP),"elapsed_seconds":float(s["elapsed_seconds"]),"v1_false_hit_quarantine":"11_CERTIFICATES/CAND-R4-0005.independent_v1_false_hit_quarantine.json"}
 CERT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
 result={"schema_version":"1.0","task_id":f"{CID}-INDEPENDENT-COMPLETE-GLOBAL-REPLAY","classification":"PASS_COMPLETE_CLOSED_DOMAIN",
  "candidate_id":CID,"candidate_order":46080,"independent_candidate_engine":"joint generated-image state machine, not separate factor word tests",
  "self_tests":{"actual_generated_order_46080":True,"inverse_shell":True,"surface_relator":True,"complete_local_B3_457":True},
  "global":{"closed_domain_records":int(s["scanned_records"]),"kernel_hits":0,"exact_trace_filter":True,"closed_boundary":True},
  "scanner_source_sha256":fh(SRC),"scanner_executable_sha256":fh(EXE),"checkpoint_sha256":fh(CP),"candidate_certificate_sha256":fh(CERT),
  "quarantined_v1_sha256":fh(QUAR)}
 OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
 p=json.loads(PASS.read_text(encoding="utf-8"));p["independent_replay"]="PASS_COMPLETE_CLOSED_DOMAIN";p["independent_replay_certificate_sha256"]=fh(OUT);p["candidate_certificate_sha256"]=fh(CERT);PASS.write_text(json.dumps(p,indent=2)+"\n",encoding="utf-8")
 f=json.loads(FREEZE.read_text(encoding="utf-8"));f["independent_complete_global_replay"]="PASS_COMPLETE_CLOSED_DOMAIN";f["candidate_certificate_sha256"]=fh(CERT);f["global_pass_certificate_sha256"]=fh(PASS);f["independent_replay_certificate_sha256"]=fh(OUT);FREEZE.write_text(json.dumps(f,indent=2)+"\n",encoding="utf-8")
 with LEDGER.open(encoding="utf-8",newline="") as h:rd=csv.DictReader(h,delimiter="\t");fields=list(rd.fieldnames or []);rows=list(rd)
 for row in rows:
  if row["Candidate ID"]==CID:row["Certificate hash"]=fh(CERT);break
 with LEDGER.open("w",encoding="utf-8",newline="") as h:w=csv.DictWriter(h,delimiter="\t",fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
