SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE21_22_AUT_PROBE_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n"); total:=0;pairs:=0;start:=Runtime();
for d in [21,22] do for k in [1..NrTransitiveGroups(d)] do G:=TransitiveGroup(d,k);n:=Size(G);
 if n>=2338 and n<=50000 and Length(GQuotients(G,CyclicGroup(2)))>0 then
  t:=Runtime();A:=AutomorphismGroup(G);
  if IsSolvableGroup(A) then iso:=IsomorphismPcGroup(A);cc:=ConjugacyClasses(Image(iso));method:="pc";else cc:=ConjugacyClasses(A);method:="native";fi;
  c8:=Filtered(cc,c->Order(Representative(c))=8);total:=total+Length(c8);pairs:=pairs+n*Length(c8);
  AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tMETHOD\t",method,"\tORDER8_CLASSES\t",Length(c8),"\tSEED_PAIRS\t",n*Length(c8),"\tMS\t",Runtime()-t,"\n");
 fi;od;od;
AppendTo(OUT,"TOTAL\tORDER8_CLASSES\t",total,"\tSEED_PAIRS\t",pairs,"\tMS\t",Runtime()-start,"\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
