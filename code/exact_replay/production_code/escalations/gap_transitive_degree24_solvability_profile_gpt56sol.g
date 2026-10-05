# Exact read-only solvability stratification of parity-capable degree-24 targets.
# No automorphism group is constructed. Internal CPU guard is below 25 minutes.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
smin:=GetEnv("BOLZA24_KMIN"); smax:=GetEnv("BOLZA24_KMAX");
if smin=fail then kmin:=1; else kmin:=Int(smin); fi;
if smax=fail then kmax:=NrTransitiveGroups(24); else kmax:=Int(smax); fi;
guardMs:=1400000;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_SOLVABILITY_",String(kmin),"_",String(kmax),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SOLVABILITY\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDATABASE\t",NrTransitiveGroups(24),"\nRANGE\t",kmin,"\t",kmax,"\nGUARD_MS\t",guardMs,"\n",
 "SCOPE\tExact IsSolvableGroup for every order-window target having a C2 epimorphism. No automorphism group is constructed.\n");
processed:=0; window:=0; parity:=0; solvable:=0; nonsolvable:=0; stopped:=false; start:=Runtime();
for k in [kmin..kmax] do
 G:=TransitiveGroup(24,k); n:=Size(G); processed:=processed+1;
 if n>=2338 and n<=50000 then
  window:=window+1; maps:=GQuotients(G,CyclicGroup(2)); m:=Length(maps);
  if m>0 then
   parity:=parity+1; sol:=IsSolvableGroup(G);
   if sol then solvable:=solvable+1; flag:=1; else nonsolvable:=nonsolvable+1; flag:=0; fi;
   AppendTo(OUT,"ENTRY\t24T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",m,"\tSOLVABLE\t",flag,"\n");
   if parity mod 100=0 then AppendTo(OUT,"CHECKPOINT\tK\t",k,"\tPROCESSED\t",processed,"\tPARITY\t",parity,"\tSOLVABLE\t",solvable,"\tNONSOLVABLE\t",nonsolvable,"\tMS\t",Runtime()-start,"\n"); fi;
  fi;
 fi;
 if Runtime()-start>=guardMs then stopped:=true; break; fi;
od;
if stopped then
 AppendTo(OUT,"TOTAL_PARTIAL\tRANGE\t",kmin,"\t",kmax,"\tLAST_K\t",k,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tSOLVABLE\t",solvable,"\tNONSOLVABLE\t",nonsolvable,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
else
 AppendTo(OUT,"TOTAL_SLICE\tRANGE\t",kmin,"\t",kmax,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tPARITY\t",parity,"\tSOLVABLE\t",solvable,"\tNONSOLVABLE\t",nonsolvable,"\tMS\t",Runtime()-start,"\nDONE\n");
fi;
Print("WROTE ",OUT,"\n"); QUIT;
