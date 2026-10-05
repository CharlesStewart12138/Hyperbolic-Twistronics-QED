# Exact workload profile for the degree-18 transitive-group C8 census.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
kmin:=1;kmax:=NrTransitiveGroups(18);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE18_PROFILE_1_983_GPT56SOL.txt";
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE18-PROFILE\nGAP_VERSION\t",GAPInfo.Version,"\nRANGE\t",kmin,"\t",kmax,"\n");
eligible:=0;parity:=0;classes:=0;invariant:=0;raw:=0;invariantRaw:=0;start:=Runtime();
for k in [kmin..kmax] do
 G:=TransitiveGroup(18,k);n:=Size(G);
 if n>=2338 and n<=50000 then eligible:=eligible+1;maps:=GQuotients(G,CyclicGroup(2));
  if Length(maps)>0 then parity:=parity+1;t:=Runtime();A:=AutomorphismGroup(G);
   if IsSolvableGroup(A) then iso:=IsomorphismPcGroup(A);P:=Image(iso);cc:=ConjugacyClasses(P);pc:=true;
   else cc:=ConjugacyClasses(A);pc:=false;fi;
   c8:=Filtered(cc,c->Order(Representative(c))=8);ci:=0;betas:=[];
   for ac in c8 do if pc then a:=PreImagesRepresentative(iso,Representative(ac));else a:=Representative(ac);fi;
    ims:=Filtered(maps,f->ForAll(GeneratorsOfGroup(G),g->Image(f,Image(a,g))=Image(f,g)));
    if Length(ims)>0 then ci:=ci+1;if Position(betas,a^4)=fail then Add(betas,a^4);fi;fi;
   od;
   classes:=classes+Length(c8);invariant:=invariant+ci;raw:=raw+n*Length(c8);invariantRaw:=invariantRaw+n*ci;
   AppendTo(OUT,"ENTRY\t18T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tPARITY_MAPS\t",Length(maps),"\tORDER8_CLASSES\t",Length(c8),"\tINVARIANT_CLASSES\t",ci,"\tDISTINCT_BETA\t",Length(betas),"\tRAW_PAIRS\t",n*Length(c8),"\tINVARIANT_RAW_PAIRS\t",n*ci,"\tMS\t",Runtime()-t,"\n");
  else AppendTo(OUT,"ORDER_WINDOW_NO_PARITY\t18T",k,"\tORDER\t",n,"\n");fi;
 fi;
od;
AppendTo(OUT,"TOTAL_PROFILE\tDATABASE\t",NrTransitiveGroups(18),"\tRANGE\t",kmin,"\t",kmax,"\tORDER_WINDOW\t",eligible,"\tPARITY_ENTRIES\t",parity,"\tORDER8_CLASSES\t",classes,"\tINVARIANT_CLASSES\t",invariant,"\tRAW_PAIRS\t",raw,"\tINVARIANT_RAW_PAIRS\t",invariantRaw,"\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n");QUIT;
