# Exact degree-16 catalogue scan, optimized by caching the twisted-involution
# locus {x in G : alpha^4(x)=x^-1} for each distinct beta=alpha^4.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
smin:=GetEnv("BOLZA16_KMIN"); smax:=GetEnv("BOLZA16_KMAX");
if smin=fail then kmin:=1; else kmin:=Int(smin); fi;
if smax=fail then kmax:=NrTransitiveGroups(16); else kmax:=Int(smax); fi;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE16_C8_BETA_",String(kmin),"_",String(kmax),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE16-BETA\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nRANGE\t",kmin,"\t",kmax,"\n",
 "SCOPE\tEvery order-window TransitiveGroup(16,k) in range, every Aut(G)-class of exact order 8, every seed in its alpha^4-twisted inverse locus.\n",
 "OPTIMIZATION\tFor each distinct beta=alpha^4 the exact locus beta(x)=x^-1 is enumerated once; alpha-invariant C2 epimorphisms filter it before orbit/relator/B3/generation.\n");

InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(alpha,x) local xs,j; xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od; return xs; end;
RelatorHolds:=function(G,xs) return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]); end;
B3Cardinality:=function(G,xs)
 local vals,frontier,next,item,j,z,depth;
 vals:=[One(G)]; frontier:=[[One(G),0]];
 for depth in [1..3] do next:=[];
  for item in frontier do for j in [1..8] do
   if item[2]=0 or j<>InvPhysicalIndex(item[2]) then z:=item[1]*xs[j]; Add(vals,z); Add(next,[z,j]); fi;
  od; od; frontier:=next;
 od; return Size(Set(vals));
end;
InvariantParityMaps:=function(G,alpha,maps) local gens; gens:=GeneratorsOfGroup(G);
 return Filtered(maps,f->ForAll(gens,g->Image(f,Image(alpha,g))=Image(f,g))); end;
SeedIsOdd:=function(maps,x) return ForAny(maps,f->not IsOne(Image(f,x))); end;
PrintNumericCandidate:=function(out,k,alphaNo,repNo,n,xs) local p,i;
 AppendTo(out,"CANDIDATE_NUMERIC\t16T",k,"\t",alphaNo,"\t",repNo,"\t",n);
 for p in xs do for i in [1..16] do AppendTo(out,"\t",i^p-1); od; od; AppendTo(out,"\n"); end;

entries:=0; parityEntries:=0; order8Classes:=0; invariantAlphaClasses:=0; betaComputations:=0;
fullSeedPairs:=0; inversePairs:=0; inverseOddPairs:=0; orbit8Pairs:=0; relatorPairs:=0;
b3Pairs:=0; generatingPairs:=0; centralizerOrbits:=0; start:=Runtime();
for k in [kmin..kmax] do
 G:=TransitiveGroup(16,k); n:=Size(G);
 if n>=2338 and n<=50000 then entries:=entries+1; maps:=GQuotients(G,CyclicGroup(2));
  if Length(maps)>0 then parityEntries:=parityEntries+1; entryStart:=Runtime(); A:=AutomorphismGroup(G);
   if IsSolvableGroup(A) then iso:=IsomorphismPcGroup(A); P:=Image(iso); allcc:=ConjugacyClasses(P);
    c8:=Filtered(allcc,c->Order(Representative(c))=8); pcmode:=true;
   else allcc:=ConjugacyClasses(A); c8:=Filtered(allcc,c->Order(Representative(c))=8); pcmode:=false; fi;
   elems:=Elements(G); betas:=[]; loci:=[];
   eInvAlpha:=0; eInv:=0; eInvOdd:=0; eOrb:=0; eRel:=0; eB3:=0; eGen:=0; eCOrbits:=0; alphaNo:=0;
   for ac in c8 do alphaNo:=alphaNo+1;
    if pcmode then alpha:=PreImagesRepresentative(iso,Representative(ac)); else alpha:=Representative(ac); fi;
    invmaps:=InvariantParityMaps(G,alpha,maps); cInv:=0; cInvOdd:=0; cOrb:=0; cRel:=0; cB3:=0; cGen:=0; maxB3:=0; survivors:=[];
    if Length(invmaps)>0 then eInvAlpha:=eInvAlpha+1; beta:=alpha^4; pos:=Position(betas,beta);
     if pos=fail then Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1)); pos:=Length(betas); betaComputations:=betaComputations+1; fi;
     locus:=loci[pos]; cInv:=Length(locus);
     for x in locus do if SeedIsOdd(invmaps,x) then cInvOdd:=cInvOdd+1; xs:=PhysicalOrbit(alpha,x);
      if Size(Set(xs))=8 then cOrb:=cOrb+1;
       if RelatorHolds(G,xs) then cRel:=cRel+1; b:=B3Cardinality(G,xs); if b>maxB3 then maxB3:=b; fi;
        if b=457 then cB3:=cB3+1; if Size(Group(xs))=n then cGen:=cGen+1; Add(survivors,x); fi; fi;
       fi;
      fi;
     fi; od;
    fi;
    reps:=[];
    if Length(survivors)>0 then C:=Centralizer(A,alpha); todo:=ShallowCopy(survivors);
     while Length(todo)>0 do x:=todo[1]; Add(reps,x); orb:=Orbit(C,x,function(y,c) return Image(c,y); end); todo:=Filtered(todo,y->not y in orb); od;
    fi;
    repNo:=0; for x in reps do repNo:=repNo+1; PrintNumericCandidate(OUT,k,alphaNo,repNo,n,PhysicalOrbit(alpha,x)); od;
    eInv:=eInv+cInv; eInvOdd:=eInvOdd+cInvOdd; eOrb:=eOrb+cOrb; eRel:=eRel+cRel; eB3:=eB3+cB3; eGen:=eGen+cGen; eCOrbits:=eCOrbits+Length(reps);
    AppendTo(OUT,"ALPHA\t16T",k,"\t",alphaNo,"\tCLASS_SIZE\t",Size(ac),"\tINVARIANT_PARITY_MAPS\t",Length(invmaps),
     "\tINVERSE_LOCUS\t",cInv,"\tINVERSE_ODD\t",cInvOdd,"\tORBIT8\t",cOrb,"\tRELATOR\t",cRel,
     "\tMAX_B3\t",maxB3,"\tB3\t",cB3,"\tGENERATE\t",cGen,"\tCENTRALIZER_ORBITS\t",Length(reps),"\n");
   od;
   order8Classes:=order8Classes+Length(c8); invariantAlphaClasses:=invariantAlphaClasses+eInvAlpha; fullSeedPairs:=fullSeedPairs+n*Length(c8);
   inversePairs:=inversePairs+eInv; inverseOddPairs:=inverseOddPairs+eInvOdd; orbit8Pairs:=orbit8Pairs+eOrb; relatorPairs:=relatorPairs+eRel;
   b3Pairs:=b3Pairs+eB3; generatingPairs:=generatingPairs+eGen; centralizerOrbits:=centralizerOrbits+eCOrbits;
   AppendTo(OUT,"ENTRY\t16T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tPARITY_MAPS\t",Length(maps),
    "\tORDER8_CLASSES\t",Length(c8),"\tINVARIANT_ALPHA_CLASSES\t",eInvAlpha,"\tDISTINCT_BETA\t",Length(betas),
    "\tFULL_SEED_PAIRS\t",n*Length(c8),"\tINVERSE\t",eInv,"\tINVERSE_ODD\t",eInvOdd,"\tORBIT8\t",eOrb,
    "\tRELATOR\t",eRel,"\tB3\t",eB3,"\tGENERATE\t",eGen,"\tCENTRALIZER_ORBITS\t",eCOrbits,"\tMS\t",Runtime()-entryStart,"\n");
  fi;
 fi;
od;
AppendTo(OUT,"TOTAL_SLICE\tRANGE\t",kmin,"\t",kmax,"\tORDER_WINDOW_ENTRIES\t",entries,"\tPARITY_ENTRIES\t",parityEntries,
 "\tORDER8_CLASSES\t",order8Classes,"\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tBETA_COMPUTATIONS\t",betaComputations,
 "\tFULL_SEED_PAIRS\t",fullSeedPairs,"\tINVERSE\t",inversePairs,"\tINVERSE_ODD\t",inverseOddPairs,
 "\tORBIT8\t",orbit8Pairs,"\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
 "\tPARITY\t",generatingPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,"\tMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
