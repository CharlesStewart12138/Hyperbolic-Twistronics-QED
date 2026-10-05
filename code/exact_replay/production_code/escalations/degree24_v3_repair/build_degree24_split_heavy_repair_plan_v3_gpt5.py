#!/usr/bin/env python3
"""Build the CLASS_ID_V3 repair plan and exact coverage/disjointness proof."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(r"D:\work\revise"); BASE=ROOT/"production_code/escalations/degree24_v3_repair"
SCOPE=BASE/"DEG24_SPLIT_HEAVY_KEYS_V3.tsv"; PLAN=BASE/"DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.tsv"
CERT=BASE/"DEG24_SPLIT_HEAVY_COVERAGE_CERTIFICATE_V3.json"; SUMMARY=BASE/"DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.json"
SEGDIR=BASE/"repair_plan_segments"; MAX_RAW=45_000_000
def sha_file(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def sha_text(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def gap_string(s): return '"'+s.replace("\\","\\\\").replace('"','\\"')+'"'
def main():
 if PLAN.exists() or CERT.exists() or SUMMARY.exists(): raise SystemExit("refusing to overwrite existing V3 repair plan/certificate")
 SEGDIR.mkdir(parents=True,exist_ok=True)
 scope=list(csv.DictReader(SCOPE.open(encoding="utf-8"),delimiter="\t")); segments=[]; per_key_cert=[]; global_ids=[]; segno=0
 for s in scope:
  k=int(s["key"]); old_classes=int(s["old_class_units"]); old_raw=int(s["old_raw_pairs"])
  mdir=BASE/f"manifests/24T{k}"; meta_path=mdir/f"DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.json"; tsv_path=mdir/f"DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.tsv"; gap_path=mdir/f"DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.g"
  if not meta_path.exists(): raise FileNotFoundError(f"missing manifest 24T{k}")
  meta=json.loads(meta_path.read_text(encoding="utf-8"))
  if sha_file(tsv_path)!=meta["manifest_sha256"] or sha_file(gap_path)!=meta["gap_manifest_sha256"]: raise ValueError(f"manifest hash mismatch 24T{k}")
  rows=list(csv.DictReader(tsv_path.open(encoding="utf-8"),delimiter="\t")); order=int(meta["group_order"])
  if len(rows)!=meta["class_count"] or len({r["class_id_v3"] for r in rows})!=len(rows): raise ValueError(f"manifest cardinality failure 24T{k}")
  max_units=MAX_RAW//order
  if max_units<1: raise ValueError(f"raw cap too small 24T{k}")
  key_segment_ids=[]; assigned=[]
  for offset in range(0,len(rows),max_units):
   chunk=rows[offset:offset+max_units]; segno+=1; segid=f"D24V3S{segno:04d}_24T{k}"; ids=[r["class_id_v3"] for r in chunk]
   id_text="\n".join(ids)+"\n"; id_path=SEGDIR/f"{segid}.class_ids.txt"; data_path=SEGDIR/f"{segid}.g"
   id_path.write_text(id_text,encoding="ascii",newline="\n"); id_sha=sha_file(id_path)
   with data_path.open("x",encoding="utf-8",newline="\n") as h:
    h.write("D24C8_SEGMENT_META:=rec(\n")
    h.write(f" segmentId:={gap_string(segid)}, key:={k}, route:={gap_string(meta['gap_route'])}, representation:={gap_string(meta['representation'])},\n")
    h.write(f" groupOrder:={order}, autOrder:={meta['automorphism_group_order']}, parity:={meta['parity_maps']}, schema:={gap_string(meta['representation_schema'])},\n")
    h.write(f" generatorTupleSha256:={gap_string(meta['generator_tuple_sha256'])}, manifestSha256:={gap_string(meta['manifest_sha256'])}, classIdListSha256:={gap_string(id_sha)}, classCount:={len(chunk)}, rawPairs:={order*len(chunk)});\n")
    h.write("D24C8_SEGMENT_RECORDS:=[\n")
    for i,row in enumerate(chunk):
     imgs=",".join("["+x+"]" for x in row["representative_serialization"].split(";")); suffix="," if i+1<len(chunk) else ""
     h.write(f"rec(classId:={gap_string(row['class_id_v3'])},manifestPositionDiagnostic:={row['manifest_position']},images:=[{imgs}],classSize:={row['class_size']},centralizerSize:={row['centralizer_size']},order:={row['order']}){suffix}\n")
    h.write("];\n")
   data_sha=sha_file(data_path); segment_hash=sha_text(segid+"\n"+id_sha+"\n"+data_sha+"\n"+str(order*len(chunk))+"\n")
   segments.append(dict(segment_id=segid,key_id=f"24T{k}",class_count=str(len(chunk)),raw_pairs=str(order*len(chunk)),class_id_first=ids[0],class_id_last=ids[-1],class_id_list=id_path.relative_to(ROOT).as_posix(),class_id_list_sha256=id_sha,segment_data=data_path.relative_to(ROOT).as_posix(),segment_data_sha256=data_sha,manifest_sha256=meta["manifest_sha256"],segment_sha256=segment_hash))
   key_segment_ids.append(segid); assigned.extend(ids); global_ids.extend(f"24T{k}:{x}" for x in ids)
  manifest_ids=[r["class_id_v3"] for r in rows]; counts=Counter(assigned); missing=sorted(set(manifest_ids)-set(assigned)); extras=sorted(set(assigned)-set(manifest_ids)); duplicates=sorted(x for x,n in counts.items() if n!=1)
  raw=order*len(manifest_ids); passed=not missing and not extras and not duplicates and len(assigned)==len(manifest_ids)
  if not passed: raise ValueError(f"coverage/disjointness failure 24T{k}")
  per_key_cert.append(dict(key_id=f"24T{k}",manifest_class_count=len(manifest_ids),segment_count=len(key_segment_ids),segment_ids=key_segment_ids,coverage_missing_count=0,coverage_extra_count=0,coverage_duplicate_count=0,class_units=len(assigned),raw_pairs=raw,old_class_units=old_classes,old_raw_pairs=old_raw,class_count_difference=len(manifest_ids)-old_classes,raw_difference=raw-old_raw,status="PASS"))
 fields=list(segments[0])
 with PLAN.open("x",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(segments)
 global_counter=Counter(global_ids); global_duplicates=sum(n-1 for n in global_counter.values() if n>1)
 total_units=sum(x["class_units"] for x in per_key_cert); total_raw=sum(x["raw_pairs"] for x in per_key_cert); old_units=sum(int(x["old_class_units"]) for x in scope); old_raw=sum(int(x["old_raw_pairs"]) for x in scope)
 cert=dict(schema="DEG24_SPLIT_HEAVY_COVERAGE_CERTIFICATE_V3",affected_keys=len(per_key_cert),segments=len(segments),manifest_class_units=total_units,assigned_class_units=len(global_ids),coverage_missing_count=0,coverage_extra_count=0,coverage_duplicate_count=global_duplicates,every_class_id_occurs_exactly_once=global_duplicates==0 and len(global_counter)==len(global_ids),old_class_units=old_units,class_unit_difference=total_units-old_units,old_raw_pairs=old_raw,v3_raw_pairs=total_raw,raw_pair_difference=total_raw-old_raw,max_segment_raw_pairs=max(int(x["raw_pairs"]) for x in segments),raw_cap=MAX_RAW,per_key=per_key_cert,status="PASS" if global_duplicates==0 else "FAIL")
 CERT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
 summary=dict(schema="DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3",affected_keys=len(per_key_cert),segments=len(segments),class_units=total_units,raw_pairs=total_raw,old_raw_pairs=old_raw,raw_pair_difference=total_raw-old_raw,plan=PLAN.relative_to(ROOT).as_posix(),plan_sha256=sha_file(PLAN),coverage_certificate=CERT.relative_to(ROOT).as_posix(),coverage_certificate_sha256=sha_file(CERT),status=cert["status"])
 SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); print(json.dumps(summary,sort_keys=True))
if __name__=="__main__": main()
