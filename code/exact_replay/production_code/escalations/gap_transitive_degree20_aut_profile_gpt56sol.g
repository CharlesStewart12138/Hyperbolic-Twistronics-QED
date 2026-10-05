SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE20_AUT_PROFILE_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");cnt:=0;c8tot:=0;pairs:=0;start:=Runtime();
for k in [1..NrTransitiveGroups(20)]do G:=TransitiveGroup(20,k);n:=Size(G);if n>=2338 and n<=50000 then maps:=GQuotients(G,CyclicGroup(2));if Length(maps)>0 then
 AppendTo(OUT,"START\t20T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",Length(maps),"\n");t:=Runtime();A:=AutomorphismGroup(G);
 if IsSolvableGroup(A)then iso:=IsomorphismPcGroup(A);cc:=ConjugacyClasses(Image(iso));method:="pc";else cc:=ConjugacyClasses(A);method:="native";fi;
 c8:=Filtered(cc,c->Order(Representative(c))=8);cnt:=cnt+1;c8tot:=c8tot+Length(c8);pairs:=pairs+n*Length(c8);
 AppendTo(OUT,"ENTRY\t20T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tMETHOD\t",method,"\tORDER8_CLASSES\t",Length(c8),"\tSEED_PAIRS\t",n*Length(c8),"\tMS\t",Runtime()-t,"\n");
fi;fi;od;
AppendTo(OUT,"TOTAL\tENTRIES\t",cnt,"\tORDER8_CLASSES\t",c8tot,"\tSEED_PAIRS\t",pairs,"\tMS\t",Runtime()-start,"\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
