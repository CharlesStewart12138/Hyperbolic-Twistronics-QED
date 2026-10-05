SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSGRP_DEGREES32_47_AVAILABILITY_GPT56SOL.txt";;
PrintTo(OUT,"CERTIFICATE_PROFILE\tTRANSGRP-AVAILABILITY-32-47\nGAP_VERSION\t",GAPInfo.Version,"\n");;
if not IsBound(TransitiveGroupsAvailable) then
 AppendTo(OUT,"FUNCTION\tTransitiveGroupsAvailable\tUNBOUND\n");;
else
 for d in [32..47] do
  a:=TransitiveGroupsAvailable(d);;
  AppendTo(OUT,"DEGREE\t",d,"\tAVAILABLE\t",a);;
  if a then AppendTo(OUT,"\tDATABASE\t",NrTransitiveGroups(d));; fi;;
  AppendTo(OUT,"\n");;
 od;;
fi;;
AppendTo(OUT,"DONE\n");;
QUIT;;
