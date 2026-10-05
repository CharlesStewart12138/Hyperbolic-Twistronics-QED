SetInfoLevel(InfoWarning,0);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if LoadPackage("io")=fail then Error("IO package required"); fi;

rawIORename:=IO_rename;
MakeReadWriteGlobal("IO_rename");
forcedFailurePending:=true;
IO_rename:=function(oldpath,newpath)
 local attempt,result;
 for attempt in [1..100] do
  if forcedFailurePending then
   result:=fail;
   forcedFailurePending:=false;
  else
   result:=rawIORename(oldpath,newpath);
  fi;
  if result=true then
   Print("ATOMIC_RENAME_ATTEMPTS\t",attempt,"\n");
   return true;
  fi;
  IO_select([],[],[],0,10000);
 od;
 return false;
end;

source:="/mnt/d/work/revise/production_code/escalations/GAP_IO_RENAME_RETRY_PROBE_TMP_GPT56SOL.txt";
target:="/mnt/d/work/revise/production_code/escalations/GAP_IO_RENAME_RETRY_PROBE_TARGET_GPT56SOL.txt";
if IsExistingFile(source) or IsExistingFile(target) then Error("probe paths already exist"); fi;
PrintTo(target,"OLD\n");
PrintTo(source,"NEW\n");
if IO_rename(source,target)<>true then Error("retry rename failed"); fi;
if IsExistingFile(source) or StringFile(target)<>"NEW\n" then Error("retry rename postcondition"); fi;
Print("IO_RENAME_RETRY_OVERRIDE_PASS\n");
QUIT_GAP(0);
