SetInfoLevel(InfoWarning,0);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE16_AUT_PROBE_PC_GPT56SOL.txt";
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\nMETHOD\tpc conjugacy classes for solvable Aut(G), native otherwise\n");
processed:=0; classes8:=0; pairSeeds:=0; start:=Runtime();
for k in [1..NrTransitiveGroups(16)] do
  G:=TransitiveGroup(16,k); n:=Size(G);
  if n>=2338 and n<=50000 then
    maps:=GQuotients(G,CyclicGroup(2));
    if Length(maps)>0 then
      AppendTo(OUT,"START\t16T",k,"\tORDER\t",n,"\tPARITY_MAPS\t",Length(maps),"\n");
      t0:=Runtime(); A:=AutomorphismGroup(G); t1:=Runtime();
      if IsSolvableGroup(A) then
        iso:=IsomorphismPcGroup(A); P:=Image(iso); t2:=Runtime(); cc:=ConjugacyClasses(P); method:="pc";
      else
        t2:=t1; cc:=ConjugacyClasses(A); method:="native";
      fi;
      c8:=Filtered(cc,c->Order(Representative(c))=8); t3:=Runtime();
      processed:=processed+1; classes8:=classes8+Length(c8); pairSeeds:=pairSeeds+n*Length(c8);
      AppendTo(OUT,"DONE_ENTRY\t16T",k,"\tAUT_ORDER\t",Size(A),"\tSOLVABLE_AUT\t",IsSolvableGroup(A),
       "\tMETHOD\t",method,"\tCLASSES\t",Length(cc),"\tORDER8_CLASSES\t",Length(c8),
       "\tSEED_PAIRS\t",n*Length(c8),"\tAUT_MS\t",t1-t0,"\tCONVERT_MS\t",t2-t1,
       "\tCLASS_MS\t",t3-t2,"\tTOTAL_ENTRY_MS\t",t3-t0,"\n");
    fi;
  fi;
od;
AppendTo(OUT,"TOTAL\tPROCESSED\t",processed,"\tORDER8_CLASSES\t",classes8,
 "\tSEED_PAIRS\t",pairSeeds,"\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
