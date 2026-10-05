#!/usr/bin/env python3
"""Build a sealed per-key Route-B manifest from one GAP source export."""
from __future__ import annotations
import argparse, csv, hashlib, json
from pathlib import Path

ROOT=Path(r"D:\work\revise")
BASE=ROOT/"production_code/escalations/degree24_v3_repair"

def sha_file(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def sha_text(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def gap_string(s): return '"'+s.replace("\\","\\\\").replace('"','\\"')+'"'

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("key",type=int); args=ap.parse_args(); k=args.key
 src=BASE/f"manifest_sources/DEG24_KEY_24T{k}_MANIFEST_SOURCE_V3.tsv"
 meta={}; rows=[]
 for line in src.read_text(encoding="utf-8").splitlines():
  f=line.split("\t")
  if f[0]=="CLASS":
   if len(f)!=9: raise ValueError(f"bad class row length {len(f)}")
   rows.append(dict(source_ordinal_diagnostic=f[1],representative_display_diagnostic=f[2],pc_exponents_diagnostic=f[3],representative_serialization=f[4],class_size=f[5],centralizer_size=f[6],order=f[7],structural_filters=f[8]))
  elif len(f)==2: meta[f[0]]=f[1]
 if meta.get("KEY_ID")!=f"24T{k}" or len(rows)!=int(meta["ORDER8_CLASS_COUNT"]): raise ValueError("source metadata mismatch")
 schema=meta["REPRESENTATION_SCHEMA"]; genser=meta["GENERATOR_SERIALIZATION"]; gensha=sha_text(genser)
 seen=set()
 for row in rows:
  ser=row["representative_serialization"]
  if ser in seen: raise ValueError("duplicate explicit representative")
  seen.add(ser)
  payload=f"KEY_ID=24T{k}\nSCHEMA={schema}\nGENERATOR_TUPLE_SHA256={gensha}\nREPRESENTATIVE_SERIALIZATION={ser}\nCLASS_SIZE={row['class_size']}\nORDER={row['order']}\nCENTRALIZER_SIZE={row['centralizer_size']}\n"
  row["class_id_v3"]=sha_text(payload)
 rows.sort(key=lambda r:(r["representative_serialization"],int(r["class_size"]),int(r["centralizer_size"])))
 for pos,row in enumerate(rows,1):
  row["key_id"]=f"24T{k}"; row["manifest_position"]=str(pos)
  row["row_sha256"]=sha_text("\t".join([row["key_id"],row["class_id_v3"],row["manifest_position"],row["representative_serialization"],row["class_size"],row["centralizer_size"],row["order"],row["structural_filters"]]))
 outdir=BASE/f"manifests/24T{k}"; outdir.mkdir(parents=True,exist_ok=True)
 tsv=outdir/f"DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.tsv"; gap=outdir/f"DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.g"; js=outdir/f"DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.json"
 for p in (tsv,gap,js):
  if p.exists(): raise SystemExit(f"refusing to overwrite {p}")
 fields=["key_id","class_id_v3","manifest_position","representative_serialization","class_size","centralizer_size","order","structural_filters","source_ordinal_diagnostic","representative_display_diagnostic","pc_exponents_diagnostic","row_sha256"]
 with tsv.open("x",encoding="utf-8",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(rows)
 with gap.open("x",encoding="utf-8",newline="\n") as h:
  h.write("D24C8_MANIFEST_META:=rec(\n")
  h.write(f" key:={k}, route:={gap_string(meta['ROUTE'])}, representation:={gap_string(meta['REPRESENTATION'])},\n")
  h.write(f" groupOrder:={meta['GROUP_ORDER']}, autOrder:={meta['AUTOMORPHISM_GROUP_ORDER']}, parity:={meta['PARITY_MAPS']}, pcOrder:={meta['PC_ORDER']},\n")
  h.write(f" schema:={gap_string(schema)}, generatorSerialization:={gap_string(genser)}, generatorTupleSha256:={gap_string(gensha)},\n")
  h.write(f" classCount:={len(rows)}, sourceSha256:={gap_string(sha_file(src))});\nD24C8_MANIFEST_RECORDS:=[\n")
  for i,row in enumerate(rows):
   imgs=",".join("["+x+"]" for x in row["representative_serialization"].split(";")); suffix="," if i+1<len(rows) else ""
   h.write(f"rec(classId:={gap_string(row['class_id_v3'])},position:={row['manifest_position']},images:=[{imgs}],classSize:={row['class_size']},centralizerSize:={row['centralizer_size']},order:={row['order']},sourceOrdinalDiagnostic:={row['source_ordinal_diagnostic']}){suffix}\n")
  h.write("];\n")
 summary=dict(schema="DEG24_AUTHORITATIVE_CLASS_MANIFEST_V3",route="B_FROZEN_EXPLICIT_REPRESENTATIVES",key_id=f"24T{k}",class_count=len(rows),class_id_count=len({r['class_id_v3'] for r in rows}),group_order=int(meta["GROUP_ORDER"]),automorphism_group_order=int(meta["AUTOMORPHISM_GROUP_ORDER"]),parity_maps=int(meta["PARITY_MAPS"]),gap_route=meta["ROUTE"],representation=meta["REPRESENTATION"],representation_schema=schema,generator_tuple_sha256=gensha,source=src.relative_to(ROOT).as_posix(),source_sha256=sha_file(src),manifest=tsv.relative_to(ROOT).as_posix(),manifest_sha256=sha_file(tsv),gap_manifest=gap.relative_to(ROOT).as_posix(),gap_manifest_sha256=sha_file(gap),worker_contract="Workers reconstruct and consume these representatives; ordinals are diagnostic only.")
 js.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
 print(json.dumps(summary,sort_keys=True))
if __name__=="__main__": main()
