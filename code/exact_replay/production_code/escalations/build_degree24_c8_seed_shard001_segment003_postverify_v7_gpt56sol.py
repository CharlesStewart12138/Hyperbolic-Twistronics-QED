from __future__ import annotations

import hashlib
from pathlib import Path


base = Path(__file__).resolve().parent
source = base / "gap_run_degree24_c8_seed_shard001_segment003_unit8115_14622_retry_v6_gpt56sol.g"
target = base / "gap_run_degree24_c8_seed_shard001_segment003_unit8115_14622_postverify_v7_gpt56sol.g"
runner = base / "run_degree24_c8_seed_shard001_segment003_postverify_v7.sh"
output_v6 = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_UNIT8115_14622_RETRY_V6_GPT56SOL.txt"
output_v7 = "GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD001_SEGMENT003_UNIT8115_14622_POSTVERIFY_V7_GPT56SOL.txt"
assert source.is_file()
assert not target.exists() and not runner.exists() and not (base / output_v7).exists()

text = source.read_text(encoding="ascii")
assert text.count(output_v6) == 1
text = text.replace(output_v6, output_v7)
old = '''IO_rename:=function(oldpath,newpath)
 local attempt,result;
 for attempt in [1..S001_RENAME_RETRY_MAX] do
  result:=S001_RAW_IO_RENAME(oldpath,newpath);
  if result=true then
   if attempt>1 then Print("ATOMIC_RENAME_RETRY_SUCCESS\\tATTEMPTS\\t",attempt,"\\n"); fi;
   return true;
  fi;
  IO_select([],[],[],0,S001_RENAME_RETRY_USEC);
 od;
 Print("ATOMIC_RENAME_RETRY_EXHAUSTED\\tATTEMPTS\\t",S001_RENAME_RETRY_MAX,"\\n");
 return false;
end;'''
new = '''IO_rename:=function(oldpath,newpath)
 local attempt,result,expectedText;
 if not IsExistingFile(oldpath) then return false; fi;
 expectedText:=StringFile(oldpath);
 for attempt in [1..S001_RENAME_RETRY_MAX] do
  result:=S001_RAW_IO_RENAME(oldpath,newpath);
  if result=true then
   if IsExistingFile(oldpath) or not IsExistingFile(newpath) or StringFile(newpath)<>expectedText then
    Print("ATOMIC_RENAME_POSTVERIFY_FAIL\\tATTEMPTS\\t",attempt,"\\n");
    return false;
   fi;
   if attempt>1 then Print("ATOMIC_RENAME_RETRY_SUCCESS\\tATTEMPTS\\t",attempt,"\\n"); fi;
   return true;
  fi;
  IO_select([],[],[],0,S001_RENAME_RETRY_USEC);
 od;
 Print("ATOMIC_RENAME_RETRY_EXHAUSTED\\tATTEMPTS\\t",S001_RENAME_RETRY_MAX,"\\n");
 return false;
end;'''
assert text.count(old) == 1
text = text.replace(old, new)
target.write_text(text, encoding="ascii", newline="\n")
runner.write_text(
    "#!/usr/bin/env bash\n"
    "set -euo pipefail\n"
    "ulimit -v 50331648\n"
    "exec /usr/bin/timeout --signal=TERM --kill-after=10s 1400s /usr/bin/time -v gap -q "
    f"/mnt/d/work/revise/production_code/escalations/{target.name}\n",
    encoding="ascii", newline="\n",
)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
print(f"POSTVERIFY_BUILD_PASS\tWRAPPER\t{target.name}\tSHA256\t{sha(target)}")
print(f"RUNNER\t{runner.name}\tSHA256\t{sha(runner)}")
