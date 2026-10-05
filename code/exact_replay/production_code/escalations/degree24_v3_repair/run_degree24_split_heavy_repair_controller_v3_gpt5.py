#!/usr/bin/env python3
"""Run the V3 explicit-CLASS_ID repair plan with atomic class checkpoints."""
from __future__ import annotations
import csv, hashlib, json, os, re, subprocess, traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(r"D:\work\revise"); BASE=ROOT/"production_code/escalations/degree24_v3_repair"
PLAN=BASE/"DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.tsv"; PLAN_META=BASE/"DEG24_SPLIT_HEAVY_REPAIR_PLAN_V3.json"; COVERAGE=BASE/"DEG24_SPLIT_HEAVY_COVERAGE_CERTIFICATE_V3.json"
ENGINE=BASE/"gap_run_degree24_split_heavy_segment_v3.g"; STATUS=BASE/"DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_STATUS_V3.json"; PROGRESS=BASE/"DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_PROGRESS_V3.tsv"; LOCK=BASE/"DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3.lock"
WRAPPERS=BASE/"repair_wrappers"; OUTPUTS=BASE/"repair_outputs"; CHECKPOINTS=BASE/"repair_checkpoints"; LOGS=BASE/"repair_logs"; COMPLETIONS=BASE/"repair_completions"
COUNTER_FIELDS=["CUM_UNITS","CUM_RAW","CUM_INVARIANT_ALPHA","CUM_BETA","CUM_INVERSE","CUM_INVERSE_ODD","CUM_ORBIT8","CUM_RELATOR","CUM_B3","CUM_GENERATE","CUM_CENTRALIZER_ORBITS","CUM_CANDIDATE_NUMERIC"]
def now(): return datetime.now(timezone.utc).isoformat()
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
 d=hashlib.sha256()
 with p.open("rb") as h:
  for chunk in iter(lambda:h.read(8*1024*1024),b""): d.update(chunk)
 return d.hexdigest()
def atomic_json(path,obj):
 tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); os.replace(tmp,path)
def wsl_path(p): return "/mnt/d/work/revise/"+p.relative_to(ROOT).as_posix()
def win_from_wsl(s):
 prefix="/mnt/d/work/revise/"
 if not s.startswith(prefix): raise ValueError(f"unexpected output path {s}")
 return ROOT/s[len(prefix):]
def parse_pairs(tokens):
 if len(tokens)%2: raise ValueError("odd key/value token count")
 return {tokens[i]:tokens[i+1] for i in range(0,len(tokens),2)}
def read_checkpoint(path,row):
 raw=path.read_bytes(); text=raw.decode("utf-8"); lines=text.splitlines()
 if len(lines)!=3 or lines[0]!="CERTIFICATE_CHECKPOINT\tDEG24_SPLIT_HEAVY_REPAIR_V3" or lines[2]!="DONE": raise ValueError("checkpoint envelope")
 marker="\tPAYLOAD_SHA256\t"; payload,claimed=lines[1].rsplit(marker,1)
 if sha_bytes(payload.encode("utf-8"))!=claimed.lower(): raise ValueError("checkpoint payload hash")
 f=parse_pairs(payload.split("\t"))
 if f["SEGMENT_ID"]!=row["segment_id"] or f["SEGMENT_FILE_SHA256"].lower()!=row["segment_data_sha256"].lower(): raise ValueError("checkpoint segment binding")
 prev=win_from_wsl(f["OUTPUT_FILE"]); n=int(f["OUTPUT_PREFIX_BYTES"]); data=prev.read_bytes()
 if len(data)<n or sha_bytes(data[:n])!=f["OUTPUT_PREFIX_SHA256"].lower(): raise ValueError("checkpoint output prefix")
 counters=[int(f[name]) for name in COUNTER_FIELDS]
 return dict(start_index=int(f["NEXT_INDEX"]),counters=counters,checkpoint_sha256=sha_bytes(raw),previous_output=prev,previous_output_prefix_bytes=n,previous_output_prefix_sha256=f["OUTPUT_PREFIX_SHA256"].lower(),last_class_id=f["LAST_CLASS_ID_V3"])
def completion_valid(row):
 p=COMPLETIONS/f"{row['segment_id']}_COMPLETE_V3.json"
 if not p.exists(): return False
 try:
  c=json.loads(p.read_text(encoding="utf-8")); return c["segment_id"]==row["segment_id"] and c["segment_data_sha256"]==row["segment_data_sha256"] and c["class_units"]==int(row["class_count"]) and c["raw_pairs"]==int(row["raw_pairs"]) and all((ROOT/x["path"]).exists() and sha_file(ROOT/x["path"])==x["sha256"] for x in c["output_parts"])
 except Exception: return False
def parse_total(path):
 total=None
 for line in path.read_text(encoding="utf-8").splitlines():
  if line.startswith("TOTAL\t"): total=parse_pairs(line.split("\t")[1:])
 return total
def finalize(row,out,checkpoint):
 total=parse_total(out)
 if not total or int(total["CLASS_UNITS"])!=int(row["class_count"]) or int(total["RAW_PAIRS"])!=int(row["raw_pairs"]): raise ValueError("terminal TOTAL mismatch")
 parts=[]
 for p in sorted(OUTPUTS.glob(f"{row['segment_id']}_ATTEMPT*_V3.txt")):
  parts.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha_file(p)))
 cert=dict(schema="DEG24_SPLIT_HEAVY_REPAIR_SEGMENT_COMPLETE_V3",segment_id=row["segment_id"],key_id=row["key_id"],class_units=int(total["CLASS_UNITS"]),raw_pairs=int(total["RAW_PAIRS"]),candidate_numeric=int(total["CANDIDATE_NUMERIC"]),segment_data_sha256=row["segment_data_sha256"],class_id_list_sha256=row["class_id_list_sha256"],final_checkpoint=checkpoint.relative_to(ROOT).as_posix(),final_checkpoint_sha256=sha_file(checkpoint),output_parts=parts,status="COMPLETE",completed_utc=now())
 atomic_json(COMPLETIONS/f"{row['segment_id']}_COMPLETE_V3.json",cert); return cert
def append_progress(event,row,done,total,detail):
 new=not PROGRESS.exists()
 with PROGRESS.open("a",encoding="utf-8",newline="\n") as h:
  if new: h.write("utc\tevent\tsegment_id\tkey_id\tcompleted\ttotal\tdetail\n")
  h.write(f"{now()}\t{event}\t{row['segment_id']}\t{row['key_id']}\t{done}\t{total}\t{detail}\n")
def wrapper_text(row,attempt,state,out,checkpoint,tmp):
 counters=",".join(str(x) for x in state["counters"])
 return (f"SEGMENT_FILE:=\"{wsl_path(ROOT/row['segment_data'])}\"; EXPECTED_SEGMENT_FILE_SHA256:=\"{row['segment_data_sha256']}\";\nOUT:=\"{wsl_path(out)}\"; CHECKPOINT_FILE:=\"{wsl_path(checkpoint)}\"; CHECKPOINT_TMP:=\"{wsl_path(tmp)}\";\nSTART_INDEX:={state['start_index']}; INITIAL_COUNTERS:=[{counters}]; PREVIOUS_CHECKPOINT_SHA256:=\"{state['checkpoint_sha256']}\";\nPREVIOUS_OUTPUT_FILE:=\"{wsl_path(state['previous_output']) if state['previous_output'] else 'NONE_FRESH_START'}\"; PREVIOUS_OUTPUT_PREFIX_BYTES:={state['previous_output_prefix_bytes']}; PREVIOUS_OUTPUT_PREFIX_SHA256:=\"{state['previous_output_prefix_sha256']}\";\nINTERNAL_GUARD_MS:=1320000; STOP_AFTER_INDEX:=fail;\nRead(\"{wsl_path(ENGINE)}\");\n")
def main():
 for d in (WRAPPERS,OUTPUTS,CHECKPOINTS,LOGS,COMPLETIONS): d.mkdir(parents=True,exist_ok=True)
 try:
  fd=os.open(LOCK,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.write(fd,f"pid={os.getpid()} utc={now()}\n".encode()); os.close(fd)
 except FileExistsError: raise SystemExit("repair controller lock exists; refuse duplicate")
 try:
  plan_meta=json.loads(PLAN_META.read_text(encoding="utf-8")); coverage=json.loads(COVERAGE.read_text(encoding="utf-8"))
  if plan_meta["status"]!="PASS" or coverage["status"]!="PASS" or coverage["coverage_missing_count"]!=0 or coverage["coverage_duplicate_count"]!=0: raise ValueError("coverage gate not PASS")
  rows=list(csv.DictReader(PLAN.open(encoding="utf-8"),delimiter="\t")); total_segments=len(rows); done=sum(completion_valid(r) for r in rows)
  atomic_json(STATUS,dict(schema="DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3",status="RUNNING",stage="AFFECTED_DOMAIN_RECOMPUTATION",completed_segments=done,total_segments=total_segments,completed_keys=len({r['key_id'] for r in rows if completion_valid(r)}),total_keys=806,updated_utc=now()))
  for row in rows:
   if completion_valid(row): continue
   checkpoint=CHECKPOINTS/f"{row['segment_id']}_CHECKPOINT_V3.txt"; tmp=CHECKPOINTS/f"{row['segment_id']}_CHECKPOINT_TMP_V3.txt"
   if tmp.exists(): raise RuntimeError(f"stale checkpoint tmp preserved: {tmp}")
   if checkpoint.exists(): state=read_checkpoint(checkpoint,row)
   else: state=dict(start_index=1,counters=[0]*12,checkpoint_sha256="NONE_FRESH_START",previous_output=None,previous_output_prefix_bytes=0,previous_output_prefix_sha256="NONE_FRESH_START",last_class_id=None)
   while True:
    attempt=len(list(OUTPUTS.glob(f"{row['segment_id']}_ATTEMPT*_V3.txt")))+1; out=OUTPUTS/f"{row['segment_id']}_ATTEMPT{attempt:03d}_V3.txt"; wrapper=WRAPPERS/f"{row['segment_id']}_ATTEMPT{attempt:03d}_V3.g"
    if out.exists() or wrapper.exists(): raise RuntimeError("attempt path collision")
    wrapper.write_text(wrapper_text(row,attempt,state,out,checkpoint,tmp),encoding="utf-8",newline="\n")
    atomic_json(STATUS,dict(schema="DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3",status="RUNNING",stage="SEGMENT_EXECUTION",current_segment=row["segment_id"],current_key=row["key_id"],start_index=state["start_index"],completed_segments=done,total_segments=total_segments,updated_utc=now()))
    proc=subprocess.run(["wsl.exe","timeout","--signal=TERM","--kill-after=10s","1400s","gap","-q",wsl_path(wrapper)],cwd=ROOT,capture_output=True,text=True)
    (LOGS/f"{row['segment_id']}_ATTEMPT{attempt:03d}_STDOUT.txt").write_text(proc.stdout,encoding="utf-8",newline="\n"); (LOGS/f"{row['segment_id']}_ATTEMPT{attempt:03d}_STDERR.txt").write_text(proc.stderr,encoding="utf-8",newline="\n")
    if proc.returncode!=0 or not out.exists(): raise RuntimeError(f"unexpected segment termination {row['segment_id']} attempt {attempt} rc={proc.returncode}")
    text=out.read_text(encoding="utf-8")
    if text.endswith("DONE\n") and "\nTOTAL\t" in text:
     cert=finalize(row,out,checkpoint); done+=1; append_progress("SEGMENT_COMPLETE",row,done,total_segments,f"raw={cert['raw_pairs']};candidates={cert['candidate_numeric']}"); break
    if "STOPPED_GUARD\n" not in text: raise RuntimeError(f"nonterminal segment output without normal guard stop: {row['segment_id']}")
    state=read_checkpoint(checkpoint,row); append_progress("SEGMENT_GUARD_RESUME",row,done,total_segments,f"next_index={state['start_index']}")
  certs=[json.loads(p.read_text(encoding="utf-8")) for p in sorted(COMPLETIONS.glob("*_COMPLETE_V3.json"))]
  atomic_json(STATUS,dict(schema="DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3",status="ALL_AFFECTED_SEGMENTS_COMPLETE",stage="AFFECTED_DOMAIN_RECOMPUTATION_COMPLETE",completed_segments=total_segments,total_segments=total_segments,completed_keys=806,total_keys=806,class_units=sum(c["class_units"] for c in certs),raw_pairs=sum(c["raw_pairs"] for c in certs),candidate_numeric=sum(c["candidate_numeric"] for c in certs),updated_utc=now()))
  print("ALL_AFFECTED_SEGMENTS_COMPLETE")
 except Exception as exc:
  atomic_json(STATUS,dict(schema="DEG24_SPLIT_HEAVY_REPAIR_CONTROLLER_V3",status="STOPPED_REQUIRES_GPT56SOL_RECOVERY",stage="AFFECTED_DOMAIN_RECOMPUTATION",error=str(exc),traceback=traceback.format_exc(),updated_utc=now()))
  print(traceback.format_exc(),file=sys.stderr); raise
 finally:
  if LOCK.exists(): LOCK.unlink()
if __name__=="__main__": main()
