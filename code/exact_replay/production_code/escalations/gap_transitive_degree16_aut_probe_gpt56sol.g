SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE16_AUT_PROBE_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");
processed:=0; classes8:=0; start:=Runtime();
for k in [1..NrTransitiveGroups(16)] do
  G:=TransitiveGroup(16,k); n:=Size(G);
  if n>=2338 and n<=50000 then
    maps:=GQuotients(G,CyclicGroup(2));
    if Length(maps)>0 then
      AppendTo(OUT,"START\t16T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",Length(maps),"\n");
      t0:=Runtime(); A:=AutomorphismGroup(G); t1:=Runtime();
      AppendTo(OUT,"AUT\t16T",k,"\tAUT_ORDER\t",Size(A),"\tAUT_MS\t",t1-t0,"\n");
      cc:=ConjugacyClasses(A); c8:=Filtered(cc,c->Order(Representative(c))=8); t2:=Runtime();
      processed:=processed+1; classes8:=classes8+Length(c8);
      AppendTo(OUT,"DONE_ENTRY\t16T",k,"\tCLASSES\t",Length(cc),"\tORDER8_CLASSES\t",Length(c8),
       "\tCLASS_MS\t",t2-t1,"\tTOTAL_ENTRY_MS\t",t2-t0,"\n");
    fi;
  fi;
od;
AppendTo(OUT,"TOTAL\tPROCESSED\t",processed,"\tORDER8_CLASSES\t",classes8,"\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
