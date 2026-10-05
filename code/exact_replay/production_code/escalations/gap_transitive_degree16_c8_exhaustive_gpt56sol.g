# Exact proof-complete scan of a checkpointable slice of TransitiveGroup(16,k).
# Environment variables BOLZA16_KMIN and BOLZA16_KMAX select the inclusive
# catalogue-key range.  All target orders are filtered to 2338..50000 and a
# nonzero homomorphism to C2 is required before Aut(G) is constructed.

SetInfoLevel(InfoWarning,0);
SizeScreen([1000000,1000000]);
smin:=GetEnv("BOLZA16_KMIN"); smax:=GetEnv("BOLZA16_KMAX");
if smin=fail then kmin:=1; else kmin:=Int(smin); fi;
if smax=fail then kmax:=NrTransitiveGroups(16); else kmax:=Int(smax); fi;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE16_C8_EXHAUSTIVE_",String(kmin),"_",String(kmax),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE16\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nRANGE\t",kmin,"\t",kmax,"\n",
 "METHOD\tAll order-window TransitiveGroup(16,k), parity prefilter, all Aut(G)-classes of order 8, all parity-compatible seeds. Solvable automorphism groups use an exact pc isomorphism for conjugacy classes.\n");

InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(alpha,x)
 local xs,j; xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od; return xs;
end;
RelatorHolds:=function(G,xs)
 return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]);
end;
B3Cardinality:=function(G,xs)
 local vals,frontier,next,item,j,z,depth;
 vals:=[One(G)]; frontier:=[[One(G),0]];
 for depth in [1..3] do
  next:=[];
  for item in frontier do for j in [1..8] do
   if item[2]=0 or j<>InvPhysicalIndex(item[2]) then
    z:=item[1]*xs[j]; Add(vals,z); Add(next,[z,j]);
   fi;
  od; od; frontier:=next;
 od;
 return Size(Set(vals));
end;
InvariantParityMaps:=function(G,alpha,maps)
 local gens;
 gens:=GeneratorsOfGroup(G);
 return Filtered(maps,f->ForAll(gens,g->Image(f,Image(alpha,g))=Image(f,g)));
end;
SeedIsOdd:=function(maps,x)
 return ForAny(maps,f->not IsOne(Image(f,x)));
end;
PrintNumericCandidate:=function(out,k,alphaNo,repNo,n,xs)
 local p,i;
 AppendTo(out,"CANDIDATE_NUMERIC\t16T",k,"\t",alphaNo,"\t",repNo,"\t",n);
 for p in xs do for i in [1..16] do AppendTo(out,"\t",i^p-1); od; od;
 AppendTo(out,"\n");
end;

entries:=0; parityEntries:=0; order8Classes:=0; invariantAlphaClasses:=0;
fullSeedPairs:=0; oddSeeds:=0; inversePairs:=0; orbit8Pairs:=0; relatorPairs:=0;
b3Pairs:=0; generatingPairs:=0; parityPairs:=0; centralizerOrbits:=0; start:=Runtime();

for k in [kmin..kmax] do
 G:=TransitiveGroup(16,k); n:=Size(G);
 if n>=2338 and n<=50000 then
  entries:=entries+1; maps:=GQuotients(G,CyclicGroup(2));
  if Length(maps)>0 then
   parityEntries:=parityEntries+1; entryStart:=Runtime();
   A:=AutomorphismGroup(G);
   if IsSolvableGroup(A) then
    iso:=IsomorphismPcGroup(A); P:=Image(iso); allcc:=ConjugacyClasses(P);
    c8:=Filtered(allcc,c->Order(Representative(c))=8); pcmode:=true;
   else
    allcc:=ConjugacyClasses(A); c8:=Filtered(allcc,c->Order(Representative(c))=8); pcmode:=false;
   fi;
   eInvAlpha:=0; eOdd:=0; eInv:=0; eOrb:=0; eRel:=0; eB3:=0; eGen:=0; ePar:=0; eCOrbits:=0;
   alphaNo:=0; elems:=Elements(G);
   for ac in c8 do
    alphaNo:=alphaNo+1;
    if pcmode then alpha:=PreImagesRepresentative(iso,Representative(ac)); else alpha:=Representative(ac); fi;
    invmaps:=InvariantParityMaps(G,alpha,maps);
    cOdd:=0; cInv:=0; cOrb:=0; cRel:=0; cB3:=0; cGen:=0; survivors:=[]; maxB3:=0;
    if Length(invmaps)>0 then
     eInvAlpha:=eInvAlpha+1; a4:=alpha^4;
     for x in elems do
      if SeedIsOdd(invmaps,x) then
       cOdd:=cOdd+1;
       if Image(a4,x)=x^-1 then
        cInv:=cInv+1; xs:=PhysicalOrbit(alpha,x);
        if Size(Set(xs))=8 then
         cOrb:=cOrb+1;
         if RelatorHolds(G,xs) then
          cRel:=cRel+1; b:=B3Cardinality(G,xs); if b>maxB3 then maxB3:=b; fi;
          if b=457 then
           cB3:=cB3+1;
           if Size(Group(xs))=n then cGen:=cGen+1; Add(survivors,x); fi;
          fi;
         fi;
        fi;
       fi;
      fi;
     od;
    fi;
    reps:=[]; todo:=ShallowCopy(survivors); C:=Centralizer(A,alpha);
    while Length(todo)>0 do
     x:=todo[1]; Add(reps,x); orb:=Orbit(C,x,function(y,c) return Image(c,y); end);
     todo:=Filtered(todo,y->not y in orb);
    od;
    repNo:=0; for x in reps do repNo:=repNo+1; PrintNumericCandidate(OUT,k,alphaNo,repNo,n,PhysicalOrbit(alpha,x)); od;
    eOdd:=eOdd+cOdd; eInv:=eInv+cInv; eOrb:=eOrb+cOrb; eRel:=eRel+cRel;
    eB3:=eB3+cB3; eGen:=eGen+cGen; ePar:=ePar+Length(survivors); eCOrbits:=eCOrbits+Length(reps);
    AppendTo(OUT,"ALPHA\t16T",k,"\t",alphaNo,"\tCLASS_SIZE\t",Size(ac),
      "\tINVARIANT_PARITY_MAPS\t",Length(invmaps),"\tODD_SEEDS\t",cOdd,
      "\tINVERSE\t",cInv,"\tORBIT8\t",cOrb,"\tRELATOR\t",cRel,
      "\tMAX_B3\t",maxB3,"\tB3\t",cB3,"\tGENERATE\t",cGen,
      "\tCENTRALIZER_ORBITS\t",Length(reps),"\n");
   od;
   order8Classes:=order8Classes+Length(c8); invariantAlphaClasses:=invariantAlphaClasses+eInvAlpha;
   fullSeedPairs:=fullSeedPairs+n*Length(c8); oddSeeds:=oddSeeds+eOdd; inversePairs:=inversePairs+eInv;
   orbit8Pairs:=orbit8Pairs+eOrb; relatorPairs:=relatorPairs+eRel; b3Pairs:=b3Pairs+eB3;
   generatingPairs:=generatingPairs+eGen; parityPairs:=parityPairs+ePar; centralizerOrbits:=centralizerOrbits+eCOrbits;
   AppendTo(OUT,"ENTRY\t16T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),
    "\tPARITY_MAPS\t",Length(maps),"\tORDER8_CLASSES\t",Length(c8),
    "\tINVARIANT_ALPHA_CLASSES\t",eInvAlpha,"\tFULL_SEED_PAIRS\t",n*Length(c8),
    "\tODD_SEEDS\t",eOdd,"\tINVERSE\t",eInv,"\tORBIT8\t",eOrb,
    "\tRELATOR\t",eRel,"\tB3\t",eB3,"\tGENERATE\t",eGen,
    "\tPARITY\t",ePar,"\tCENTRALIZER_ORBITS\t",eCOrbits,"\tMS\t",Runtime()-entryStart,"\n");
  fi;
 fi;
od;
AppendTo(OUT,"TOTAL_SLICE\tRANGE\t",kmin,"\t",kmax,"\tORDER_WINDOW_ENTRIES\t",entries,
 "\tPARITY_ENTRIES\t",parityEntries,"\tORDER8_CLASSES\t",order8Classes,
 "\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tFULL_SEED_PAIRS\t",fullSeedPairs,
 "\tODD_SEEDS\t",oddSeeds,"\tINVERSE\t",inversePairs,"\tORBIT8\t",orbit8Pairs,
 "\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
 "\tPARITY\t",parityPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,
 "\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
