# Low-memory exact Route-B replay for a native automorphism-group key.
# V5 recovery: require the frozen manifest's exact legacy_original_native representation.
# Class size is used only as a prefilter; identity is proved by exact class membership.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(MANIFEST_FILE) or not IsBound(VERIFY_SEED) or not IsBound(VERIFY_RUN_ID) or not IsBound(VERIFY_OUT) then Error("manifest verifier wrapper variables missing"); fi;
if IsExistingFile(VERIFY_OUT) then Error("refusing to overwrite replay certificate"); fi;
Read(MANIFEST_FILE);
PermSerialization:=function(p) return JoinStringsWithSeparator(List([1..24],i->String(i^p)),","); end;
Reset(GlobalRandomSource,VERIFY_SEED); Reset(GlobalMersenneTwister,VERIFY_SEED);
r:=D24C8_MANIFEST_META;
if r.route<>"native" or r.representation<>"legacy_original_native" then Error("native verifier route mismatch"); fi;
G0:=TransitiveGroup(24,r.key); gens0:=GeneratorsOfGroup(G0);
if Size(G0)<>r.groupOrder then Error("group order mismatch"); fi;
if JoinStringsWithSeparator(List(gens0,PermSerialization),";")<>r.generatorSerialization then Error("fixed generator tuple mismatch"); fi;
maps:=GQuotients(G0,CyclicGroup(2)); if Length(maps)<>r.parity then Error("parity mismatch"); fi;
A:=AutomorphismGroup(G0); if Size(A)<>r.autOrder then Error("Aut order mismatch"); fi;
c8:=Filtered(ConjugacyClasses(A),c->Order(Representative(c))=8);
freshCount:=Length(c8); freshClassSizes:=List(c8,Size);
matchedPositions:=[]; reconstructionFailures:=0; orderFailures:=0; metadataMismatches:=0; ambiguousMatches:=0;
for row in D24C8_MANIFEST_RECORDS do
 imgs0:=List(row.images,PermList); alpha0:=GroupHomomorphismByImages(G0,G0,gens0,imgs0);
 if alpha0=fail or not IsBijective(alpha0) or not (alpha0 in A) then reconstructionFailures:=reconstructionFailures+1;
 else
  if Order(alpha0)<>8 or row.order<>8 then orderFailures:=orderFailures+1; fi;
  candidatePositions:=Filtered([1..freshCount],i->freshClassSizes[i]=row.classSize);
  exactPositions:=Filtered(candidatePositions,i->alpha0 in c8[i]);
  if Length(exactPositions)<>1 then ambiguousMatches:=ambiguousMatches+1;
  else
   pos:=exactPositions[1]; Add(matchedPositions,pos);
   if Size(c8[pos])<>row.classSize or Size(A)/Size(c8[pos])<>row.centralizerSize then metadataMismatches:=metadataMismatches+1; fi;
  fi;
 fi;
od;
duplicates:=Length(matchedPositions)-Length(Set(matchedPositions));
missing:=freshCount-Length(Set(matchedPositions));
classSizeMultisetMatch:=SortedList(freshClassSizes)=SortedList(List(D24C8_MANIFEST_RECORDS,row->row.classSize));
status:="FAIL";
if freshCount=r.classCount and Length(D24C8_MANIFEST_RECORDS)=r.classCount and reconstructionFailures=0 and orderFailures=0 and metadataMismatches=0 and ambiguousMatches=0 and duplicates=0 and missing=0 and classSizeMultisetMatch then status:="PASS"; fi;
PrintTo(VERIFY_OUT,"CERTIFICATE\tDEG24_KEY_MANIFEST_INDEPENDENT_REPLAY_V3\n",
 "VERIFY_RUN_ID\t",VERIFY_RUN_ID,"\nVERIFY_SEED\t",VERIFY_SEED,"\nGAP_VERSION\t",GAPInfo.Version,"\nKEY_ID\t24T",r.key,"\n",
 "ROUTE\t",r.route,"\nREPRESENTATION\t",r.representation,"\nMANIFEST_CLASS_COUNT\t",r.classCount,"\nFRESH_CLASS_COUNT\t",freshCount,"\n",
 "RECONSTRUCTION_FAILURES\t",reconstructionFailures,"\nORDER_FAILURES\t",orderFailures,"\nCLASS_METADATA_MISMATCHES\t",metadataMismatches,"\n",
 "AMBIGUOUS_EXACT_MATCHES\t",ambiguousMatches,"\nDUPLICATE_MATCHES\t",duplicates,"\nMISSING_MATCHES\t",missing,"\nCLASS_SIZE_MULTISET_MATCH\t",classSizeMultisetMatch,"\n",
 "PROOF\tEvery frozen representative is reconstructed in Aut(G), matched to exactly one freshly enumerated conjugacy class by exact class membership, and the resulting positions exhaust the fresh class set exactly once; class size is only a prefilter.\n",
 "STATUS\t",status,"\nDONE\n");
Print("KEY_MANIFEST_REPLAY_",status,"\t24T",r.key,"\tCLASSES\t",freshCount,"\n"); if status<>"PASS" then QUIT_GAP(1); fi; QUIT_GAP(0);
