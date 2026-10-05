SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSGRP_DEGREE32_AVAILABILITY_GPT56SOL.txt";;
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");;
available:=true;;
if not IsBound(NrTransitiveGroups) then available:=false;; fi;;
if available then
  n:=NrTransitiveGroups(32);;
  AppendTo(OUT,"DEGREE\t32\tNR_TRANSITIVE_GROUPS\t",n,"\n");;
fi;;
AppendTo(OUT,"DONE\n");;
QUIT;;
