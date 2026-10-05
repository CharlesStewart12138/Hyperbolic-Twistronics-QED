# Optimized independent replay of the frozen 24T13493 Route-B manifest.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(VERIFY_RUN_ID) or not IsBound(VERIFY_SEED) or not IsBound(VERIFY_OUT) then Error("verifier wrapper variables missing"); fi;
if IsExistingFile(VERIFY_OUT) then Error("refusing to overwrite verifier output"); fi;
Read("/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/DEG24_KEY_24T13493_CLASS_MANIFEST_V3.g");
PermSerialization:=function(p) return JoinStringsWithSeparator(List([1..24],i->String(i^p)),","); end;
Reset(GlobalRandomSource,VERIFY_SEED); Reset(GlobalMersenneTwister,VERIFY_SEED);
k:=D24C8_MANIFEST_META.key; G0:=TransitiveGroup(24,k); gens0:=GeneratorsOfGroup(G0);
generatorSerialization:=JoinStringsWithSeparator(List(gens0,PermSerialization),";");
if generatorSerialization<>D24C8_MANIFEST_META.generatorSerialization then Error("fixed generator tuple mismatch"); fi;
isoG:=IsomorphismPcGroup(G0); G:=Image(isoG); gensG:=GeneratorsOfGroup(G);
A:=AutomorphismGroup(G); isoA:=IsomorphismPcGroup(A); AP:=Image(isoA);
c8:=Filtered(ConjugacyClasses(AP),c->Order(Representative(c))=8);
if Length(c8)<>D24C8_MANIFEST_META.classCount then Error("fresh class count mismatch"); fi;
actualCanonByOrdinal:=List(c8,CanonicalRepresentativeOfExternalSet);
actualCanonSet:=Set(actualCanonByOrdinal);
if Length(actualCanonSet)<>Length(c8) then Error("fresh canonical representative collision"); fi;
manifestCanon:=[]; classSizeMismatch:=0; reconstructionFailure:=0; membershipFailure:=0;
ordinalChanges:=0; ordinal844MappedPosition:=fail;
for row in D24C8_MANIFEST_RECORDS do
 imgs0:=List(row.images,PermList); alpha0:=GroupHomomorphismByImages(G0,G0,gens0,imgs0);
 if alpha0=fail or not IsBijective(alpha0) or Order(alpha0)<>row.order then reconstructionFailure:=reconstructionFailure+1;
 else
  preG:=List(gensG,g->PreImagesRepresentative(isoG,g));
  imgsG:=List(preG,x0->Image(isoG,Image(alpha0,x0)));
  alphaG:=GroupHomomorphismByImages(G,G,gensG,imgsG);
  if alphaG=fail or not IsBijective(alphaG) or not (alphaG in A) then reconstructionFailure:=reconstructionFailure+1;
  else
   ap:=Image(isoA,alphaG); cc:=ConjugacyClass(AP,ap); canon:=CanonicalRepresentativeOfExternalSet(cc);
   Add(manifestCanon,canon);
   if Size(cc)<>row.classSize or Size(AP)/Size(cc)<>row.centralizerSize then classSizeMismatch:=classSizeMismatch+1; fi;
   freshOrdinal:=Position(actualCanonByOrdinal,canon);
   if freshOrdinal=fail then membershipFailure:=membershipFailure+1;
   elif freshOrdinal<>row.sourceOrdinalDiagnostic then ordinalChanges:=ordinalChanges+1; fi;
   if row.sourceOrdinalDiagnostic=844 then ordinal844MappedPosition:=freshOrdinal; fi;
  fi;
 fi;
od;
manifestCanonSet:=Set(manifestCanon); duplicateMatches:=Length(manifestCanon)-Length(manifestCanonSet);
missingMatches:=Length(Difference(actualCanonSet,manifestCanonSet)); extraMatches:=Length(Difference(manifestCanonSet,actualCanonSet));
status:="FAIL";
if reconstructionFailure=0 and membershipFailure=0 and classSizeMismatch=0 and duplicateMatches=0 and missingMatches=0 and extraMatches=0 and Length(manifestCanonSet)=Length(actualCanonSet) then status:="PASS"; fi;
PrintTo(VERIFY_OUT,"CERTIFICATE\tDEG24_SHARD208_MANIFEST_INDEPENDENT_REPLAY_V3\n",
 "VERIFY_RUN_ID\t",VERIFY_RUN_ID,"\nVERIFY_SEED\t",VERIFY_SEED,"\nGAP_VERSION\t",GAPInfo.Version,"\nKEY_ID\t24T",k,"\n",
 "MANIFEST_CLASS_COUNT\t",Length(D24C8_MANIFEST_RECORDS),"\nFRESH_CLASS_COUNT\t",Length(c8),"\n",
 "RECONSTRUCTION_FAILURES\t",reconstructionFailure,"\nMEMBERSHIP_FAILURES\t",membershipFailure,"\n",
 "CLASS_METADATA_MISMATCHES\t",classSizeMismatch,"\nDUPLICATE_MATCHES\t",duplicateMatches,"\n",
 "MISSING_MATCHES\t",missingMatches,"\nEXTRA_MATCHES\t",extraMatches,"\nORDINAL_CHANGES\t",ordinalChanges,"\n",
 "AUTHORITATIVE_SOURCE_ORDINAL844_FRESH_POSITION\t",ordinal844MappedPosition,"\nSTATUS\t",status,"\nDONE\n");
Print("MANIFEST_REPLAY_",status,"\t",VERIFY_RUN_ID,"\tORDINAL_CHANGES\t",ordinalChanges,"\n");
if status<>"PASS" then QUIT_GAP(1); fi; QUIT_GAP(0);
