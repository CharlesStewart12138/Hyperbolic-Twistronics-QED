# Guarded Aut(G)+exact-order-8-class forecast on a deterministic degree-24 sample.
# SAMPLE_KEYS and SAMPLE_LABEL are fixed by wrappers. No physical seeds are scanned.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if not IsBound(SAMPLE_KEYS) then Error("SAMPLE_KEYS must be bound by wrapper"); fi;
if not IsBound(SAMPLE_LABEL) then Error("SAMPLE_LABEL must be bound by wrapper"); fi;
guardMs:=300000;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_FORECAST_",SAMPLE_LABEL,"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SAMPLE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-FORECAST\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nLABEL\t",SAMPLE_LABEL,"\nKEYS\t",SAMPLE_KEYS,"\nGUARD_MS\t",guardMs,"\n",
 "SCOPE\tExact Aut(G) and exact-order-8 Aut(G)-class count for fixed sample keys only; no seed enumeration.\n");
processed:=0; classes:=0; raw:=0; autTime:=0; classTime:=0; stopped:=false; start:=Runtime();
for k in SAMPLE_KEYS do
 G:=TransitiveGroup(24,k); n:=Size(G); maps:=GQuotients(G,CyclicGroup(2));
 if not (n>=2338 and n<=50000 and Length(maps)>0) then Error("sample contract failure at ",k); fi;
 sol:=IsSolvableGroup(G); t:=Runtime(); A:=AutomorphismGroup(G); aMs:=Runtime()-t;
 t:=Runtime();
 if IsSolvableGroup(A) then iso:=IsomorphismPcGroup(A); P:=Image(iso); cc:=ConjugacyClasses(P); method:="pc";
 else cc:=ConjugacyClasses(A); method:="native"; fi;
 c8:=Filtered(cc,c->Order(Representative(c))=8); cMs:=Runtime()-t;
 processed:=processed+1; classes:=classes+Length(c8); raw:=raw+n*Length(c8); autTime:=autTime+aMs; classTime:=classTime+cMs;
 AppendTo(OUT,"ENTRY\t24T",k,"\tORDER\t",n,"\tSOLVABLE\t",sol,"\tPARITY_MAPS\t",Length(maps),
  "\tAUT_ORDER\t",Size(A),"\tAUT_MS\t",aMs,"\tMETHOD\t",method,"\tCLASS_MS\t",cMs,
  "\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",n*Length(c8),"\tTOTAL_MS\t",Runtime()-start,"\n");
 if Runtime()-start>=guardMs then stopped:=true; break; fi;
od;
if stopped then
 AppendTo(OUT,"TOTAL_PARTIAL\tLABEL\t",SAMPLE_LABEL,"\tPROCESSED\t",processed,"\tREQUESTED\t",Length(SAMPLE_KEYS),
  "\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,"\tAUT_MS\t",autTime,"\tCLASS_MS\t",classTime,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
else
 AppendTo(OUT,"TOTAL_SAMPLE\tLABEL\t",SAMPLE_LABEL,"\tPROCESSED\t",processed,"\tREQUESTED\t",Length(SAMPLE_KEYS),
  "\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,"\tAUT_MS\t",autTime,"\tCLASS_MS\t",classTime,"\tMS\t",Runtime()-start,"\nDONE\n");
fi;
Print("WROTE ",OUT,"\n"); QUIT;
