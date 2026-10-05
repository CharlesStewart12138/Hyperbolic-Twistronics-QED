SetInfoLevel(InfoWarning, 0);
Print("GAP_VERSION\t", GAPInfo.Version, "\n");
for d in [1..15] do
  n := NrTransitiveGroups(d);
  eligible := 0;
  ords := [];
  for k in [1..n] do
    G := TransitiveGroup(d,k);
    o := Size(G);
    if o >= 2338 and o <= 50000 then
      eligible := eligible + 1;
      Add(ords,o);
    fi;
  od;
  Print("DEGREE\t",d,"\tDATABASE\t",n,"\tELIGIBLE\t",eligible,"\tORDERS\t",Set(ords),"\n");
od;
QUIT;
