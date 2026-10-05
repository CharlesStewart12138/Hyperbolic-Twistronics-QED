# Exact single-key Aut/order-8 profile transported to an isomorphic pc group.
# No seeds are enumerated.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if not IsBound(TARGET_DEGREE) or not IsBound(TARGET_KEY) or not IsBound(PROFILE_GUARD_MS) then Error("wrapper variables missing"); fi;
d:=TARGET_DEGREE; k:=TARGET_KEY; guardMs:=PROFILE_GUARD_MS; start:=Runtime();
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE",String(d),"_AUT_PROFILE_",String(d),"T",String(k),"_PC_DOMAIN_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_PROFILE\tPF-GRP-001-C8-TRANSITIVE-PC-DOMAIN-AUT-PROFILE\nDEGREE\t",d,"\nKEY\t",k,"\nGUARD_MS\t",guardMs,"\nSCOPE\tExact parity, Aut(P), and exact-order-8 conjugacy classes for P isomorphic to the single target G; no seed enumeration.\n");
StopIfGuarded:=function(stage)
 if Runtime()-start>=guardMs then
  AppendTo(OUT,"TOTAL_PARTIAL\tDEGREE\t",d,"\tKEY\t",k,"\tSTAGE\t",stage,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
  Print("WROTE ",OUT,"\n"); QUIT;
 fi;
end;
G:=TransitiveGroup(d,k); n:=Size(G); mapsG:=GQuotients(G,CyclicGroup(2));
AppendTo(OUT,"STAGE\tLOAD_G\tORDER\t",n,"\tPARITY_MAPS_G\t",Length(mapsG),"\tMS\t",Runtime()-start,"\n");
StopIfGuarded("LOAD_G");
t:=Runtime(); isoG:=IsomorphismPcGroup(G); P:=Image(isoG); isoMs:=Runtime()-t;
if Size(P)<>n then Error("pc image order mismatch"); fi;
mapsP:=GQuotients(P,CyclicGroup(2));
if Length(mapsP)<>Length(mapsG) then Error("parity quotient count mismatch under isomorphism"); fi;
AppendTo(OUT,"STAGE\tPC_IMAGE\tPC_ORDER\t",Size(P),"\tPARITY_MAPS_P\t",Length(mapsP),"\tISO_MS\t",isoMs,"\tMS\t",Runtime()-start,"\n");
StopIfGuarded("PC_IMAGE");
t:=Runtime(); A:=AutomorphismGroup(P); autMs:=Runtime()-t;
AppendTo(OUT,"STAGE\tAUT_PC\tAUT_ORDER\t",Size(A),"\tAUT_MS\t",autMs,"\tMS\t",Runtime()-start,"\n");
StopIfGuarded("AUT_PC");
t:=Runtime();
if IsSolvableGroup(A) then isoA:=IsomorphismPcGroup(A); AA:=Image(isoA); cc:=ConjugacyClasses(AA); method:="pc";
else cc:=ConjugacyClasses(A); method:="native"; fi;
c8:=Filtered(cc,c->Order(Representative(c))=8); classMs:=Runtime()-t; raw:=n*Length(c8);
AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,"\tPC_ORDER\t",Size(P),"\tPARITY_MAPS_G\t",Length(mapsG),"\tPARITY_MAPS_P\t",Length(mapsP),"\tAUT_ORDER\t",Size(A),"\tISO_MS\t",isoMs,"\tAUT_MS\t",autMs,"\tMETHOD\t",method,"\tCLASS_MS\t",classMs,"\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",raw,"\n");
if Runtime()-start>=guardMs then AppendTo(OUT,"TOTAL_PARTIAL\tDEGREE\t",d,"\tKEY\t",k,"\tSTAGE\tCLASSES_COMPLETE\tPROCESSED\t1\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",raw,"\tISO_MS\t",isoMs,"\tAUT_MS\t",autMs,"\tCLASS_MS\t",classMs,"\tMS\t",Runtime()-start,"\nSTOPPED_GUARD\n");
else AppendTo(OUT,"TOTAL\tDEGREE\t",d,"\tKEY\t",k,"\tPROCESSED\t1\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",raw,"\tISO_MS\t",isoMs,"\tAUT_MS\t",autMs,"\tCLASS_MS\t",classMs,"\tMS\t",Runtime()-start,"\nDONE\n"); fi;
Print("WROTE ",OUT,"\n"); QUIT;
