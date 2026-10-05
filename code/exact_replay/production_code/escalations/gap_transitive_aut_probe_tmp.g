SetInfoLevel(InfoWarning, 0);
Print("GAP_VERSION\t", GAPInfo.Version, "\n");
for d in [7..15] do
  for k in [1..NrTransitiveGroups(d)] do
    G := TransitiveGroup(d,k);
    o := Size(G);
    if o >= 2338 and o <= 50000 then
      t0 := Runtime();
      A := AutomorphismGroup(G);
      t1 := Runtime();
      cc := ConjugacyClasses(A);
      c8 := Filtered(cc, c -> Order(Representative(c)) = 8);
      t2 := Runtime();
      Print("ENTRY\t",d,"T",k,"\tORDER\t",o,"\tAUT_ORDER\t",Size(A),
            "\tAUT_MS\t",t1-t0,"\tCLASSES_MS\t",t2-t1,
            "\tCLASSES\t",Length(cc),"\tORDER8_CLASSES\t",Length(c8),"\n");
    fi;
  od;
od;
Print("DONE\n");
QUIT;
