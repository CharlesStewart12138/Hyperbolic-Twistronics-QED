#!/usr/bin/env python3
"""Prepare versioned GAP wrappers for sample or all split-heavy manifest exports."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

ROOT=Path(r"D:\work\revise"); BASE=ROOT/"production_code/escalations/degree24_v3_repair"
PROFILE=ROOT/"production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt"
SCOPE=BASE/"DEG24_SPLIT_HEAVY_KEYS_V3.tsv"; SAMPLE=BASE/"DEG24_MANIFEST_REPRODUCIBILITY_SAMPLE_KEYS_V3.tsv"

def profiles():
 out={}
 for line in PROFILE.read_text(encoding="utf-8").splitlines():
  f=line.split("\t")
  if f[0]!="ENTRY": continue
  v={f[i]:f[i+1] for i in range(2,len(f),2)}; k=int(f[1].removeprefix("24T")); out[k]=v
 return out
def write_exact(path,text):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():
  if path.read_text(encoding="utf-8")!=text: raise ValueError(f"existing wrapper differs: {path}")
  return
 path.write_text(text,encoding="utf-8",newline="\n")
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--scope",choices=("sample","all"),required=True); a=ap.parse_args()
 allkeys=[int(r["key"]) for r in csv.DictReader(SCOPE.open(encoding="utf-8"),delimiter="\t")]
 if a.scope=="sample":
  keys=[int(r["key"]) for r in csv.DictReader(SAMPLE.open(encoding="utf-8"),delimiter="\t")]
  keys=sorted(set(keys+[8491,11363]))
 else: keys=allkeys
 p=profiles(); jobs=[]
 for k in keys:
  v=p[k]
  wrapper=BASE/f"manifest_jobs/gap_export_24T{k}_manifest_source_v3.g"
  out=BASE/f"manifest_sources/DEG24_KEY_24T{k}_MANIFEST_SOURCE_V3.tsv"
  text=(f"KEY_RECORD:=rec(k:={k},order:={v['ORDER']},autOrder:={v['AUT_ORDER']},parity:={v['PARITY_MAPS']},classes:={v['ORDER8_CLASSES']},route:=\"{v['ROUTE']}\",representation:=\"{v['REPRESENTATION']}\",pcOrder:={v['PC_ORDER']});\n"
        f"AUTHOR_SEED:=1; OUT:=\"/mnt/d/work/revise/{out.relative_to(ROOT).as_posix()}\";\n"
        "Read(\"/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_export_key_authoritative_manifest_raw_v3.g\");\n")
  write_exact(wrapper,text); jobs.append(dict(key=k,wrapper=wrapper.relative_to(ROOT).as_posix(),output=out.relative_to(ROOT).as_posix(),route=v["ROUTE"],classes=int(v["ORDER8_CLASSES"])))
 reg=BASE/f"DEG24_MANIFEST_{a.scope.upper()}_JOBS_V3.json"
 reg.write_text(json.dumps(dict(schema="DEG24_MANIFEST_JOBS_V3",scope=a.scope,jobs=jobs),indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
 print(json.dumps(dict(scope=a.scope,jobs=len(jobs),keys=keys),sort_keys=True))
if __name__=="__main__": main()
