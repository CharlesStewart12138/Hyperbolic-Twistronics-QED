# Exact Aut(G)/order-8-class profile for one TARGET_DEGREE key slice. No seeds.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if not IsBound(TARGET_DEGREE) or not IsBound(KMIN) or not IsBound(KMAX) then Error("wrapper variables missing"); fi;
d:=TARGET_DEGREE; guardMs:=1400000;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE",String(d),"_AUT_PROFILE_",String(KMIN),"_",String(KMAX),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-AUT-PROFILE\nDEGREE\t",d,"\nRANGE\t",KMIN,"\t",KMAX,"\nGUARD_MS\t",guardMs,"\nSCOPE\tExact Aut(G) and exact-order-8 conjugacy classes for every parity-capable order-window target; no seed enumeration.\n");
processed:=0; classes:=0; raw:=0; autMs:=0; classMs:=0; stopped:=false; start:=Runtime();
for k in [KMIN..KMAX] do
 G:=TransitiveGroup(d,k); n:=Size(G);
 if n>=2338 and n<=50000 then maps:=GQuotients(G,CyclicGroup(2)); if Length(maps)>0 then
  t:=Runtime(); A:=AutomorphismGroup(G); aMs:=Runtime()-t; t:=Runtime();
  if IsSolvableGroup(A) then iso:=IsomorphismPcGroup(A); cc:=ConjugacyClasses(Image(iso)); method:="pc";
  else cc:=ConjugacyClasses(A); method:="native"; fi;
  c8:=Filtered(cc,c->Order(Representative(c))=8); cMs:=Runtime()-t;
  processed:=processed+1; classes:=classes+Length(c8); raw:=raw+n*Length(c8); autMs:=autMs+aMs; classMs:=classMs+cMs;
  AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tAUT_MS\t",aMs,
   "\tMETHOD\t",method,"\tCLASS_MS\t",cMs,"\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",n*Length(c8),"\n");
 fi; fi;
 if Runtime()-start>=guardMs then stopped:=true; break; fi;
od;
if stopped then AppendTo(OUT,"TOTAL_PARTIAL\tDEGREE\t",d,"\tRANGE\t",KMIN,"\t",KMAX,"\tLAST_K\t",k,"\tPROCESSED\t",processed,"\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,"\tAUT_MS\t",autMs,"\tCLASS_MS\t",classMs,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
else AppendTo(OUT,"TOTAL\tDEGREE\t",d,"\tRANGE\t",KMIN,"\t",KMAX,"\tPROCESSED\t",processed,"\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,"\tAUT_MS\t",autMs,"\tCLASS_MS\t",classMs,"\tMS\t",Runtime()-start,"\nDONE\n"); fi;
Print("WROTE ",OUT,"\n"); QUIT;
