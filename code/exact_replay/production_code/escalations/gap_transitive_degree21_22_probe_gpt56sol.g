SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE21_22_PROBE_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");
for d in [21,22] do
 start:=Runtime(); e:=0; p:=0; ords:=[]; pords:=[];
 for k in [1..NrTransitiveGroups(d)] do G:=TransitiveGroup(d,k); n:=Size(G);
  if n>=2338 and n<=50000 then e:=e+1; Add(ords,n); maps:=GQuotients(G,CyclicGroup(2));
   if Length(maps)>0 then p:=p+1; Add(pords,n); AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",Length(maps),"\n"); fi;
  fi;
 od;
 AppendTo(OUT,"DEGREE\t",d,"\tDATABASE\t",NrTransitiveGroups(d),"\tORDER_WINDOW\t",e,"\tPARITY\t",p,"\tORDERS\t",Set(ords),"\tPARITY_ORDERS\t",Set(pords),"\tMS\t",Runtime()-start,"\n");
od; AppendTo(OUT,"DONE\n"); Print("WROTE ",OUT,"\n"); QUIT;
