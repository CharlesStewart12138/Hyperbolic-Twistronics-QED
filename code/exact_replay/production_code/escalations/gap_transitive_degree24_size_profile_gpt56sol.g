# Exact read-only order-window profile for a fixed slice of TransitiveGroup(24,k).
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
smin:=GetEnv("BOLZA24_KMIN"); smax:=GetEnv("BOLZA24_KMAX");
if smin=fail then kmin:=1; else kmin:=Int(smin); fi;
if smax=fail then kmax:=NrTransitiveGroups(24); else kmax:=Int(smax); fi;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_SIZE_",String(kmin),"_",String(kmax),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SIZE\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDATABASE\t",NrTransitiveGroups(24),"\nRANGE\t",kmin,"\t",kmax,"\n",
 "SCOPE\tExact Size(TransitiveGroup(24,k)); retain actual orders 2338 through 50000 inclusive. No automorphism group is constructed.\n");
window:=0; processed:=0; start:=Runtime();
for k in [kmin..kmax] do
 G:=TransitiveGroup(24,k); n:=Size(G); processed:=processed+1;
 if n>=2338 and n<=50000 then window:=window+1; AppendTo(OUT,"ENTRY\t24T",k,"\tORDER\t",n,"\n"); fi;
 if processed mod 250=0 then AppendTo(OUT,"CHECKPOINT\tK\t",k,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tMS\t",Runtime()-start,"\n"); fi;
od;
AppendTo(OUT,"TOTAL_SLICE\tRANGE\t",kmin,"\t",kmax,"\tPROCESSED\t",processed,"\tORDER_WINDOW\t",window,"\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
