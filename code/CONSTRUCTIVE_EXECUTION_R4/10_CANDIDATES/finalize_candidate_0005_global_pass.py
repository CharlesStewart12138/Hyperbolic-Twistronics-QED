"""Freeze the first complete global-pass candidate as FEASIBLE_UNMINIMIZED."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4"
CID="CAND-R4-0005"; CERT=R4/"10_CANDIDATES"/f"{CID}.certificate.json"; CP=R4/"checkpoints"/f"{CID}-axis6.tsv"
SCAN=R4/"10_CANDIDATES"/"scan_candidate_0005_axis6.cpp"; EXE=SCAN.with_suffix(".exe"); MAN=R4/"00_FROZEN_INPUTS"/"manifests"/"axis6_exact_ball_manifest.json"
LEDGER=R4/"10_CANDIDATES"/"CANDIDATE_LEDGER.tsv"; PASS=R4/"11_CERTIFICATES"/f"{CID}.global_pass_scan.json"
FREEZE=R4/"11_CERTIFICATES"/f"FEASIBLE_UNMINIMIZED_{CID}.json"; REPORT=R4/"16_REPORTS"/"FIRST_GLOBAL_VALID_CANDIDATE.md"
def fh(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def state():
 with CP.open(encoding="utf-8") as h:return dict(line.rstrip("\n").split("\t",1) for line in h if "\t" in line)
def main():
 s=state(); total=int(s["total_records"]); scanned=int(s["scanned_records"])
 if s["hit"]!="0" or scanned!=total or total!=785639753: raise RuntimeError(f"incomplete global pass checkpoint: {s}")
 witness=R4/"10_CANDIDATES"/f"{CID}.global_witness.tsv"
 if witness.exists(): raise RuntimeError("global-pass candidate unexpectedly has a witness file")
 cert=json.loads(CERT.read_text(encoding="utf-8"))
 if cert["classification"]!="LOCAL_PASS_GLOBAL_PENDING": raise RuntimeError("candidate not global-pending")
 cert["schema_version"]="1.1"; cert["gates"]["based"]="NOT_REQUIRED_BY_CURRENT_GLOBAL_SYSTOLE_TARGET"
 cert["gates"]["global_systole"]="PASS_COMPLETE_CLOSED_DOMAIN"
 cert["global_pass"]={"cutoff":"translation length <= 6*a_B is dangerous; equality included","complete_closed_domain_records":total,
  "kernel_hits":0,"registry_manifest":"00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json","registry_manifest_sha256":fh(MAN),
  "scanner_source":"10_CANDIDATES/scan_candidate_0005_axis6.cpp","scanner_source_sha256":fh(SCAN),"scanner_executable_sha256":fh(EXE),
  "checkpoint_sha256":fh(CP),"elapsed_seconds":float(s["elapsed_seconds"]),"independent_clean_replay":"PENDING"}
 cert["resource"].update({"global_registry_total_records":total,"global_registry_scanned_records":scanned,"global_scan_complete":True,
  "global_kernel_hits":0,"global_scan_elapsed_seconds":float(s["elapsed_seconds"])})
 cert["classification"]="FEASIBLE_UNMINIMIZED"
 CERT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
 pass_cert={"schema_version":"1.0","task_id":f"{CID}-GLOBAL-PASS-SCAN","classification":"PASS_COMPLETE_CLOSED_DOMAIN",
  "candidate_id":CID,"candidate_order":cert["actual_order"],"marked_quotient_hash":cert["marked_quotient_hash"],"records_scanned":scanned,
  "kernel_hits":0,"closed_boundary":True,"cutoff":"6*a_B","registry_manifest_sha256":fh(MAN),"scanner_source_sha256":fh(SCAN),
  "scanner_executable_sha256":fh(EXE),"checkpoint_sha256":fh(CP),"candidate_certificate_sha256":fh(CERT),"independent_replay":"PENDING"}
 PASS.write_text(json.dumps(pass_cert,indent=2)+"\n",encoding="utf-8")
 freeze={"schema_version":"1.0","status":"FEASIBLE_UNMINIMIZED","candidate_id":CID,"actual_order":cert["actual_order"],
  "factor_ids":cert["factor_ids"],"marked_quotient_hash":cert["marked_quotient_hash"],"hard_gates":{"algebra":"PASS","shell":"PASS","C8":"PASS","parity":"PASS",
  "local_B_geom_3":"PASS","global_systole":"PASS_COMPLETE_CLOSED_DOMAIN"},"resource_gate":"PENDING","independent_complete_global_replay":"PENDING",
  "candidate_certificate_sha256":fh(CERT),"global_pass_certificate_sha256":fh(PASS)}
 FREEZE.write_text(json.dumps(freeze,indent=2)+"\n",encoding="utf-8")
 with LEDGER.open(encoding="utf-8",newline="") as h: r=csv.DictReader(h,delimiter="\t"); fields=list(r.fieldnames or []); rows=list(r)
 for row in rows:
  if row["Candidate ID"]==CID:
   row["Based status"]="NOT_REQUIRED_BY_CURRENT_GLOBAL_SYSTOLE_TARGET"; row["Global status"]="PASS_COMPLETE_CLOSED_DOMAIN"
   row["Resource estimate"]=json.dumps(cert["resource"],separators=(",",":")); row["Final disposition"]="FEASIBLE_UNMINIMIZED"; row["Certificate hash"]=fh(CERT); break
 else: raise RuntimeError("candidate ledger row absent")
 with LEDGER.open("w",encoding="utf-8",newline="") as h: w=csv.DictWriter(h,delimiter="\t",fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
 REPORT.write_text("# First global-valid constructive candidate\n\n"
  "`CAND-R4-0005` is frozen as **FEASIBLE_UNMINIMIZED**. Its actual generated order is 46,080. It passes the exact algebra, physical-shell, C8, parity, complete B_geom(3), and complete closed global systole domains. The first scan evaluated all 785,639,753 frozen registry records with no kernel hit.\n\n"
  "Independent complete global replay, minimization, faithful-degree analysis, and the production resource gate remain pending; therefore this is not yet LEVEL_A1.\n",encoding="utf-8")
if __name__=="__main__":main()
