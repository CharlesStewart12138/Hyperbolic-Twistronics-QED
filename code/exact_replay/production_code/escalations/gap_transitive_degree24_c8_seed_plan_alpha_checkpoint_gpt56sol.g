# Exact resource-guarded C8 seed scan for one sealed lexicographic
# (TransitiveGroup(24,k), exact-order-8 Aut-class index) workload shard.
# The wrapper supplies S001_RECORDS and the recovery state.  Each ALPHA_DONE
# line is the durable recovery boundary; a continuation starts at NEXT_UNIT
# and never repeats a sealed alpha unit.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if not IsBound(S001_RECORDS) or not IsBound(OUT) or
   not IsBound(INTERNAL_GUARD_MS) or not IsBound(START_UNIT) or
   not IsBound(INITIAL_COUNTERS) or not IsBound(PREVIOUS_CHECKPOINT_SHA256) or
   not IsBound(EXPECTED_PROFILE_SHA256) or not IsBound(EXPECTED_PLAN_SHA256) then
 Error("seed shard wrapper variables missing");
fi;
d:=24; db:=NrTransitiveGroups(d);
if db<>25000 then Error("unexpected degree-24 catalogue size"); fi;
if Length(INITIAL_COUNTERS)<>12 then Error("INITIAL_COUNTERS length"); fi;

InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(alpha,x) local xs,j;
 xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od; return xs;
end;
RelatorHolds:=function(G,xs)
 return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]);
end;
B3Cardinality:=function(G,xs)
 local vals,frontier,next,item,j,z,depth;
 vals:=[One(G)]; frontier:=[[One(G),0]];
 for depth in [1..3] do
  next:=[];
  for item in frontier do
   for j in [1..8] do
    if item[2]=0 or j<>InvPhysicalIndex(item[2]) then
     z:=item[1]*xs[j]; Add(vals,z); Add(next,[z,j]);
    fi;
   od;
  od;
  frontier:=next;
 od;
 return Size(Set(vals));
end;
InvariantParityMaps:=function(G,alpha,maps) local gens;
 gens:=GeneratorsOfGroup(G);
 return Filtered(maps,f->ForAll(gens,g->Image(f,Image(alpha,g))=Image(f,g)));
end;
SeedIsOdd:=function(maps,x)
 return ForAny(maps,f->not IsOne(Image(f,x)));
end;
PrintNumericCandidate:=function(out,k,alphaNo,repNo,n,unitNo,xs) local p,i;
 AppendTo(out,"CANDIDATE_NUMERIC\t24T",k,"\tALPHA\t",alphaNo,
  "\tREP\t",repNo,"\tORDER\t",n,"\tUNIT\t",unitNo,"\tDEGREE\t24");
 for p in xs do for i in [1..24] do AppendTo(out,"\t",i^p-1); od; od;
 AppendTo(out,"\n");
end;

# Verify the wrapper's exact sealed plan slice before any group computation.
if Length(S001_RECORDS)<>466 then Error("S001 record count"); fi;
planUnits:=0; planRaw:=0; planProfileMs:=0; previousKey:=0; expectedUnitFirst:=1;
for row in S001_RECORDS do
 if row.k<=previousKey then Error("S001 key order"); fi;
 if row.first<1 or row.last<row.first or row.last>row.classes then Error("S001 alpha interval"); fi;
 if row.unitFirst<>expectedUnitFirst then Error("S001 unit continuity"); fi;
 if row.unitLast-row.unitFirst<>row.last-row.first then Error("S001 unit span"); fi;
 if row.raw<>row.order*row.classes then Error("S001 full-profile raw identity"); fi;
 planUnits:=planUnits+row.last-row.first+1;
 planRaw:=planRaw+row.order*(row.last-row.first+1);
 planProfileMs:=planProfileMs+row.profileMs;
 previousKey:=row.k; expectedUnitFirst:=row.unitLast+1;
od;
if S001_RECORDS[1].k<>5155 or S001_RECORDS[1].first<>1 or
   S001_RECORDS[Length(S001_RECORDS)].k<>5715 or
   S001_RECORDS[Length(S001_RECORDS)].last<>66 then Error("S001 endpoint mismatch"); fi;
if planUnits<>14622 or planRaw<>43149024 or planProfileMs<>224649 or
   expectedUnitFirst<>14623 then Error("S001 checksum mismatch"); fi;
if START_UNIT<1 or START_UNIT>14622 then Error("invalid START_UNIT"); fi;
if INITIAL_COUNTERS[1]<>START_UNIT-1 then Error("initial unit counter mismatch"); fi;

PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD001\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDEGREE\t24\nDATABASE\t",db,"\n",
 "PLAN_FIRST\t24T5155\t1\nPLAN_LAST\t24T5715\t66\n",
 "PLAN_KEYS\t466\nPLAN_CLASS_UNITS\t14622\nPLAN_RAW_PAIRS\t43149024\n",
 "PLAN_PROFILE_REBUILD_MS\t224649\nINTERNAL_GUARD_MS\t",INTERNAL_GUARD_MS,"\n",
 "START_UNIT\t",START_UNIT,"\nPREVIOUS_CHECKPOINT_SHA256\t",PREVIOUS_CHECKPOINT_SHA256,"\n",
 "PROFILE_SHA256\t",EXPECTED_PROFILE_SHA256,"\nPLAN_SHA256\t",EXPECTED_PLAN_SHA256,"\n",
 "FROZEN\tg_j=alpha^j(x); alpha^4(x)=x^-1; relator indices 0,5,2,7,4,1,6,3; B3=457; generated image exact; invariant odd C2 parity exact.\n",
 "RECOVERY\tALPHA_DONE is the atomic boundary; resume at NEXT_UNIT with its CUM counters and prior-file SHA256; completed alpha units are never replayed.\n",
 "SCOPE\tExactly seed-plan shard001 only; later shards are excluded.\n");

completedUnits:=INITIAL_COUNTERS[1]; rawPairs:=INITIAL_COUNTERS[2];
invariantAlphaClasses:=INITIAL_COUNTERS[3]; betaComputations:=INITIAL_COUNTERS[4];
inversePairs:=INITIAL_COUNTERS[5]; inverseOddPairs:=INITIAL_COUNTERS[6];
orbit8Pairs:=INITIAL_COUNTERS[7]; relatorPairs:=INITIAL_COUNTERS[8];
b3Pairs:=INITIAL_COUNTERS[9]; generatingPairs:=INITIAL_COUNTERS[10];
centralizerOrbits:=INITIAL_COUNTERS[11]; candidateNumeric:=INITIAL_COUNTERS[12];
segmentUnits:=0; segmentRaw:=0; profileKeysRebuilt:=0; profileActualMs:=0;
start:=Runtime(); stoppedGuard:=false; stoppedCandidate:=false; lastUnit:=START_UNIT-1;

for row in S001_RECORDS do
 if row.unitLast>=START_UNIT then
  G:=TransitiveGroup(24,row.k); n:=Size(G); keyStart:=Runtime();
  if n<>row.order or n<2338 or n>50000 then Error("profile order/window mismatch"); fi;
  maps:=GQuotients(G,CyclicGroup(2));
  if Length(maps)<>row.parity or Length(maps)=0 then Error("profile parity mismatch"); fi;
  A:=AutomorphismGroup(G);
  if Size(A)<>row.autOrder then Error("profile Aut order mismatch"); fi;
  if row.method="pc" then
   if not IsSolvableGroup(A) then Error("profile pc method mismatch"); fi;
   isoA:=IsomorphismPcGroup(A); AP:=Image(isoA); allcc:=ConjugacyClasses(AP); pcmode:=true;
  elif row.method="native" then
   if IsSolvableGroup(A) then Error("profile native method mismatch"); fi;
   allcc:=ConjugacyClasses(A); pcmode:=false;
  else Error("unknown profile method"); fi;
  c8:=Filtered(allcc,c->Order(Representative(c))=8);
  if Length(c8)<>row.classes or n*Length(c8)<>row.raw then Error("profile class/raw mismatch"); fi;
  profileKeysRebuilt:=profileKeysRebuilt+1; profileActualMs:=profileActualMs+Runtime()-keyStart;
  AppendTo(OUT,"PROFILE_OK\t24T",row.k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),
   "\tPARITY_MAPS\t",Length(maps),"\tMETHOD\t",row.method,
   "\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",n*Length(c8),
   "\tPLAN_ALPHA_FIRST\t",row.first,"\tPLAN_ALPHA_LAST\t",row.last,
   "\tPROFILE_EXPECTED_MS\t",row.profileMs,"\n");
  elems:=Elements(G); betas:=[]; loci:=[];
  alphaStart:=row.first;
  if START_UNIT>row.unitFirst then alphaStart:=row.first+START_UNIT-row.unitFirst; fi;
  for alphaNo in [alphaStart..row.last] do
   unitNo:=row.unitFirst+alphaNo-row.first; ac:=c8[alphaNo];
   if pcmode then alpha:=PreImagesRepresentative(isoA,Representative(ac));
   else alpha:=Representative(ac); fi;
   invmaps:=InvariantParityMaps(G,alpha,maps);
   cInv:=0; cInvOdd:=0; cOrb:=0; cRel:=0; cB3:=0; cGen:=0; maxB3:=0; survivors:=[];
   if Length(invmaps)>0 then
    invariantAlphaClasses:=invariantAlphaClasses+1; beta:=alpha^4; pos:=Position(betas,beta);
    if pos=fail then
     Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1));
     pos:=Length(betas); betaComputations:=betaComputations+1;
    fi;
    locus:=loci[pos]; cInv:=Length(locus);
    for x in locus do
     if SeedIsOdd(invmaps,x) then
      cInvOdd:=cInvOdd+1; xs:=PhysicalOrbit(alpha,x);
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
    od;
   fi;
   reps:=[];
   if Length(survivors)>0 then
    C:=Centralizer(A,alpha); todo:=ShallowCopy(survivors);
    while Length(todo)>0 do
     x:=todo[1]; Add(reps,x);
     orb:=Orbit(C,x,function(y,c) return Image(c,y); end);
     todo:=Filtered(todo,y->not y in orb);
    od;
   fi;
   repNo:=0;
   for x in reps do
    repNo:=repNo+1; PrintNumericCandidate(OUT,row.k,alphaNo,repNo,n,unitNo,PhysicalOrbit(alpha,x));
   od;
   completedUnits:=completedUnits+1; segmentUnits:=segmentUnits+1;
   rawPairs:=rawPairs+n; segmentRaw:=segmentRaw+n;
   inversePairs:=inversePairs+cInv; inverseOddPairs:=inverseOddPairs+cInvOdd;
   orbit8Pairs:=orbit8Pairs+cOrb; relatorPairs:=relatorPairs+cRel;
   b3Pairs:=b3Pairs+cB3; generatingPairs:=generatingPairs+cGen;
   centralizerOrbits:=centralizerOrbits+Length(reps); candidateNumeric:=candidateNumeric+Length(reps);
   lastUnit:=unitNo; nextUnit:=unitNo+1;
   AppendTo(OUT,"ALPHA_DONE\tUNIT\t",unitNo,"\tKEY\t24T",row.k,"\tALPHA\t",alphaNo,
    "\tCLASS_SIZE\t",Size(ac),"\tINVARIANT_PARITY_MAPS\t",Length(invmaps),
    "\tINVERSE_LOCUS\t",cInv,"\tINVERSE_ODD\t",cInvOdd,"\tORBIT8\t",cOrb,
    "\tRELATOR\t",cRel,"\tMAX_B3\t",maxB3,"\tB3\t",cB3,
    "\tGENERATE\t",cGen,"\tPARITY\t",cGen,"\tCENTRALIZER_ORBITS\t",Length(reps),
    "\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,
    "\tCUM_INVARIANT_ALPHA\t",invariantAlphaClasses,"\tCUM_BETA\t",betaComputations,
    "\tCUM_INVERSE\t",inversePairs,"\tCUM_INVERSE_ODD\t",inverseOddPairs,
    "\tCUM_ORBIT8\t",orbit8Pairs,"\tCUM_RELATOR\t",relatorPairs,
    "\tCUM_B3\t",b3Pairs,"\tCUM_GENERATE\t",generatingPairs,
    "\tCUM_CENTRALIZER_ORBITS\t",centralizerOrbits,
    "\tCUM_CANDIDATE_NUMERIC\t",candidateNumeric,"\tNEXT_UNIT\t",nextUnit,
    "\tMS\t",Runtime()-start,"\n");
   if Length(reps)>0 then stoppedCandidate:=true; break; fi;
   if Runtime()-start>=INTERNAL_GUARD_MS then stoppedGuard:=true; break; fi;
  od;
  if not stoppedGuard and not stoppedCandidate then
   AppendTo(OUT,"KEY_SEGMENT_DONE\t24T",row.k,"\tALPHA_FIRST\t",alphaStart,
    "\tALPHA_LAST\t",row.last,"\tUNIT_LAST\t",row.unitLast,
    "\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,"\n");
  fi;
  if stoppedGuard or stoppedCandidate then break; fi;
 fi;
od;

if stoppedCandidate or stoppedGuard then
 AppendTo(OUT,"TOTAL_PARTIAL\tSTART_UNIT\t",START_UNIT,"\tLAST_COMPLETE_UNIT\t",lastUnit,
  "\tNEXT_UNIT\t",lastUnit+1,"\tSEGMENT_UNITS\t",segmentUnits,
  "\tSEGMENT_RAW\t",segmentRaw,"\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,
  "\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tBETA_COMPUTATIONS\t",betaComputations,
  "\tINVERSE\t",inversePairs,"\tINVERSE_ODD\t",inverseOddPairs,"\tORBIT8\t",orbit8Pairs,
  "\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
  "\tPARITY\t",generatingPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,
  "\tCANDIDATE_NUMERIC\t",candidateNumeric,"\tPROFILE_KEYS_REBUILT\t",profileKeysRebuilt,
  "\tPROFILE_ACTUAL_MS\t",profileActualMs,"\tGAP_MS\t",Runtime()-start,"\n");
 if stoppedCandidate then AppendTo(OUT,"STOPPED_CANDIDATE\n");
 else AppendTo(OUT,"STOPPED_GUARD\n"); fi;
else
 if completedUnits<>14622 or rawPairs<>43149024 then Error("S001 terminal coverage mismatch"); fi;
 AppendTo(OUT,"TOTAL\tSTART_UNIT\t",START_UNIT,"\tLAST_COMPLETE_UNIT\t",lastUnit,
  "\tSEGMENT_UNITS\t",segmentUnits,"\tSEGMENT_RAW\t",segmentRaw,
  "\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,
  "\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tBETA_COMPUTATIONS\t",betaComputations,
  "\tINVERSE\t",inversePairs,"\tINVERSE_ODD\t",inverseOddPairs,"\tORBIT8\t",orbit8Pairs,
  "\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
  "\tPARITY\t",generatingPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,
  "\tCANDIDATE_NUMERIC\t",candidateNumeric,"\tPROFILE_KEYS_REBUILT\t",profileKeysRebuilt,
  "\tPROFILE_ACTUAL_MS\t",profileActualMs,"\tGAP_MS\t",Runtime()-start,"\nDONE\n");
fi;
Print("WROTE ",OUT,"\n"); QUIT;
