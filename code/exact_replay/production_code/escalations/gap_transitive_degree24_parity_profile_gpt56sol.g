# Exact read-only C2-quotient profile for a fixed slice of TransitiveGroup(24,k).
# No automorphism group is constructed. Internal CPU guard is below 25 minutes.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
smin:=GetEnv("BOLZA24_KMIN"); smax:=GetEnv("BOLZA24_KMAX");
if smin=fail then kmin:=1; else kmin:=Int(smin); fi;
if smax=fail then kmax:=NrTransitiveGroups(24); else kmax:=Int(smax); fi;
guardMs:=1400000;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_PARITY_",String(kmin),"_",String(kmax),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-PARITY\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDATABASE\t",NrTransitiveGroups(24),"\nRANGE\t",kmin,"\t",kmax,"\nGUARD_MS\t",guardMs,"\n",
 "SCOPE\tFor every actual order-window target, compute exact GQuotients(G,C2) count. No automorphism group is constructed.\n");
processed:=0; window:=0; parity:=0; stopped:=false; start:=Runtime();
for k in [kmin..kmax] do
 G:=TransitiveGroup(24,k); n:=Size(G); processed:=processed+1;
 if n>=2338 and n<=50000 then
  window:=window+1; maps:=GQuotients(G,CyclicGroup(2)); m:=Length(maps);
  AppendTo(OUT,"ENTRY\t24T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",m,"\n");
  if m>0 then parity:=parity+1; fi;
  if window mod 100=0 then AppendTo(OUT,"CHECKPOINT\tK\t",k,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tMS\t",Runtime()-start,"\n"); fi;
 fi;
 if Runtime()-start>=guardMs then stopped:=true; break; fi;
od;
if stopped then
 AppendTo(OUT,"TOTAL_PARTIAL\tRANGE\t",kmin,"\t",kmax,"\tLAST_K\t",k,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
else
 AppendTo(OUT,"TOTAL_SLICE\tRANGE\t",kmin,"\t",kmax,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tMS\t",Runtime()-start,"\nDONE\n");
fi;
Print("WROTE ",OUT,"\n"); QUIT;
