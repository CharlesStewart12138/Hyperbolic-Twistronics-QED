# Execute one explicit CLASS_ID_V3 segment. No conjugacy-class ordinal is used.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if LoadPackage("io")=fail then Error("IO package required"); fi;
required:=["SEGMENT_FILE","EXPECTED_SEGMENT_FILE_SHA256","OUT","CHECKPOINT_FILE","CHECKPOINT_TMP","START_INDEX","INITIAL_COUNTERS","PREVIOUS_CHECKPOINT_SHA256","PREVIOUS_OUTPUT_FILE","PREVIOUS_OUTPUT_PREFIX_BYTES","PREVIOUS_OUTPUT_PREFIX_SHA256","INTERNAL_GUARD_MS"];
if ForAny(required,n->not IsBoundGlobal(n)) then Error("V3 segment wrapper variable missing"); fi;
if not IsBound(STOP_AFTER_INDEX) then STOP_AFTER_INDEX:=fail; fi;
HexSHA256Padded:=function(value) local result;
 result:=HexSHA256(value); while Length(result)<64 do result:=Concatenation("0",result); od;
 if Length(result)<>64 then Error("SHA256 width"); fi; return LowercaseString(result);
end;
AtomicReplaceVerified:=function(oldpath,newpath) local attempt,result,expectedText;
 if not IsExistingFile(oldpath) then return false; fi; expectedText:=StringFile(oldpath);
 for attempt in [1..500] do
  result:=IO_rename(oldpath,newpath);
  if result=true then
   if IsExistingFile(oldpath) or not IsExistingFile(newpath) or StringFile(newpath)<>expectedText then return false; fi;
   return true;
  fi;
  IO_select([],[],[],0,20000);
 od; return false;
end;
PermSerialization:=function(p) return JoinStringsWithSeparator(List([1..24],i->String(i^p)),","); end;
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(alpha,x) local xs,j; xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od; return xs; end;
RelatorHolds:=function(G,xs) return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]); end;
B3Cardinality:=function(G,xs) local vals,frontier,next,item,j,z,depth;
 vals:=[One(G)]; frontier:=[[One(G),0]];
 for depth in [1..3] do next:=[]; for item in frontier do for j in [1..8] do
  if item[2]=0 or j<>InvPhysicalIndex(item[2]) then z:=item[1]*xs[j]; Add(vals,z); Add(next,[z,j]); fi;
 od; od; frontier:=next; od; return Size(Set(vals));
end;
InvariantParityMaps:=function(G,alpha,maps) local gens; gens:=GeneratorsOfGroup(G); return Filtered(maps,f->ForAll(gens,g->Image(f,Image(alpha,g))=Image(f,g))); end;
SeedIsOdd:=function(maps,x) return ForAny(maps,f->not IsOne(Image(f,x))); end;
PrintNumericCandidate:=function(out,k,classId,repNo,n,xs) local p,i;
 AppendTo(out,"CANDIDATE_NUMERIC_V3\t24T",k,"\t",classId,"\t",repNo,"\t",n,"\t24");
 for p in xs do for i in [1..24] do AppendTo(out,"\t",i^p-1); od; od; AppendTo(out,"\n");
end;

if HexSHA256Padded(StringFile(SEGMENT_FILE))<>LowercaseString(EXPECTED_SEGMENT_FILE_SHA256) then Error("segment file hash mismatch"); fi;
Read(SEGMENT_FILE); r:=D24C8_SEGMENT_META; records:=D24C8_SEGMENT_RECORDS;
if Length(records)<>r.classCount or r.rawPairs<>r.groupOrder*r.classCount or Length(Set(List(records,x->x.classId)))<>Length(records) then Error("segment metadata/identity mismatch"); fi;
if START_INDEX<1 or START_INDEX>Length(records)+1 or Length(INITIAL_COUNTERS)<>12 or INITIAL_COUNTERS[1]<>START_INDEX-1 or INITIAL_COUNTERS[2]<>(START_INDEX-1)*r.groupOrder then Error("checkpoint start mismatch"); fi;
if IsExistingFile(OUT) or IsExistingFile(CHECKPOINT_TMP) then Error("refusing overwrite/stale tmp"); fi;
if START_INDEX=1 then
 if IsExistingFile(CHECKPOINT_FILE) then Error("fresh segment has checkpoint"); fi;
 if PREVIOUS_CHECKPOINT_SHA256<>"NONE_FRESH_START" or PREVIOUS_OUTPUT_PREFIX_BYTES<>0 then Error("fresh metadata mismatch"); fi;
else
 if not IsExistingFile(CHECKPOINT_FILE) or HexSHA256Padded(StringFile(CHECKPOINT_FILE))<>LowercaseString(PREVIOUS_CHECKPOINT_SHA256) then Error("prior checkpoint hash mismatch"); fi;
 if not IsExistingFile(PREVIOUS_OUTPUT_FILE) then Error("previous output missing"); fi;
 priorText:=StringFile(PREVIOUS_OUTPUT_FILE);
 if Length(priorText)<PREVIOUS_OUTPUT_PREFIX_BYTES or HexSHA256Padded(priorText{[1..PREVIOUS_OUTPUT_PREFIX_BYTES]})<>LowercaseString(PREVIOUS_OUTPUT_PREFIX_SHA256) then Error("previous output prefix mismatch"); fi;
fi;

start:=Runtime(); G0:=TransitiveGroup(24,r.key); gens0:=GeneratorsOfGroup(G0);
if Size(G0)<>r.groupOrder then Error("group order mismatch"); fi;
generatorSerialization:=JoinStringsWithSeparator(List(gens0,PermSerialization),";");
if HexSHA256Padded(generatorSerialization)<>LowercaseString(r.generatorTupleSha256) then Error("generator tuple hash mismatch"); fi;
transportG:=r.representation="pc_single" or r.representation="pc_transport";
if transportG then isoG:=IsomorphismPcGroup(G0); G:=Image(isoG); else G:=G0; fi;
maps:=GQuotients(G,CyclicGroup(2)); if Length(maps)<>r.parity then Error("parity mismatch"); fi;
A:=AutomorphismGroup(G); if Size(A)<>r.autOrder then Error("Aut order mismatch"); fi;
elems:=Elements(G); gensG:=GeneratorsOfGroup(G);
ReconstructAlpha:=function(row) local imgs0,alpha0,preG,imgsG,alpha,serialization,payload;
 imgs0:=List(row.images,PermList); alpha0:=GroupHomomorphismByImages(G0,G0,gens0,imgs0);
 if alpha0=fail or not IsBijective(alpha0) or Order(alpha0)<>8 then Error("explicit representative reconstruction failed"); fi;
 serialization:=JoinStringsWithSeparator(List(imgs0,PermSerialization),";");
 payload:=Concatenation("KEY_ID=24T",String(r.key),"\nSCHEMA=",r.schema,"\nGENERATOR_TUPLE_SHA256=",r.generatorTupleSha256,"\nREPRESENTATIVE_SERIALIZATION=",serialization,"\nCLASS_SIZE=",String(row.classSize),"\nORDER=",String(row.order),"\nCENTRALIZER_SIZE=",String(row.centralizerSize),"\n");
 if HexSHA256Padded(payload)<>LowercaseString(row.classId) then Error("CLASS_ID_V3 content hash mismatch"); fi;
 if transportG then
  preG:=List(gensG,g->PreImagesRepresentative(isoG,g)); imgsG:=List(preG,x0->Image(isoG,Image(alpha0,x0)));
  alpha:=GroupHomomorphismByImages(G,G,gensG,imgsG);
 else alpha:=alpha0; fi;
 if alpha=fail or not IsBijective(alpha) or not (alpha in A) then Error("reconstructed alpha not in Aut(G)"); fi;
 return alpha;
end;

PrintTo(OUT,"CERTIFICATE\tDEG24_SPLIT_HEAVY_REPAIR_SEGMENT_V3\nGAP_VERSION\t",GAPInfo.Version,"\nSEGMENT_ID\t",r.segmentId,"\nKEY_ID\t24T",r.key,"\nCLASS_COUNT\t",r.classCount,"\nRAW_PAIRS\t",r.rawPairs,"\nSTART_INDEX\t",START_INDEX,"\nSEGMENT_FILE_SHA256\t",EXPECTED_SEGMENT_FILE_SHA256,"\nMANIFEST_SHA256\t",r.manifestSha256,"\nCLASS_ID_LIST_SHA256\t",r.classIdListSha256,"\nIDENTITY_CONTRACT\tExplicit frozen representatives and content-bound CLASS_ID_V3; ordinal is diagnostic only.\n");
completedUnits:=INITIAL_COUNTERS[1]; rawPairs:=INITIAL_COUNTERS[2]; invariantAlphaClasses:=INITIAL_COUNTERS[3]; betaComputations:=INITIAL_COUNTERS[4]; inversePairs:=INITIAL_COUNTERS[5]; inverseOddPairs:=INITIAL_COUNTERS[6]; orbit8Pairs:=INITIAL_COUNTERS[7]; relatorPairs:=INITIAL_COUNTERS[8]; b3Pairs:=INITIAL_COUNTERS[9]; generatingPairs:=INITIAL_COUNTERS[10]; centralizerOrbits:=INITIAL_COUNTERS[11]; candidateNumeric:=INITIAL_COUNTERS[12]; checkpointSha:=PREVIOUS_CHECKPOINT_SHA256; stoppedGuard:=false; stoppedTest:=false; lastIndex:=START_INDEX-1; betas:=[]; loci:=[];
if START_INDEX>1 then
 for priorIndex in [1..START_INDEX-1] do priorAlpha:=ReconstructAlpha(records[priorIndex]); beta:=priorAlpha^4; pos:=Position(betas,beta); if pos=fail then Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1)); fi; od;
 AppendTo(OUT,"CACHE_REBUILT\tCLASS_FIRST\t1\tCLASS_LAST\t",START_INDEX-1,"\tDISTINCT_BETA\t",Length(betas),"\tSEED_PREDICATES_REPLAYED\t0\n");
fi;
if START_INDEX<=Length(records) then
 for index in [START_INDEX..Length(records)] do
  row:=records[index]; alpha:=ReconstructAlpha(row); invmaps:=InvariantParityMaps(G,alpha,maps); cInv:=0; cInvOdd:=0; cOrb:=0; cRel:=0; cB3:=0; cGen:=0; maxB3:=0; survivors:=[];
  if Length(invmaps)>0 then
   invariantAlphaClasses:=invariantAlphaClasses+1; beta:=alpha^4; pos:=Position(betas,beta);
   if pos=fail then Add(betas,beta); Add(loci,Filtered(elems,x->Image(beta,x)=x^-1)); pos:=Length(betas); betaComputations:=betaComputations+1; fi;
   locus:=loci[pos]; cInv:=Length(locus);
   for x in locus do if SeedIsOdd(invmaps,x) then cInvOdd:=cInvOdd+1; xs:=PhysicalOrbit(alpha,x); if Size(Set(xs))=8 then cOrb:=cOrb+1; if RelatorHolds(G,xs) then cRel:=cRel+1; b:=B3Cardinality(G,xs); if b>maxB3 then maxB3:=b; fi; if b=457 then cB3:=cB3+1; if Size(Group(xs))=Size(G) then cGen:=cGen+1; Add(survivors,x); fi; fi; fi; fi; fi; od;
  fi;
  reps:=[]; if Length(survivors)>0 then C:=Centralizer(A,alpha); todo:=ShallowCopy(survivors); while Length(todo)>0 do x:=todo[1]; Add(reps,x); orb:=Orbit(C,x,function(y,c) return Image(c,y); end); todo:=Filtered(todo,y->not y in orb); od; fi;
  for repNo in [1..Length(reps)] do x:=reps[repNo]; candidateXs:=PhysicalOrbit(alpha,x); if transportG then candidateXs:=List(candidateXs,y->PreImagesRepresentative(isoG,y)); fi; PrintNumericCandidate(OUT,r.key,row.classId,repNo,Size(G0),candidateXs); AppendTo(OUT,"CANDIDATE_META_V3\tSEGMENT\t",r.segmentId,"\tCLASS_ID_V3\t",row.classId,"\tREP\t",repNo,"\n"); od;
  completedUnits:=completedUnits+1; rawPairs:=rawPairs+r.groupOrder; inversePairs:=inversePairs+cInv; inverseOddPairs:=inverseOddPairs+cInvOdd; orbit8Pairs:=orbit8Pairs+cOrb; relatorPairs:=relatorPairs+cRel; b3Pairs:=b3Pairs+cB3; generatingPairs:=generatingPairs+cGen; centralizerOrbits:=centralizerOrbits+Length(reps); candidateNumeric:=candidateNumeric+Length(reps); lastIndex:=index; nextIndex:=index+1;
  alphaLine:=Concatenation("CLASS_DONE\tINDEX\t",String(index),"\tKEY\t24T",String(r.key),"\tCLASS_ID_V3\t",row.classId,"\tREPRESENTATIVE_FINGERPRINT\t",row.classId,"\tMANIFEST_POSITION_DIAGNOSTIC\t",String(row.manifestPositionDiagnostic),"\tCLASS_SIZE\t",String(row.classSize),"\tINVARIANT_PARITY_MAPS\t",String(Length(invmaps)),"\tINVERSE_LOCUS\t",String(cInv),"\tINVERSE_ODD\t",String(cInvOdd),"\tORBIT8\t",String(cOrb),"\tRELATOR\t",String(cRel),"\tMAX_B3\t",String(maxB3),"\tB3\t",String(cB3),"\tGENERATE\t",String(cGen),"\tCENTRALIZER_ORBITS\t",String(Length(reps)),"\tCUM_UNITS\t",String(completedUnits),"\tCUM_RAW\t",String(rawPairs),"\tCUM_INVARIANT_ALPHA\t",String(invariantAlphaClasses),"\tCUM_BETA\t",String(betaComputations),"\tCUM_INVERSE\t",String(inversePairs),"\tCUM_INVERSE_ODD\t",String(inverseOddPairs),"\tCUM_ORBIT8\t",String(orbit8Pairs),"\tCUM_RELATOR\t",String(relatorPairs),"\tCUM_B3\t",String(b3Pairs),"\tCUM_GENERATE\t",String(generatingPairs),"\tCUM_CENTRALIZER_ORBITS\t",String(centralizerOrbits),"\tCUM_CANDIDATE_NUMERIC\t",String(candidateNumeric),"\tNEXT_INDEX\t",String(nextIndex)); AppendTo(OUT,alphaLine,"\n");
  outText:=StringFile(OUT); outBytes:=Length(outText); outSha:=HexSHA256Padded(outText);
  checkpointPayload:=Concatenation("SEGMENT_ID\t",r.segmentId,"\tKEY\t24T",String(r.key),"\tLAST_CLASS_ID_V3\t",row.classId,"\tREPRESENTATIVE_FINGERPRINT\t",row.classId,"\tINDEX\t",String(index),"\tNEXT_INDEX\t",String(nextIndex),"\tCUM_UNITS\t",String(completedUnits),"\tCUM_RAW\t",String(rawPairs),"\tCUM_INVARIANT_ALPHA\t",String(invariantAlphaClasses),"\tCUM_BETA\t",String(betaComputations),"\tCUM_INVERSE\t",String(inversePairs),"\tCUM_INVERSE_ODD\t",String(inverseOddPairs),"\tCUM_ORBIT8\t",String(orbit8Pairs),"\tCUM_RELATOR\t",String(relatorPairs),"\tCUM_B3\t",String(b3Pairs),"\tCUM_GENERATE\t",String(generatingPairs),"\tCUM_CENTRALIZER_ORBITS\t",String(centralizerOrbits),"\tCUM_CANDIDATE_NUMERIC\t",String(candidateNumeric),"\tOUTPUT_FILE\t",OUT,"\tOUTPUT_PREFIX_BYTES\t",String(outBytes),"\tOUTPUT_PREFIX_SHA256\t",outSha,"\tPREVIOUS_CHECKPOINT_SHA256\t",checkpointSha,"\tSEGMENT_FILE_SHA256\t",EXPECTED_SEGMENT_FILE_SHA256);
  checkpointPayloadSha:=HexSHA256Padded(checkpointPayload); PrintTo(CHECKPOINT_TMP,"CERTIFICATE_CHECKPOINT\tDEG24_SPLIT_HEAVY_REPAIR_V3\n",checkpointPayload,"\tPAYLOAD_SHA256\t",checkpointPayloadSha,"\nDONE\n"); if not AtomicReplaceVerified(CHECKPOINT_TMP,CHECKPOINT_FILE) then Error("atomic checkpoint replace failed"); fi; checkpointSha:=HexSHA256Padded(StringFile(CHECKPOINT_FILE)); AppendTo(OUT,"CHECKPOINT_COMMITTED\tINDEX\t",index,"\tCLASS_ID_V3\t",row.classId,"\tCHECKPOINT_SHA256\t",checkpointSha,"\tOUTPUT_PREFIX_BYTES\t",outBytes,"\tOUTPUT_PREFIX_SHA256\t",outSha,"\n");
  if STOP_AFTER_INDEX<>fail and index=STOP_AFTER_INDEX then stoppedTest:=true; break; fi;
  if Runtime()-start>=INTERNAL_GUARD_MS then stoppedGuard:=true; break; fi;
 od;
fi;
if stoppedGuard or stoppedTest then AppendTo(OUT,"TOTAL_PARTIAL\tSTART_INDEX\t",START_INDEX,"\tLAST_COMPLETE_INDEX\t",lastIndex,"\tNEXT_INDEX\t",lastIndex+1,"\tCUM_UNITS\t",completedUnits,"\tCUM_RAW\t",rawPairs,"\tCANDIDATE_NUMERIC\t",candidateNumeric,"\tFINAL_CHECKPOINT_SHA256\t",checkpointSha,"\tGAP_MS\t",Runtime()-start,"\n"); if stoppedTest then AppendTo(OUT,"STOPPED_RECOVERY_SMOKE\n"); else AppendTo(OUT,"STOPPED_GUARD\n"); fi;
else
 if completedUnits<>Length(records) or rawPairs<>r.rawPairs then Error("terminal segment coverage mismatch"); fi;
 AppendTo(OUT,"TOTAL\tCLASS_UNITS\t",completedUnits,"\tRAW_PAIRS\t",rawPairs,"\tINVARIANT_ALPHA_CLASSES\t",invariantAlphaClasses,"\tBETA_COMPUTATIONS\t",betaComputations,"\tINVERSE\t",inversePairs,"\tINVERSE_ODD\t",inverseOddPairs,"\tORBIT8\t",orbit8Pairs,"\tRELATOR\t",relatorPairs,"\tB3\t",b3Pairs,"\tGENERATE\t",generatingPairs,"\tCENTRALIZER_ORBITS\t",centralizerOrbits,"\tCANDIDATE_NUMERIC\t",candidateNumeric,"\tFINAL_CHECKPOINT_SHA256\t",checkpointSha,"\tGAP_MS\t",Runtime()-start,"\nDONE\n");
fi;
Print("SEGMENT_EXIT\t",r.segmentId,"\tNEXT_INDEX\t",lastIndex+1,"\tTOTAL_CLASSES\t",Length(records),"\n"); QUIT_GAP(0);
