# Exact catalogue exhaustion for C8-equivariant Bolza quotients whose target
# has a faithful transitive permutation representation of degree at most 15.
# GAP 4.12.1; requires the TransGrp library.

SetInfoLevel(InfoWarning, 0);
SizeScreen([1000000,1000000]);

OUT := "/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE15_C8_EXHAUSTIVE_GPT56SOL.txt";
PrintTo(OUT, "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE15\n");
AppendTo(OUT, "GAP_VERSION\t", GAPInfo.Version, "\n");
AppendTo(OUT, "SCOPE\tEvery TransitiveGroup(d,k) catalogue entry for 1<=d<=15 and 2338<=Size(G)<=50000; every Aut(G)-conjugacy class of exact-order-8 automorphisms; every seed x in G.\n");
AppendTo(OUT, "PHYSICAL\tx_j=alpha^j(x), inverse alpha^4(x)=x^-1, relator indices zero-based 0,5,2,7,4,1,6,3.\n");
AppendTo(OUT, "B3\tAll 1+8+8*7+8*7^2=457 freely reduced physical words of length at most 3 must have distinct images.\n");
AppendTo(OUT, "PARITY\tComplete GQuotients(G,C2); accept iff one epimorphism sends every x_j to the nonidentity.\n");

InvPhysicalIndex := function(i)
  return ((i-1+4) mod 8)+1;
end;

B3Cardinality := function(G, xs)
  local vals, frontier, next, item, j, z, depth;
  vals := [One(G)];
  frontier := [[One(G),0]];
  for depth in [1..3] do
    next := [];
    for item in frontier do
      for j in [1..8] do
        if item[2]=0 or j<>InvPhysicalIndex(item[2]) then
          z := item[1]*xs[j];
          Add(vals,z);
          Add(next,[z,j]);
        fi;
      od;
    od;
    frontier := next;
  od;
  return Size(Set(vals));
end;

HasFrozenParity := function(parityMaps, xs)
  local f, j, good;
  for f in parityMaps do
    good := true;
    for j in [1..8] do
      if IsOne(Image(f,xs[j])) then
        good := false;
        break;
      fi;
    od;
    if good then return true; fi;
  od;
  return false;
end;

PhysicalOrbit := function(alpha,x)
  local xs,j;
  xs := [x];
  for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od;
  return xs;
end;

RelatorHolds := function(G,xs)
  return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]);
end;

PrintElementList := function(out, tag, xs)
  local j;
  AppendTo(out,tag,"\t[");
  for j in [1..Length(xs)] do
    if j>1 then AppendTo(out,","); fi;
    AppendTo(out,xs[j]);
  od;
  AppendTo(out,"]\n");
end;

totalEntries := 0;
eligibleEntries := 0;
order8Classes := 0;
seedPairs := 0;
inversePairs := 0;
orbit8Pairs := 0;
relatorPairs := 0;
b3Pairs := 0;
generatingPairs := 0;
parityPairs := 0;
orbitReps := 0;
globalStart := Runtime();

for d in [1..15] do
  degreeEligible := 0;
  degreeStart := Runtime();
  for k in [1..NrTransitiveGroups(d)] do
    totalEntries := totalEntries+1;
    G := TransitiveGroup(d,k);
    n := Size(G);
    if n>=2338 and n<=50000 then
      eligibleEntries := eligibleEntries+1;
      degreeEligible := degreeEligible+1;
      entryStart := Runtime();
      A := AutomorphismGroup(G);
      classes := Filtered(ConjugacyClasses(A),c->Order(Representative(c))=8);
      parityMaps := GQuotients(G,CyclicGroup(2));
      elems := Elements(G);
      entryInv := 0; entryOrb8 := 0; entryRel := 0; entryB3 := 0;
      entryGen := 0; entryParity := 0; entryOrbitReps := 0;
      alphaNo := 0;
      for ac in classes do
        alphaNo := alphaNo+1;
        alpha := Representative(ac);
        a4 := alpha^4;
        cInv := 0; cOrb8 := 0; cRel := 0; cB3 := 0; cGen := 0; cParity := 0;
        b3sizes := [];
        survivors := [];
        for x in elems do
          if Image(a4,x)=x^-1 then
            cInv := cInv+1;
            xs := PhysicalOrbit(alpha,x);
            if Size(Set(xs))=8 then
              cOrb8 := cOrb8+1;
              if RelatorHolds(G,xs) then
                cRel := cRel+1;
                b := B3Cardinality(G,xs);
                Add(b3sizes,b);
                if b=457 then
                  cB3 := cB3+1;
                  if Size(Group(xs))=n then
                    cGen := cGen+1;
                    if HasFrozenParity(parityMaps,xs) then
                      cParity := cParity+1;
                      Add(survivors,x);
                    fi;
                  fi;
                fi;
              fi;
            fi;
          fi;
        od;
        C := Centralizer(A,alpha);
        reps := [];
        todo := ShallowCopy(survivors);
        while Length(todo)>0 do
          x := todo[1];
          Add(reps,x);
          orb := Orbit(C,x,function(y,c) return Image(c,y); end);
          todo := Filtered(todo,y->not y in orb);
        od;
        entryInv := entryInv+cInv; entryOrb8 := entryOrb8+cOrb8;
        entryRel := entryRel+cRel; entryB3 := entryB3+cB3;
        entryGen := entryGen+cGen; entryParity := entryParity+cParity;
        entryOrbitReps := entryOrbitReps+Length(reps);
        AppendTo(OUT,"ALPHA\t",d,"T",k,"\t",alphaNo,
          "\tAUT_CLASS_SIZE\t",Size(ac),"\tCENTRALIZER\t",Size(C),
          "\tSEEDS\t",n,"\tINVERSE\t",cInv,"\tORBIT8\t",cOrb8,
          "\tRELATOR\t",cRel,"\tB3\t",cB3,"\tGENERATE\t",cGen,
          "\tPARITY\t",cParity,"\tPARITY_CENTRALIZER_ORBITS\t",Length(reps),
          "\tB3_HIST\t",Collected(b3sizes),"\n");
        if Length(reps)>0 then
          PrintElementList(OUT,Concatenation("ALPHA_IMAGES\t",String(d),"T",String(k),"\t",String(alphaNo)),
             List(GeneratorsOfGroup(G),g->Image(alpha,g)));
          repNo := 0;
          for x in reps do
            repNo := repNo+1;
            xs := PhysicalOrbit(alpha,x);
            AppendTo(OUT,"CANDIDATE\t",d,"T",k,"\tALPHA\t",alphaNo,
                     "\tREP\t",repNo,"\tORDER\t",n,"\tSEED\t",x,"\n");
            PrintElementList(OUT,Concatenation("PHYSICAL_IMAGES\t",String(d),"T",String(k),"\t",String(alphaNo),"\t",String(repNo)),xs);
          od;
        fi;
      od;
      order8Classes := order8Classes+Length(classes);
      seedPairs := seedPairs+n*Length(classes);
      inversePairs := inversePairs+entryInv; orbit8Pairs := orbit8Pairs+entryOrb8;
      relatorPairs := relatorPairs+entryRel; b3Pairs := b3Pairs+entryB3;
      generatingPairs := generatingPairs+entryGen; parityPairs := parityPairs+entryParity;
      orbitReps := orbitReps+entryOrbitReps;
      AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,
        "\tAUT_ORDER\t",Size(A),"\tORDER8_CLASSES\t",Length(classes),
        "\tPARITY_MAPS\t",Length(parityMaps),"\tINVERSE\t",entryInv,
        "\tORBIT8\t",entryOrb8,"\tRELATOR\t",entryRel,
        "\tB3\t",entryB3,"\tGENERATE\t",entryGen,
        "\tPARITY\t",entryParity,"\tPARITY_CENTRALIZER_ORBITS\t",entryOrbitReps,
        "\tMS\t",Runtime()-entryStart,"\n");
    fi;
  od;
  AppendTo(OUT,"DEGREE_DONE\t",d,"\tDATABASE_ENTRIES\t",NrTransitiveGroups(d),
           "\tELIGIBLE\t",degreeEligible,"\tMS\t",Runtime()-degreeStart,"\n");
od;

AppendTo(OUT,"TOTAL\tDATABASE_ENTRIES\t",totalEntries,
  "\tELIGIBLE_ENTRIES\t",eligibleEntries,"\tORDER8_CLASSES\t",order8Classes,
  "\tSEED_PAIRS\t",seedPairs,"\tINVERSE\t",inversePairs,
  "\tORBIT8\t",orbit8Pairs,"\tRELATOR\t",relatorPairs,
  "\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
  "\tPARITY\t",parityPairs,"\tPARITY_CENTRALIZER_ORBITS\t",orbitReps,
  "\tMS\t",Runtime()-globalStart,"\n");
AppendTo(OUT,"DONE\n");
Print("WROTE ",OUT,"\n");
QUIT;
