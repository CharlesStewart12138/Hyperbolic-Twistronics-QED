# Frozen degree-24 C8 seed predicate for one sealed lexicographic alpha shard.
# Recovery commits one alpha at a time to an atomically replaced checkpoint.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if LoadPackage("io")=fail then Error("IO package required"); fi;
HexSHA256Padded:=function(value) local result;
 result:=HexSHA256(value);
 while Length(result)<64 do result:=Concatenation("0",result); od;
 if Length(result)<>64 then Error("SHA256 width"); fi;
 return result;
end;
S076AtomicReplaceVerified:=function(oldpath,newpath)
 local attempt,result,expectedText;
 if not IsExistingFile(oldpath) then return false; fi;
 expectedText:=StringFile(oldpath);
 for attempt in [1..500] do
  result:=IO_rename(oldpath,newpath);
  if result=true then
   if IsExistingFile(oldpath) or not IsExistingFile(newpath) or StringFile(newpath)<>expectedText then
    Print("ATOMIC_RENAME_POSTVERIFY_FAIL\tATTEMPTS\t",attempt,"\n");
    return false;
   fi;
   if attempt>1 then Print("ATOMIC_RENAME_RETRY_SUCCESS\tATTEMPTS\t",attempt,"\n"); fi;
   return true;
  fi;
  IO_select([],[],[],0,20000);
 od;
 Print("ATOMIC_RENAME_RETRY_EXHAUSTED\tATTEMPTS\t500\n");
 return false;
end;
required:=["S076_RECORDS","OUT","CHECKPOINT_FILE","CHECKPOINT_TMP","INTERNAL_GUARD_MS",
 "START_UNIT","INITIAL_COUNTERS","PREVIOUS_CHECKPOINT_SHA256","PREVIOUS_OUTPUT_FILE",
 "PREVIOUS_OUTPUT_PREFIX_BYTES","PREVIOUS_OUTPUT_PREFIX_SHA256",
 "EXPECTED_PROFILE_SHA256","EXPECTED_PLAN_SHA256","ENGINE_FILE","EXPECTED_ENGINE_SHA256",
 "PROFILE_FILE","PLAN_FILE"];
if ForAny(required,n->not IsBoundGlobal(n)) then Error("seed wrapper variable missing"); fi;
if not IsBound(STOP_AFTER_UNIT) then STOP_AFTER_UNIT:=fail; fi;
d:=24; db:=NrTransitiveGroups(d);
if db<>25000 then Error("degree-24 catalogue mismatch"); fi;
if HexSHA256Padded(StringFile(ENGINE_FILE))<>LowercaseString(EXPECTED_ENGINE_SHA256) then Error("engine hash mismatch"); fi;
if HexSHA256Padded(StringFile(PROFILE_FILE))<>LowercaseString(EXPECTED_PROFILE_SHA256) then Error("profile hash mismatch"); fi;
if HexSHA256Padded(StringFile(PLAN_FILE))<>LowercaseString(EXPECTED_PLAN_SHA256) then Error("plan hash mismatch"); fi;
if Length(INITIAL_COUNTERS)<>12 then Error("INITIAL_COUNTERS length"); fi;

InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(alpha,x) local xs,j;
 xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od; return xs;
end;
RelatorHolds:=function(G,xs)
 return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]);
end;
B3Cardinality:=function(G,xs) local vals,frontier,next,item,j,z,depth;
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
PrintNumericCandidate:=function(out,k,alphaNo,repNo,n,xs) local p,i;
 # Canonical degrees42/44/45 replay schema: key, alpha, rep, order, degree, 8*d images.
 AppendTo(out,"CANDIDATE_NUMERIC\t24T",k,"\t",alphaNo,"\t",repNo,"\t",n,"\t24");
 for p in xs do for i in [1..24] do AppendTo(out,"\t",i^p-1); od; od;
 AppendTo(out,"\n");
end;

# Exact wrapper slice and prefix-state validation before any seed work.
if Length(S076_RECORDS)<>16 then Error("S076 record count"); fi;
planUnits:=0; planRaw:=0; planProfileMs:=0; previousKey:=0; expectedUnitFirst:=1;
for row in S076_RECORDS do
 if row.k<=previousKey then Error("S076 key order"); fi;
 if row.first<1 or row.last<row.first or row.last>row.classes then Error("S076 alpha interval"); fi;
 if row.unitFirst<>expectedUnitFirst or row.unitLast-row.unitFirst<>row.last-row.first then Error("S076 unit continuity"); fi;
 if row.raw<>row.order*row.classes then Error("S076 full raw identity"); fi;
 if row.method="pc" then
  if (row.representation<>"legacy_sealed_pc" and row.representation<>"original" and row.representation<>"pc_transport") or row.pcOrder<>row.order then Error("S076 pc representation"); fi;
 elif row.method="native" then
  if not ((row.representation="legacy_original_native" and row.pcOrder=0) or ((row.representation="pc_single" or row.representation="pc_transport") and row.pcOrder=row.order)) then Error("S076 native representation"); fi;
 else Error("S076 method"); fi;
 planUnits:=planUnits+row.last-row.first+1;
 planRaw:=planRaw+row.order*(row.last-row.first+1);
 planProfileMs:=planProfileMs+row.profileMs;
 previousKey:=row.k; expectedUnitFirst:=row.unitLast+1;
od;
if S076_RECORDS[1].k<>11389 or S076_RECORDS[1].first<>80 or
   S076_RECORDS[Length(S076_RECORDS)].k<>11404 or
   S076_RECORDS[Length(S076_RECORDS)].last<>57 then Error("S076 endpoint"); fi;
if planUnits<>3662 or planRaw<>44998656 or planProfileMs<>11892 or expectedUnitFirst<>3663 then Error("S076 checksum"); fi;
if START_UNIT<1 or START_UNIT>3663 or INITIAL_COUNTERS[1]<>START_UNIT-1 then Error("S076 recovery unit"); fi;
prefixRaw:=0;
for row in S076_RECORDS do
 if START_UNIT>row.unitFirst then
  prefixTaken:=Minimum(row.unitLast,START_UNIT-1)-row.unitFirst+1;
  if prefixTaken>0 then prefixRaw:=prefixRaw+prefixTaken*row.order; fi;
 fi;
od;
if INITIAL_COUNTERS[2]<>prefixRaw then Error("S076 recovery raw"); fi;
if Minimum(INITIAL_COUNTERS)<0 or INITIAL_COUNTERS[3]>INITIAL_COUNTERS[1] or
   INITIAL_COUNTERS[4]>INITIAL_COUNTERS[3] or INITIAL_COUNTERS[5]>INITIAL_COUNTERS[2] or
   INITIAL_COUNTERS[6]>INITIAL_COUNTERS[5] or INITIAL_COUNTERS[7]>INITIAL_COUNTERS[6] or
   INITIAL_COUNTERS[8]>INITIAL_COUNTERS[7] or INITIAL_COUNTERS[9]>INITIAL_COUNTERS[8] or
   INITIAL_COUNTERS[10]>INITIAL_COUNTERS[9] or INITIAL_COUNTERS[11]>INITIAL_COUNTERS[10] or
   INITIAL_COUNTERS[12]<>INITIAL_COUNTERS[11] then Error("S076 recovery counter inequalities"); fi;
if IsExistingFile(OUT) then Error("refusing to overwrite output"); fi;
if IsExistingFile(CHECKPOINT_TMP) then Error("stale checkpoint temp"); fi;
if START_UNIT=1 then
 if IsExistingFile(CHECKPOINT_FILE) then Error("refusing to overwrite fresh checkpoint"); fi;
 if PREVIOUS_CHECKPOINT_SHA256<>"NONE_FRESH_START" or PREVIOUS_OUTPUT_PREFIX_BYTES<>0 then Error("fresh recovery metadata"); fi;
else
 if not IsExistingFile(CHECKPOINT_FILE) or HexSHA256Padded(StringFile(CHECKPOINT_FILE))<>PREVIOUS_CHECKPOINT_SHA256 then Error("prior checkpoint hash"); fi;
 if not IsExistingFile(PREVIOUS_OUTPUT_FILE) then Error("prior output missing"); fi;
 priorText:=StringFile(PREVIOUS_OUTPUT_FILE);
 if Length(priorText)<PREVIOUS_OUTPUT_PREFIX_BYTES or
    HexSHA256Padded(priorText{[1..PREVIOUS_OUTPUT_PREFIX_BYTES]})<>PREVIOUS_OUTPUT_PREFIX_SHA256 then Error("prior output prefix hash"); fi;
fi;

PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE24-SEED-SHARD076-V2\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nDEGREE\t24\nDATABASE\t",db,"\n",
 "PLAN_FIRST\t24T11389\t80\nPLAN_LAST\t24T11404\t57\nPLAN_KEYS\t16\n",
 "PLAN_CLASS_UNITS\t3662\nPLAN_RAW_PAIRS\t44998656\nPLAN_PROFILE_REBUILD_MS\t11892\n",
 "INTERNAL_GUARD_MS\t",INTERNAL_GUARD_MS,"\nSTART_UNIT\t",START_UNIT,"\n",
 "PREVIOUS_CHECKPOINT_SHA256\t",PREVIOUS_CHECKPOINT_SHA256,"\n",
 "PROFILE_SHA256\t",EXPECTED_PROFILE_SHA256,"\nPLAN_SHA256\t",EXPECTED_PLAN_SHA256,"\n",
 "FROZEN\tg_j=alpha^j(x); alpha^4(x)=x^-1; relator indices 0,5,2,7,4,1,6,3; B3=457; generated image exact; invariant odd C2 parity exact.\n",
 "RECOVERY\tPer-alpha temp-write plus bounded IO_rename retry; source absence, destination presence, and exact destination bytes are verified after rename; output-prefix SHA256/bytes and exact successor are recorded.\n",
 "SCOPE\tExactly seed-plan shard076 only; shard077 and later are excluded.\n");

completedUnits:=INITIAL_COUNTERS[1]; rawPairs:=INITIAL_COUNTERS[2];
invariantAlphaClasses:=INITIAL_COUNTERS[3]; betaComputations:=INITIAL_COUNTERS[4];
inversePairs:=INITIAL_COUNTERS[5]; inverseOddPairs:=INITIAL_COUNTERS[6];
orbit8Pairs:=INITIAL_COUNTERS[7]; relatorPairs:=INITIAL_COUNTERS[8];
b3Pairs:=INITIAL_COUNTERS[9]; generatingPairs:=INITIAL_COUNTERS[10];
centralizerOrbits:=INITIAL_COUNTERS[11]; candidateNumeric:=INITIAL_COUNTERS[12];
segmentUnits:=0; segmentRaw:=0; profileKeysRebuilt:=0; profileActualMs:=0;
start:=Runtime(); stoppedGuard:=false; stoppedCandidate:=false; stoppedTest:=false; lastUnit:=START_UNIT-1;
checkpointSha:=PREVIOUS_CHECKPOINT_SHA256;

for row in S076_RECORDS do
 if row.unitLast>=START_UNIT and START_UNIT<=3662 then
  G0:=TransitiveGroup(24,row.k); n:=Size(G0); keyStart:=Runtime();
  if n<>row.order or n<2338 or n>50000 then Error("profile order/window mismatch"); fi;
  transportG:=row.representation="pc_single" or row.representation="pc_transport";
  if transportG then
   isoG:=IsomorphismPcGroup(G0); G:=Image(isoG);
   if Size(G)<>n or row.pcOrder<>Size(G) then Error("profile transported-domain mismatch"); fi;
   mapsOriginal:=GQuotients(G0,CyclicGroup(2)); maps:=GQuotients(G,CyclicGroup(2));
   if Length(mapsOriginal)<>row.parity or Length(maps)<>row.parity or Length(maps)=0 then Error("profile transported parity mismatch"); fi;
   AppendTo(OUT,"TRANSPORT_OK\t24T",row.k,"\tREPRESENTATION\t",row.representation,
    "\tORIGINAL_ORDER\t",n,"\tPC_ORDER\t",Size(G),"\tPARITY_ORIGINAL\t",Length(mapsOriginal),
    "\tPARITY_PC\t",Length(maps),"\n");
  else
   G:=G0; maps:=GQuotients(G,CyclicGroup(2));
   if Length(maps)<>row.parity or Length(maps)=0 then Error("profile parity mismatch"); fi;
  fi;
  A:=AutomorphismGroup(G);
  if Size(A)<>row.autOrder then Error("profile Aut order mismatch"); fi;
  if row.method="pc" then
   if not IsSolvableGroup(A) then Error("profile pc method mismatch"); fi;
   isoA:=IsomorphismPcGroup(A); AP:=Image(isoA); allcc:=ConjugacyClasses(AP); pcmode:=true;
  else
   if IsSolvableGroup(A) then Error("profile native method mismatch"); fi;
   allcc:=ConjugacyClasses(A); pcmode:=false;
  fi;
  c8:=Filtered(allcc,c->Order(Representative(c))=8);
  if Length(c8)<>row.classes or n*Length(c8)<>row.raw then Error("profile class/raw mismatch"); fi;
  profileKeysRebuilt:=profileKeysRebuilt+1; profileActualMs:=profileActualMs+Runtime()-keyStart;
  AppendTo(OUT,"PROFILE_OK\t24T",row.k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),
   "\tPARITY_MAPS\t",Length(maps),"\tMETHOD\t",row.method,"\tREPRESENTATION\t",row.representation,
   "\tPC_ORDER\t",row.pcOrder,"\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",n*Length(c8),
   "\tPLAN_ALPHA_FIRST\t",row.first,"\tPLAN_ALPHA_LAST\t",row.last,
   "\tPROFILE_EXPECTED_MS\t",row.profileMs,"\n");
  elems:=Elements(G); betas:=[]; loci:=[];
  alphaStart:=row.first;
  if START_UNIT>row.unitFirst then alphaStart:=row.first+START_UNIT-row.unitFirst; fi;
  # Reconstruct only the current-key beta cache on recovery; no seed predicate is replayed.
  if alphaStart>row.first then
   for priorAlphaNo in [row.first..alphaStart-1] do
    priorAc:=c8[priorAlphaNo];
    if pcmode then priorAlpha:=PreImagesRepresentative(isoA,Representative(priorAc));
    else priorAlpha:=Representative(priorAc); fi;
    beta:=priorAlpha^4; pos:=Position(betas,beta);
    if pos=fail then
     Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1));
    fi;
   od;
   AppendTo(OUT,"CACHE_REBUILT\t24T",row.k,"\tALPHA_FIRST\t",row.first,
    "\tALPHA_LAST\t",alphaStart-1,"\tDISTINCT_BETA\t",Length(betas),"\tSEED_PREDICATES_REPLAYED\t0\n");
  fi;
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
    repNo:=repNo+1; seedCandidateXs:=PhysicalOrbit(alpha,x); candidateXs:=seedCandidateXs;
    if transportG then
     candidateXs:=List(seedCandidateXs,y->PreImagesRepresentative(isoG,y));
     if ForAny(candidateXs,y->y=fail or not IsPerm(y) or not (y in G0)) or not ForAll([1..8],j->Image(isoG,candidateXs[j])=seedCandidateXs[j]) then Error("candidate transport mismatch"); fi;
    fi;
    PrintNumericCandidate(OUT,row.k,alphaNo,repNo,n,candidateXs);
    AppendTo(OUT,"CANDIDATE_META\tUNIT\t",unitNo,"\tKEY\t24T",row.k,
     "\tALPHA\t",alphaNo,"\tREP\t",repNo,"\tINVARIANT_PARITY_MAPS\t",Length(invmaps),"\n");
   od;
   completedUnits:=completedUnits+1; segmentUnits:=segmentUnits+1;
   rawPairs:=rawPairs+n; segmentRaw:=segmentRaw+n;
   inversePairs:=inversePairs+cInv; inverseOddPairs:=inverseOddPairs+cInvOdd;
   orbit8Pairs:=orbit8Pairs+cOrb; relatorPairs:=relatorPairs+cRel;
   b3Pairs:=b3Pairs+cB3; generatingPairs:=generatingPairs+cGen;
   centralizerOrbits:=centralizerOrbits+Length(reps); candidateNumeric:=candidateNumeric+Length(reps);
   lastUnit:=unitNo; nextUnit:=unitNo+1;
   alphaLine:=Concatenation("ALPHA_DONE\tUNIT\t",String(unitNo),"\tKEY\t24T",String(row.k),
    "\tALPHA\t",String(alphaNo),"\tCLASS_SIZE\t",String(Size(ac)),
    "\tINVARIANT_PARITY_MAPS\t",String(Length(invmaps)),"\tINVERSE_LOCUS\t",String(cInv),
    "\tINVERSE_ODD\t",String(cInvOdd),"\tORBIT8\t",String(cOrb),"\tRELATOR\t",String(cRel),
    "\tMAX_B3\t",String(maxB3),"\tB3\t",String(cB3),"\tGENERATE\t",String(cGen),
    "\tPARITY\t",String(cGen),"\tCENTRALIZER_ORBITS\t",String(Length(reps)),
    "\tCUM_UNITS\t",String(completedUnits),"\tCUM_RAW\t",String(rawPairs),
    "\tCUM_INVARIANT_ALPHA\t",String(invariantAlphaClasses),"\tCUM_BETA\t",String(betaComputations),
    "\tCUM_INVERSE\t",String(inversePairs),"\tCUM_INVERSE_ODD\t",String(inverseOddPairs),
    "\tCUM_ORBIT8\t",String(orbit8Pairs),"\tCUM_RELATOR\t",String(relatorPairs),
    "\tCUM_B3\t",String(b3Pairs),"\tCUM_GENERATE\t",String(generatingPairs),
    "\tCUM_CENTRALIZER_ORBITS\t",String(centralizerOrbits),
    "\tCUM_CANDIDATE_NUMERIC\t",String(candidateNumeric),"\tNEXT_UNIT\t",String(nextUnit),
    "\tPREVIOUS_CHECKPOINT_SHA256\t",checkpointSha,"\tMS\t",String(Runtime()-start));
   AppendTo(OUT,alphaLine,"\n");
   outText:=StringFile(OUT); outBytes:=Length(outText); outSha:=HexSHA256Padded(outText);
   checkpointPayload:=Concatenation("SHARD\t076\tUNIT\t",String(unitNo),"\tKEY\t24T",String(row.k),
    "\tALPHA\t",String(alphaNo),"\tNEXT_UNIT\t",String(nextUnit),
    "\tCUM_UNITS\t",String(completedUnits),"\tCUM_RAW\t",String(rawPairs),
    "\tCUM_INVARIANT_ALPHA\t",String(invariantAlphaClasses),"\tCUM_BETA\t",String(betaComputations),
    "\tCUM_INVERSE\t",String(inversePairs),"\tCUM_INVERSE_ODD\t",String(inverseOddPairs),
    "\tCUM_ORBIT8\t",String(orbit8Pairs),"\tCUM_RELATOR\t",String(relatorPairs),
    "\tCUM_B3\t",String(b3Pairs),"\tCUM_GENERATE\t",String(generatingPairs),
    "\tCUM_CENTRALIZER_ORBITS\t",String(centralizerOrbits),
    "\tCUM_CANDIDATE_NUMERIC\t",String(candidateNumeric),
    "\tOUTPUT_PREFIX_BYTES\t",String(outBytes),"\tOUTPUT_PREFIX_SHA256\t",outSha,
    "\tPREVIOUS_CHECKPOINT_SHA256\t",checkpointSha,
    "\tPROFILE_SHA256\t",EXPECTED_PROFILE_SHA256,"\tPLAN_SHA256\t",EXPECTED_PLAN_SHA256);
   checkpointPayloadSha:=HexSHA256Padded(checkpointPayload);
   PrintTo(CHECKPOINT_TMP,"CERTIFICATE_CHECKPOINT\tPF-GRP-001-C8-DEGREE24-SEED-SHARD076\n",
    checkpointPayload,"\tPAYLOAD_SHA256\t",checkpointPayloadSha,"\nDONE\n");
   if not S076AtomicReplaceVerified(CHECKPOINT_TMP,CHECKPOINT_FILE) then Error("atomic checkpoint rename/postverify failed"); fi;
   checkpointSha:=HexSHA256Padded(StringFile(CHECKPOINT_FILE));
   AppendTo(OUT,"CHECKPOINT_COMMITTED\tUNIT\t",unitNo,"\tCHECKPOINT_SHA256\t",checkpointSha,
    "\tOUTPUT_PREFIX_BYTES\t",outBytes,"\tOUTPUT_PREFIX_SHA256\t",outSha,"\n");
   if Length(reps)>0 then stoppedCandidate:=true; break; fi;
   if STOP_AFTER_UNIT<>fail and unitNo=STOP_AFTER_UNIT then stoppedTest:=true; break; fi;
   if Runtime()-start>=INTERNAL_GUARD_MS then stoppedGuard:=true; break; fi;
  od;
  if not stoppedGuard and not stoppedCandidate and not stoppedTest then
   AppendTo(OUT,"KEY_SEGMENT_DONE\t24T",row.k,"\tALPHA_FIRST\t",alphaStart,
    "\tALPHA_LAST\t",row.last,"\tUNIT_LAST\t",row.unitLast,
    "\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,"\n");
  fi;
  if stoppedGuard or stoppedCandidate or stoppedTest then break; fi;
 fi;
od;

if stoppedCandidate or stoppedGuard or stoppedTest then
 AppendTo(OUT,"TOTAL_PARTIAL\tSTART_UNIT\t",START_UNIT,"\tLAST_COMPLETE_UNIT\t",lastUnit,
  "\tNEXT_UNIT\t",lastUnit+1,"\tSEGMENT_UNITS\t",segmentUnits,"\tSEGMENT_RAW\t",segmentRaw,
  "\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,
  "\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tBETA_COMPUTATIONS\t",betaComputations,
  "\tINVERSE\t",inversePairs,"\tINVERSE_ODD\t",inverseOddPairs,"\tORBIT8\t",orbit8Pairs,
  "\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
  "\tPARITY\t",generatingPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,
  "\tCANDIDATE_NUMERIC\t",candidateNumeric,"\tPROFILE_KEYS_REBUILT\t",profileKeysRebuilt,
  "\tPROFILE_ACTUAL_MS\t",profileActualMs,"\tFINAL_CHECKPOINT_SHA256\t",checkpointSha,
  "\tGAP_MS\t",Runtime()-start,"\n");
 if stoppedCandidate then AppendTo(OUT,"STOPPED_CANDIDATE\n");
 elif stoppedTest then AppendTo(OUT,"STOPPED_RECOVERY_SMOKE\n");
 else AppendTo(OUT,"STOPPED_GUARD\n"); fi;
else
 if completedUnits<>3662 or rawPairs<>44998656 or lastUnit<>3662 then Error("S076 terminal coverage"); fi;
 AppendTo(OUT,"TOTAL\tSTART_UNIT\t",START_UNIT,"\tLAST_COMPLETE_UNIT\t",lastUnit,
  "\tSEGMENT_UNITS\t",segmentUnits,"\tSEGMENT_RAW\t",segmentRaw,
  "\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,
  "\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tBETA_COMPUTATIONS\t",betaComputations,
  "\tINVERSE\t",inversePairs,"\tINVERSE_ODD\t",inverseOddPairs,"\tORBIT8\t",orbit8Pairs,
  "\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,
  "\tPARITY\t",generatingPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,
  "\tCANDIDATE_NUMERIC\t",candidateNumeric,"\tPROFILE_KEYS_REBUILT\t",profileKeysRebuilt,
  "\tPROFILE_ACTUAL_MS\t",profileActualMs,"\tFINAL_CHECKPOINT_SHA256\t",checkpointSha,
  "\tGAP_MS\t",Runtime()-start,"\nDONE\n");
fi;
Print("WROTE ",OUT,"\n"); QUIT_GAP(0);
