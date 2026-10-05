#!/usr/bin/env python3
"""Sequential, restart-auditable authoring of all 806 V3 class manifests."""
from __future__ import annotations
import csv, hashlib, json, os, subprocess, sys, traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(r"D:\work\revise"); BASE=ROOT/"production_code/escalations/degree24_v3_repair"
SCOPE=BASE/"DEG24_SPLIT_HEAVY_KEYS_V3.tsv"; JOBS=BASE/"DEG24_MANIFEST_ALL_JOBS_V3.json"
STATUS=BASE/"DEG24_MANIFEST_AUTHORING_CONTROLLER_STATUS_V3.json"; PROGRESS=BASE/"DEG24_MANIFEST_AUTHORING_CONTROLLER_PROGRESS_V3.tsv"
LOCK=BASE/"DEG24_MANIFEST_AUTHORING_CONTROLLER_V3.lock"; BUILDER=BASE/"build_key_authoritative_manifest_v3_gpt5.py"

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p):
 d=hashlib.sha256()
 with p.open("rb") as h:
  for chunk in iter(lambda:h.read(8*1024*1024),b""): d.update(chunk)
 return d.hexdigest()
def atomic_json(path,obj):
 tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); os.replace(tmp,path)
def wsl_path(path): return "/mnt/d/work/revise/"+path.relative_to(ROOT).as_posix()
def source_valid(path,classes):
 if not path.exists(): return False
 count=0; last=""
 with path.open(encoding="utf-8") as h:
  for line in h:
   last=line.rstrip("\r\n")
   if line.startswith("CLASS\t"): count+=1
 return count==classes and last=="DONE"
def manifest_valid(key,classes):
 d=BASE/f"manifests/24T{key}"; js=d/f"DEG24_KEY_24T{key}_CLASS_MANIFEST_V3.json"
 if not js.exists(): return False
 try:
  m=json.loads(js.read_text(encoding="utf-8")); tsv=ROOT/m["manifest"]; gap=ROOT/m["gap_manifest"]
  return m["key_id"]==f"24T{key}" and m["class_count"]==classes and m["class_id_count"]==classes and tsv.exists() and gap.exists() and sha(tsv)==m["manifest_sha256"] and sha(gap)==m["gap_manifest_sha256"]
 except Exception: return False
def append_progress(event,key,completed,detail):
 new=not PROGRESS.exists()
 with PROGRESS.open("a",encoding="utf-8",newline="\n") as h:
  if new: h.write("utc\tevent\tkey\tcompleted\ttotal\tdetail\n")
  h.write(f"{now()}\t{event}\t24T{key}\t{completed}\t806\t{detail}\n")
def main():
 BASE.mkdir(parents=True,exist_ok=True)
 try:
  fd=os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.write(fd,f"pid={os.getpid()} utc={now()}\n".encode()); os.close(fd)
 except FileExistsError: raise SystemExit("controller lock exists; refuse duplicate")
 try:
  expected={int(r["key"]):int(r["old_class_units"]) for r in csv.DictReader(SCOPE.open(encoding="utf-8"),delimiter="\t")}
  jobs=json.loads(JOBS.read_text(encoding="utf-8"))["jobs"]
  if len(jobs)!=806 or {j["key"] for j in jobs}!=set(expected): raise ValueError("job registry mismatch")
  completed=sum(manifest_valid(k,c) for k,c in expected.items())
  atomic_json(STATUS,dict(schema="DEG24_MANIFEST_AUTHORING_CONTROLLER_V3",status="RUNNING",stage="MANIFEST_AUTHORING",completed=completed,total=806,updated_utc=now()))
  for job in jobs:
   key=int(job["key"]); classes=expected[key]
   if manifest_valid(key,classes): continue
   source=ROOT/job["output"]; wrapper=ROOT/job["wrapper"]
   if not source_valid(source,classes):
    if source.exists(): raise RuntimeError(f"incomplete source exists and is preserved: {source}")
    atomic_json(STATUS,dict(schema="DEG24_MANIFEST_AUTHORING_CONTROLLER_V3",status="RUNNING",stage="EXPORT_SOURCE",current_key=f"24T{key}",completed=completed,total=806,updated_utc=now()))
    proc=subprocess.run(["wsl.exe","gap","-q",wsl_path(wrapper)],cwd=ROOT,capture_output=True,text=True)
    (BASE/f"manifest_logs/24T{key}").mkdir(parents=True,exist_ok=True)
    (BASE/f"manifest_logs/24T{key}/stdout.txt").write_text(proc.stdout,encoding="utf-8",newline="\n")
    (BASE/f"manifest_logs/24T{key}/stderr.txt").write_text(proc.stderr,encoding="utf-8",newline="\n")
    if proc.returncode!=0 or f"MANIFEST_SOURCE_PASS\t24T{key}\tCLASSES\t{classes}" not in proc.stdout or not source_valid(source,classes): raise RuntimeError(f"GAP manifest export failed for 24T{key}, rc={proc.returncode}")
   atomic_json(STATUS,dict(schema="DEG24_MANIFEST_AUTHORING_CONTROLLER_V3",status="RUNNING",stage="SEAL_MANIFEST",current_key=f"24T{key}",completed=completed,total=806,updated_utc=now()))
   proc=subprocess.run([sys.executable,str(BUILDER),str(key)],cwd=ROOT,capture_output=True,text=True)
   (BASE/f"manifest_logs/24T{key}/builder_stdout.txt").write_text(proc.stdout,encoding="utf-8",newline="\n")
   (BASE/f"manifest_logs/24T{key}/builder_stderr.txt").write_text(proc.stderr,encoding="utf-8",newline="\n")
   if proc.returncode!=0 or not manifest_valid(key,classes): raise RuntimeError(f"manifest sealing failed for 24T{key}, rc={proc.returncode}")
   completed+=1; append_progress("MANIFEST_COMPLETE",key,completed,f"classes={classes};route={job['route']}")
  atomic_json(STATUS,dict(schema="DEG24_MANIFEST_AUTHORING_CONTROLLER_V3",status="ALL_MANIFESTS_COMPLETE_WAITING_COVERAGE_PLAN",stage="MANIFEST_AUTHORING_COMPLETE",completed=806,total=806,updated_utc=now()))
  print("ALL_806_MANIFESTS_COMPLETE")
 except Exception as exc:
  atomic_json(STATUS,dict(schema="DEG24_MANIFEST_AUTHORING_CONTROLLER_V3",status="STOPPED_REQUIRES_GPT56SOL_RECOVERY",stage="MANIFEST_AUTHORING",error=str(exc),traceback=traceback.format_exc(),updated_utc=now()))
  print(traceback.format_exc(),file=sys.stderr); raise
 finally:
  if LOCK.exists(): LOCK.unlink()
if __name__=="__main__": main()
