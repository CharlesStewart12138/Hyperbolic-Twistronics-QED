SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE20_PROBE_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");e:=0;p:=0;ords:=[];pords:=[];start:=Runtime();
for k in [1..NrTransitiveGroups(20)]do G:=TransitiveGroup(20,k);n:=Size(G);if n>=2338 and n<=50000 then e:=e+1;Add(ords,n);maps:=GQuotients(G,CyclicGroup(2));if Length(maps)>0 then p:=p+1;Add(pords,n);AppendTo(OUT,"ENTRY\t20T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",Length(maps),"\n");fi;fi;od;
AppendTo(OUT,"TOTAL\tDATABASE\t",NrTransitiveGroups(20),"\tORDER_WINDOW\t",e,"\tPARITY\t",p,"\tORDERS\t",Set(ords),"\tPARITY_ORDERS\t",Set(pords),"\tMS\t",Runtime()-start,"\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
