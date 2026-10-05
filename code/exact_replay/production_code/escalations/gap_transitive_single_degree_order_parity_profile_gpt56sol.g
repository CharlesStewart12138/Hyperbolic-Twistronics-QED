# Exact cheap order-window and C2-parity profile for TARGET_DEGREE.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if not IsBound(TARGET_DEGREE) then Error("TARGET_DEGREE must be bound by wrapper"); fi;
d:=TARGET_DEGREE; db:=NrTransitiveGroups(d); guardMs:=1400000;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE",String(d),"_ORDER_PARITY_PROFILE_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE",d,"-ORDER-PARITY\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDEGREE\t",d,"\nDATABASE\t",db,"\nGUARD_MS\t",guardMs,"\n",
 "SCOPE\tExact Size and GQuotients(G,C2) only; no automorphism group or seed scan.\n");
window:=0; parity:=0; stopped:=false; start:=Runtime();
for k in [1..db] do
 G:=TransitiveGroup(d,k); n:=Size(G);
 if n>=2338 and n<=50000 then window:=window+1; maps:=GQuotients(G,CyclicGroup(2)); m:=Length(maps);
  if m>0 then parity:=parity+1; fi;
  AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",m,"\n");
 fi;
 if k mod 100=0 then AppendTo(OUT,"CHECKPOINT\tK\t",k,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tMS\t",Runtime()-start,"\n"); fi;
 if Runtime()-start>=guardMs then stopped:=true; break; fi;
od;
if stopped then AppendTo(OUT,"TOTAL_PARTIAL\tDEGREE\t",d,"\tDATABASE\t",db,"\tLAST_K\t",k,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
else AppendTo(OUT,"TOTAL\tDEGREE\t",d,"\tDATABASE\t",db,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tMS\t",Runtime()-start,"\nDONE\n"); fi;
Print("WROTE ",OUT,"\n"); QUIT;
