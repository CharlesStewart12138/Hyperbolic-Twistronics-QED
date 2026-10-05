SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE16_PROBE_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");
eligible:=0; parityEligible:=0; orders:=[]; parityOrders:=[]; start:=Runtime();
for k in [1..NrTransitiveGroups(16)] do
  G:=TransitiveGroup(16,k); n:=Size(G);
  if n>=2338 and n<=50000 then
    eligible:=eligible+1; Add(orders,n);
    maps:=GQuotients(G,CyclicGroup(2));
    if Length(maps)>0 then
      parityEligible:=parityEligible+1; Add(parityOrders,n);
      AppendTo(OUT,"ENTRY\t16T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",Length(maps),"\n");
    fi;
  fi;
od;
AppendTo(OUT,"TOTAL\tDATABASE\t",NrTransitiveGroups(16),"\tELIGIBLE\t",eligible,
 "\tPARITY_ELIGIBLE\t",parityEligible,"\tORDERS\t",Set(orders),
 "\tPARITY_ORDERS\t",Set(parityOrders),"\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
