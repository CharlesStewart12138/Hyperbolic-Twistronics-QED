# Process-independent Route-B manifest verification by exact reconstruction,
# pairwise class distinction, class-count exhaustion, and size-multiset equality.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(MANIFEST_FILE) or not IsBound(VERIFY_SEED) or not IsBound(VERIFY_RUN_ID) or not IsBound(VERIFY_OUT) then Error("manifest verifier wrapper variables missing"); fi;
if IsExistingFile(VERIFY_OUT) then Error("refusing to overwrite replay certificate"); fi;
Read(MANIFEST_FILE);
PermSerialization:=function(p) return JoinStringsWithSeparator(List([1..24],i->String(i^p)),","); end;
Reset(GlobalRandomSource,VERIFY_SEED); Reset(GlobalMersenneTwister,VERIFY_SEED);
r:=D24C8_MANIFEST_META; G0:=TransitiveGroup(24,r.key); gens0:=GeneratorsOfGroup(G0);
if Size(G0)<>r.groupOrder then Error("group order mismatch"); fi;
if JoinStringsWithSeparator(List(gens0,PermSerialization),";")<>r.generatorSerialization then Error("fixed generator tuple mismatch"); fi;
transportG:=r.representation="pc_single" or r.representation="pc_transport";
if transportG then isoG:=IsomorphismPcGroup(G0); G:=Image(isoG); else G:=G0; fi;
maps:=GQuotients(G,CyclicGroup(2)); if Length(maps)<>r.parity then Error("parity mismatch"); fi;
A:=AutomorphismGroup(G); if Size(A)<>r.autOrder then Error("Aut order mismatch"); fi;
if r.route="pc" then isoA:=IsomorphismPcGroup(A); AP:=Image(isoA); allcc:=ConjugacyClasses(AP);
elif r.route="native" then AP:=A; allcc:=ConjugacyClasses(A);
else Error("unknown route"); fi;
c8:=Filtered(allcc,c->Order(Representative(c))=8);
freshCount:=Length(c8); freshClassSizes:=SortedList(List(c8,Size));
manifestCanon:=[]; manifestClassSizes:=[]; reconstructionFailures:=0; orderFailures:=0; metadataMismatches:=0;
for row in D24C8_MANIFEST_RECORDS do
 imgs0:=List(row.images,PermList); alpha0:=GroupHomomorphismByImages(G0,G0,gens0,imgs0);
 if alpha0=fail or not IsBijective(alpha0) then reconstructionFailures:=reconstructionFailures+1;
 else
  if Order(alpha0)<>8 or row.order<>8 then orderFailures:=orderFailures+1; fi;
  if transportG then
   gensG:=GeneratorsOfGroup(G); preG:=List(gensG,g->PreImagesRepresentative(isoG,g));
   imgsG:=List(preG,x0->Image(isoG,Image(alpha0,x0)));
   alphaG:=GroupHomomorphismByImages(G,G,gensG,imgsG);
  else alphaG:=alpha0; fi;
  if alphaG=fail or not IsBijective(alphaG) or not (alphaG in A) then reconstructionFailures:=reconstructionFailures+1;
  else
   if r.route="pc" then ap:=Image(isoA,alphaG); else ap:=alphaG; fi;
   cc:=ConjugacyClass(AP,ap); Add(manifestCanon,CanonicalRepresentativeOfExternalSet(cc)); Add(manifestClassSizes,Size(cc));
   if Size(cc)<>row.classSize or Size(AP)/Size(cc)<>row.centralizerSize then metadataMismatches:=metadataMismatches+1; fi;
  fi;
 fi;
od;
manifestCanonSet:=Set(manifestCanon); manifestClassSizes:=SortedList(manifestClassSizes);
duplicates:=Length(manifestCanon)-Length(manifestCanonSet);
missing:=Maximum(0,freshCount-Length(manifestCanonSet));
classSizeMultisetMatch:=freshClassSizes=manifestClassSizes;
status:="FAIL";
if freshCount=r.classCount and Length(D24C8_MANIFEST_RECORDS)=r.classCount and reconstructionFailures=0 and orderFailures=0 and metadataMismatches=0 and duplicates=0 and missing=0 and classSizeMultisetMatch then status:="PASS"; fi;
PrintTo(VERIFY_OUT,"CERTIFICATE\tDEG24_KEY_MANIFEST_INDEPENDENT_REPLAY_V3\n",
 "VERIFY_RUN_ID\t",VERIFY_RUN_ID,"\nVERIFY_SEED\t",VERIFY_SEED,"\nGAP_VERSION\t",GAPInfo.Version,"\nKEY_ID\t24T",r.key,"\n",
 "ROUTE\t",r.route,"\nREPRESENTATION\t",r.representation,"\nMANIFEST_CLASS_COUNT\t",r.classCount,"\nFRESH_CLASS_COUNT\t",freshCount,"\n",
 "RECONSTRUCTION_FAILURES\t",reconstructionFailures,"\nORDER_FAILURES\t",orderFailures,"\nCLASS_METADATA_MISMATCHES\t",metadataMismatches,"\n",
 "DUPLICATE_MATCHES\t",duplicates,"\nMISSING_MATCHES\t",missing,"\nCLASS_SIZE_MULTISET_MATCH\t",classSizeMultisetMatch,"\n",
 "PROOF\tEvery reconstructed representative has order 8; pairwise distinct conjugacy classes plus equality with the independently enumerated class count exhausts the target class set.\n",
 "STATUS\t",status,"\nDONE\n");
Print("KEY_MANIFEST_REPLAY_",status,"\t24T",r.key,"\tCLASSES\t",freshCount,"\n"); if status<>"PASS" then QUIT_GAP(1); fi; QUIT_GAP(0);
