# Checkpoint-safe exact degree-24 Aut/order-8 profile on isomorphic pc domains.
# The wrapper binds KMIN, KMAX, PROFILE_GUARD_MS, EXPECTED_WINDOW, and
# EXPECTED_PARITY.  This recovery source enumerates no seed predicate.
# Conjugation by each exact isomorphism G -> P identifies Aut(G) with Aut(P),
# preserving automorphism orders and conjugacy classes; |G|=|P| preserves raw.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if not IsBound(KMIN) or not IsBound(KMAX) or not IsBound(PROFILE_GUARD_MS) or
   not IsBound(EXPECTED_WINDOW) or not IsBound(EXPECTED_PARITY) then
 Error("wrapper variables missing");
fi;
d:=24; db:=NrTransitiveGroups(d);
if KMIN<1 or KMAX<KMIN or KMAX>db then Error("invalid catalogue range"); fi;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_",
 String(KMIN),"_",String(KMAX),"_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDATABASE\t",db,"\nRANGE\t",KMIN,"\t",KMAX,"\n",
 "GUARD_MS\t",PROFILE_GUARD_MS,"\nEXPECTED_ORDER_WINDOW\t",EXPECTED_WINDOW,"\nEXPECTED_PARITY\t",EXPECTED_PARITY,"\n",
 "SCOPE\tExact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds.\n",
 "RECOVERY\tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.\n");
window:=0; processed:=0; classes:=0; raw:=0; isoMs:=0; autMs:=0; classMs:=0;
start:=Runtime(); stopped:=false; lastComplete:=KMIN-1;
for k in [KMIN..KMAX] do
 G:=TransitiveGroup(d,k); n:=Size(G);
 if n>=2338 and n<=50000 then
  window:=window+1; mapsG:=GQuotients(G,CyclicGroup(2));
  if Length(mapsG)>0 then
   solG:=IsSolvableGroup(G);
   if not solG then Error("pc-domain recovery encountered a nonsolvable target"); fi;
   t:=Runtime(); isoG:=IsomorphismPcGroup(G); P:=Image(isoG); oneIsoMs:=Runtime()-t;
   if Size(P)<>n then Error("pc image order mismatch"); fi;
   mapsP:=GQuotients(P,CyclicGroup(2));
   if Length(mapsP)<>Length(mapsG) then Error("parity quotient count mismatch under isomorphism"); fi;
   t:=Runtime(); A:=AutomorphismGroup(P); oneAutMs:=Runtime()-t; t:=Runtime();
   if IsSolvableGroup(A) then isoA:=IsomorphismPcGroup(A); cc:=ConjugacyClasses(Image(isoA)); method:="pc";
   else cc:=ConjugacyClasses(A); method:="native"; fi;
   c8:=Filtered(cc,c->Order(Representative(c))=8); oneClassMs:=Runtime()-t;
   processed:=processed+1; classes:=classes+Length(c8); raw:=raw+n*Length(c8);
   isoMs:=isoMs+oneIsoMs; autMs:=autMs+oneAutMs; classMs:=classMs+oneClassMs;
   AppendTo(OUT,"ENTRY\t24T",k,"\tORDER\t",n,"\tSOLVABLE_G\t",solG,
    "\tPARITY_MAPS_G\t",Length(mapsG),"\tPC_ORDER\t",Size(P),
    "\tPARITY_MAPS_P\t",Length(mapsP),"\tAUT_ORDER\t",Size(A),"\tISO_MS\t",oneIsoMs,
    "\tAUT_MS\t",oneAutMs,"\tMETHOD\t",method,"\tCLASS_MS\t",oneClassMs,
    "\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",n*Length(c8),"\n",
    "CHECKPOINT\tLAST_COMPLETE_K\t",k,"\tPROCESSED\t",processed,
    "\tISO_MS\t",isoMs,"\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,
    "\tMS\t",Runtime()-start,"\n");
  fi;
 fi;
 lastComplete:=k;
 if k mod 25=0 then
  AppendTo(OUT,"SCAN_CHECKPOINT\tLAST_COMPLETE_K\t",k,"\tORDER_WINDOW\t",window,
   "\tPROCESSED\t",processed,"\tISO_MS\t",isoMs,"\tORDER8_CLASSES\t",classes,
   "\tRAW_PAIRS\t",raw,"\tMS\t",Runtime()-start,"\n");
 fi;
 if Runtime()-start>=PROFILE_GUARD_MS then stopped:=true; break; fi;
od;
if stopped then
 AppendTo(OUT,"TOTAL_PARTIAL\tDEGREE\t24\tDATABASE\t",db,"\tRANGE\t",KMIN,"\t",KMAX,
  "\tLAST_COMPLETE_K\t",lastComplete,"\tORDER_WINDOW\t",window,"\tPROCESSED\t",processed,
  "\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,"\tISO_MS\t",isoMs,
  "\tAUT_MS\t",autMs,"\tCLASS_MS\t",classMs,"\tMS\t",Runtime()-start,
  "\nSTOPPED_GUARD\n");
else
 if window<>EXPECTED_WINDOW or processed<>EXPECTED_PARITY then Error("profile expectation mismatch"); fi;
 AppendTo(OUT,"TOTAL\tDEGREE\t24\tDATABASE\t",db,"\tRANGE\t",KMIN,"\t",KMAX,
  "\tLAST_COMPLETE_K\t",lastComplete,"\tORDER_WINDOW\t",window,"\tPROCESSED\t",processed,
  "\tORDER8_CLASSES\t",classes,"\tRAW_PAIRS\t",raw,"\tISO_MS\t",isoMs,
  "\tAUT_MS\t",autMs,"\tCLASS_MS\t",classMs,"\tMS\t",Runtime()-start,"\nDONE\n");
fi;
Print("WROTE ",OUT,"\n"); QUIT;
