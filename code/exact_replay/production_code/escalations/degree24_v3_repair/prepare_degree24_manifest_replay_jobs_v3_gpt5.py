#!/usr/bin/env python3
"""Prepare fresh-process replay wrappers for the seven validation samples."""
from __future__ import annotations
import csv, json
from pathlib import Path
ROOT=Path(r"D:\work\revise"); BASE=ROOT/"production_code/escalations/degree24_v3_repair"
SAMPLE=BASE/"DEG24_MANIFEST_REPRODUCIBILITY_SAMPLE_KEYS_V3.tsv"
def main():
 keys=[int(r["key"]) for r in csv.DictReader(SAMPLE.open(encoding="utf-8"),delimiter="\t")]; keys=sorted(set(keys+[8491,11363]))
 jobs=[]
 for k in keys:
  manifest=BASE/f"manifests/24T{k}/DEG24_KEY_24T{k}_CLASS_MANIFEST_V3.g"; wrapper=BASE/f"manifest_replay_jobs/gap_replay_24T{k}_seed12345_v3.g"; out=BASE/f"manifest_replay/DEG24_KEY_24T{k}_MANIFEST_REPLAY_SEED12345_V3.txt"
  wrapper.parent.mkdir(parents=True,exist_ok=True); out.parent.mkdir(parents=True,exist_ok=True)
  text=(f"MANIFEST_FILE:=\"/mnt/d/work/revise/{manifest.relative_to(ROOT).as_posix()}\"; VERIFY_SEED:=12345; VERIFY_RUN_ID:=\"24T{k}_INDEPENDENT_SEED12345\";\n"
        f"VERIFY_OUT:=\"/mnt/d/work/revise/{out.relative_to(ROOT).as_posix()}\";\nRead(\"/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_verify_key_authoritative_manifest_v3.g\");\n")
  if wrapper.exists() and wrapper.read_text(encoding="utf-8")!=text: raise ValueError(f"wrapper mismatch {wrapper}")
  if not wrapper.exists(): wrapper.write_text(text,encoding="utf-8",newline="\n")
  jobs.append(dict(key=k,wrapper=wrapper.relative_to(ROOT).as_posix(),output=out.relative_to(ROOT).as_posix()))
 reg=BASE/"DEG24_MANIFEST_SAMPLE_REPLAY_JOBS_V3.json"; reg.write_text(json.dumps(dict(schema="DEG24_MANIFEST_SAMPLE_REPLAY_JOBS_V3",seed=12345,jobs=jobs),indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
 print(json.dumps(dict(jobs=len(jobs),keys=keys),sort_keys=True))
if __name__=="__main__": main()
