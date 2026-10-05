"""Finalize a standard-named R4 candidate at an exact global failure.

Usage: python -m ...finalize_global_candidate_generic CAND-R4-NNNN
The scanner/checkpoint/witness names must use the standard NNNN convention.
"""

from __future__ import annotations

import csv, hashlib, importlib, json, sys
from pathlib import Path
import sympy as sp
from production_code.group.run_cm_grp_ext_001 import projective_key
from production_code.group.universal_cover import IDENTITY_MATRIX, field_to_sympy, matrix_from_word

arith=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.04_ARITHMETIC.build_arithmetic_separators")
p2=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.05_P_QUOTIENT.build_c8_class2_marginal")
d0=importlib.import_module("CONSTRUCTIVE_EXECUTION_R4.02_DANGEROUS_SETS.build_initial_registry")
ROOT=Path(__file__).resolve().parents[2]; R4=ROOT/"CONSTRUCTIVE_EXECUTION_R4"
DANGER=R4/"02_DANGEROUS_SETS"/"DANGEROUS_SET_REGISTRY.tsv"; WLEDGER=R4/"09_CEGAR"/"WITNESS_LEDGER.tsv"
MATRIX=R4/"03_SEPARATOR_LIBRARY"/"SEPARATOR_MATRIX.tsv"; LIBRARY=R4/"03_SEPARATOR_LIBRARY"/"SEPARATOR_LIBRARY.tsv"
CLEDGER=R4/"10_CANDIDATES"/"CANDIDATE_LEDGER.tsv"; MANIFEST=R4/"00_FROZEN_INPUTS"/"manifests"/"axis6_exact_ball_manifest.json"

def fh(path): return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def write_tsv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,delimiter="\t",fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(rows)
def checkpoint(path):
    with path.open(encoding="utf-8") as h: return dict(line.rstrip("\n").split("\t",1) for line in h if "\t" in line)

def factor_value(factor,word):
    if factor["factor_id"].startswith("ARITH-P"):
        prime=int(factor["parameters"].split("p=",1)[1].split(";",1)[0]); return int(arith.word_image(word,prime)!=arith.aidentity(prime))
    if factor["factor_id"].startswith("P2C2-"):
        cert=json.loads((R4/factor["certificate_path"]).read_text(encoding="utf-8")); rows=tuple(cert["construction"]["selected_dual_row_space_integers"])
        return int(p2.q_word(word,rows)!=(0,0))
    raise RuntimeError(f"unsupported separator family {factor['factor_id']}")

def main(candidate_id):
    serial=candidate_id.rsplit("-",1)[1]; short=str(int(serial)); c=importlib.import_module(f"CONSTRUCTIVE_EXECUTION_R4.10_CANDIDATES.build_candidate_{serial}")
    cert_path=R4/"10_CANDIDATES"/f"{candidate_id}.certificate.json"; scan=R4/"10_CANDIDATES"/f"{candidate_id}.global_witness.tsv"
    cp=R4/"checkpoints"/f"{candidate_id}-axis6.tsv"; scanner=R4/"10_CANDIDATES"/f"scan_candidate_{serial}_axis6.cpp"; exe=scanner.with_suffix(".exe")
    with scan.open(encoding="utf-8",newline="") as h: scan_rows=list(csv.DictReader(h,delimiter="\t"))
    if len(scan_rows)!=1: raise RuntimeError("expected one early-exit witness")
    row=scan_rows[0]; source=tuple(row["word"].split()); word=d0.canonical_c8_inverse_word(source); image=c.word_image(word)
    if image!=c.identity(): raise RuntimeError("scanner witness is not in candidate kernel")
    geom=matrix_from_word(word); key=projective_key(geom)
    if key==projective_key(IDENTITY_MATRIX): raise RuntimeError("scanner witness is identity in Gamma_B")
    payload=json.dumps(key,separators=(",",":")); keyhash=hashlib.sha256(payload.encode("ascii")).hexdigest().upper(); a=geom[0]
    if a[3] or a[4]: raise RuntimeError("beta component in real half-trace")
    tr=sp.re(field_to_sympy(a)).expand(); cutoff=2405+1700*sp.sqrt(2)
    if a[1]>=0 and a[2]>=0: absolute=tr
    elif a[1]<=0 and a[2]<=0: absolute=-tr
    else: raise RuntimeError("mixed-sign Qsqrt2 trace branch")
    margin=sp.expand(cutoff-absolute); delta=sp.expand(absolute**2-cutoff**2)
    if margin.is_positive is not True or delta.is_negative is not True: raise RuntimeError("strict global cutoff not proved")
    scanner_coeffs=tuple(int(row[f"re_c{i}"]) for i in range(4))
    canonical_coeffs=tuple(a[1:5]); projective_coeffs={canonical_coeffs,tuple(-value for value in canonical_coeffs)}
    if int(row["exponent"])!=a[0] or scanner_coeffs not in projective_coeffs: raise RuntimeError("scanner trace mismatch modulo M~-M")
    state=checkpoint(cp); witness_id=f"W-{keyhash[:20]}"; orbit_id=f"C8-{hashlib.sha256(' '.join(word).encode('ascii')).hexdigest().upper()[:20]}"
    witness={"witness_id":witness_id,"canonical_word":list(word),"source_word":list(source),"record_index_zero_based":int(row["record_index"]),
      "record_depth":int(row["depth"]),"candidate_image":list(image),"candidate_image_identity":True,"nonidentity_in_Gamma_B":True,
      "exact_group_key":payload,"exact_group_key_sha256":keyhash,"global_type":"D_global(6a_B)","universal_class2_image":list(p2.word_full_geometric(word)),
      "half_trace_absolute_expression":str(absolute),"cutoff_cosh_3aB_over_R":"2405 + 1700*sqrt(2)","strict_positive_cutoff_margin":str(margin),
      "squared_cutoff_delta":str(delta),"translation_length_over_a_B":f"acosh({absolute})/acosh(1+sqrt(2))",
      "boundary_policy":"equality is dangerous; this witness is strictly below the cutoff","early_exit_scope":"first dangerous kernel hit in canonical registry order",
      "registry_manifest":"00_FROZEN_INPUTS/manifests/axis6_exact_ball_manifest.json","registry_manifest_sha256":fh(MANIFEST),
      "scanner_source":str(scanner.relative_to(R4)).replace("\\","/"),"scanner_source_sha256":fh(scanner),"scanner_executable_sha256":fh(exe),
      "scanner_checkpoint_sha256":fh(cp),"scanner_witness_sha256":fh(scan)}
    cert=json.loads(cert_path.read_text(encoding="utf-8"))
    if cert["classification"]!="LOCAL_PASS_GLOBAL_PENDING": raise RuntimeError("candidate not global-pending")
    cert["schema_version"]="1.1"; cert["gates"]["based"]="NOT_RUN_NOT_REQUIRED_AFTER_GLOBAL_FAILURE"; cert["gates"]["global_systole"]="FAIL_EARLY_EXACT_WITNESS"
    cert["global_failure_witness"]=witness; cert["resource"].update({"global_registry_total_records":int(state["total_records"]),"global_registry_scanned_records":int(state["scanned_records"]),
      "global_scan_early_exit":True,"global_scan_elapsed_seconds":float(state["elapsed_seconds"])}); cert["classification"]="REJECTED_GLOBAL_WITNESS"
    cert_path.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")

    with DANGER.open(encoding="utf-8",newline="") as h: rr=csv.DictReader(h,delimiter="\t"); fields=list(rr.fieldnames or []); rows=list(rr)
    danger_id=f"DGLOBAL-R6-C{serial}-{witness_id}"
    if not any(x["danger_id"]==danger_id for x in rows):
      rows.append({"danger_id":danger_id,"type":"D_global(6a_B)","constraint_word_geometric":" ".join(word),"canonical_word_geometric":" ".join(word),
       "canonical_word_standard":" ".join(d0.standard_word(word)),"exact_group_key":payload,"exact_group_key_sha256":keyhash,"witness_id":witness_id,"word_depth":str(len(word)),
       "based_displacement_over_a_B":"","translation_length_over_a_B":witness["translation_length_over_a_B"],"translation_length_interval":"STRICTLY_LESS_THAN_6",
       "c8_orbit_id":orbit_id,"legacy_source_orbit_id":"","nonidentity_in_Gamma_B":"PASS_EXACT_KEY","geometry_status":"PASS_EXACT_TRACE_STRICT",
       "geometry_statement":"kernel element has translation length strictly less than 6*a_B","source_certificate":f"10_CANDIDATES/{candidate_id}.certificate.json","registry_status":"ACTIVE_CEGAR"})
      write_tsv(DANGER,fields,sorted(rows,key=lambda x:x["danger_id"]))
    with LIBRARY.open(encoding="utf-8",newline="") as h: factors=list(csv.DictReader(h,delimiter="\t"))
    values={f["factor_id"]:str(factor_value(f,word)) for f in factors}; known=[fid for fid,v in values.items() if v=="1"]
    with WLEDGER.open(encoding="utf-8",newline="") as h: rr=csv.DictReader(h,delimiter="\t"); fields=list(rr.fieldnames or []); rows=list(rr)
    if not any(x["Witness ID"]==witness_id for x in rows):
      rows.append({"Witness ID":witness_id,"Canonical word":" ".join(word),"Exact group key":payload,"Type":"D_global(6a_B)","Word depth":str(len(word)),
       "Based displacement if relevant":"","Translation length interval/exact expression":witness["translation_length_over_a_B"],"C8 orbit ID":orbit_id,
       "First candidate killed":candidate_id,"Separator factors known":",".join(known),"Currently separated by candidate":"NO","Certificate path":f"10_CANDIDATES/{candidate_id}.certificate.json"})
      write_tsv(WLEDGER,fields,sorted(rows,key=lambda x:x["Witness ID"]))
    with MATRIX.open(encoding="utf-8",newline="") as h: rr=csv.DictReader(h,delimiter="\t"); fields=list(rr.fieldnames or []); rows=list(rr)
    if not any(x["witness_id"]==witness_id for x in rows): rows.append({"witness_id":witness_id,**values}); write_tsv(MATRIX,fields,sorted(rows,key=lambda x:x["witness_id"]))
    with CLEDGER.open(encoding="utf-8",newline="") as h: rr=csv.DictReader(h,delimiter="\t"); fields=list(rr.fieldnames or []); rows=list(rr)
    for x in rows:
      if x["Candidate ID"]==candidate_id:
       x["Based status"]="NOT_RUN_NOT_REQUIRED_AFTER_GLOBAL_FAILURE"; x["Global status"]="FAIL_EARLY_EXACT_WITNESS"; x["Shortest failure witness"]=witness_id
       x["Witness orbit ID"]=orbit_id; x["Resource estimate"]=json.dumps(cert["resource"],separators=(",",":")); x["Final disposition"]="REJECTED_GLOBAL_WITNESS"; x["Certificate hash"]=fh(cert_path); break
    else: raise RuntimeError("candidate ledger row absent")
    write_tsv(CLEDGER,fields,rows)
    lower=cert["actual_order"]*2
    iteration={"schema_version":"1.0","iteration":int(serial),"candidate_id":candidate_id,"candidate_order":cert["actual_order"],"first_failed_gate":"global_systole",
      "classification":"EXACT_GLOBAL_COUNTEREXAMPLE_REGISTERED","witness_id":witness_id,"witness_orbit_id":orbit_id,"known_separator_factors":known,
      "universal_class2_image":witness["universal_class2_image"],"strict_refinement_order_lower_bound":lower,
      "strict_refinement_within_order_window":lower<=50000,"next_action":"audit nonnested separator branches" if lower>50000 else "construct strict refinement",
      "hpc_escalation_triggered":False,"candidate_certificate_sha256":fh(cert_path),"witness_ledger_sha256":fh(WLEDGER),"danger_registry_sha256":fh(DANGER),"separator_matrix_sha256":fh(MATRIX)}
    (R4/"09_CEGAR"/f"ITERATION_{serial}_GLOBAL_REJECTION.json").write_text(json.dumps(iteration,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: ... CAND-R4-NNNN")
    main(sys.argv[1])
