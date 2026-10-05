# Degree-24 V3 forensic regression for 24T13493.
# Ordinals are diagnostics only. Exact automorphisms are serialized by their
# images on the fixed ordered generators of the original permutation group.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(RUN_ID) or not IsBound(SEED) or not IsBound(OUT) then
 Error("RUN_ID, SEED, and OUT are required");
fi;
if IsExistingFile(OUT) then Error("refusing to overwrite forensic output"); fi;

HexSHA256Padded:=function(value) local result;
 result:=HexSHA256(value);
 while Length(result)<64 do result:=Concatenation("0",result); od;
 if Length(result)<>64 then Error("SHA256 width"); fi;
 return LowercaseString(result);
end;
PermSerialization:=function(p)
 return JoinStringsWithSeparator(List([1..24],i->String(i^p)),",");
end;
AutomorphismSerialization:=function(alpha,isoG,gens0)
 local imgs;
 imgs:=List(gens0,g0->PreImagesRepresentative(isoG,Image(alpha,Image(isoG,g0))));
 if ForAny(imgs,p->p=fail or not IsPerm(p)) then Error("image serialization failure"); fi;
 return JoinStringsWithSeparator(List(imgs,PermSerialization),";");
end;

Reset(GlobalRandomSource,SEED);
Reset(GlobalMersenneTwister,SEED);
rngLegacyBefore:=HexSHA256Padded(String(State(GlobalRandomSource)));
rngMtBefore:=HexSHA256Padded(String(State(GlobalMersenneTwister)));

k:=13493; G0:=TransitiveGroup(24,k); gens0:=GeneratorsOfGroup(G0);
isoG:=IsomorphismPcGroup(G0); G:=Image(isoG);
A:=AutomorphismGroup(G); isoA:=IsomorphismPcGroup(A); AP:=Image(isoA);
allcc:=ConjugacyClasses(AP);
c8:=Filtered(allcc,c->Order(Representative(c))=8);
if Length(c8)<>1976 then Error("24T13493 C8 class count mismatch"); fi;
pcgsAP:=Pcgs(AP); autOrder:=Size(AP);
rngLegacyAfter:=HexSHA256Padded(String(State(GlobalRandomSource)));
rngMtAfter:=HexSHA256Padded(String(State(GlobalMersenneTwister)));

PrintTo(OUT,
 "FORENSIC_SCHEMA\tDEG24_SHARD208_24T13493_V3\n",
 "RUN_ID\t",RUN_ID,"\n",
 "KEY_ID\t24T",k,"\n",
 "GAP_VERSION\t",GAPInfo.Version,"\n",
 "RANDOM_SOURCE_CONFIGURATION\tGLOBAL_RANDOM_SOURCE_AND_GLOBAL_MERSENNE_TWISTER_RESET\n",
 "RANDOM_SEED\t",SEED,"\n",
 "GLOBAL_RANDOM_SOURCE_STATE_BEFORE_SHA256\t",rngLegacyBefore,"\n",
 "GLOBAL_MERSENNE_TWISTER_STATE_BEFORE_SHA256\t",rngMtBefore,"\n",
 "GLOBAL_RANDOM_SOURCE_STATE_AFTER_SHA256\t",rngLegacyAfter,"\n",
 "GLOBAL_MERSENNE_TWISTER_STATE_AFTER_SHA256\t",rngMtAfter,"\n",
 "GROUP_ORDER\t",Size(G0),"\n",
 "AUTOMORPHISM_GROUP_ORDER\t",autOrder,"\n",
 "ORDER8_CLASS_COUNT\t",Length(c8),"\n",
 "GENERATOR_COUNT\t",Length(gens0),"\n",
 "GENERATOR_SERIALIZATION\t",JoinStringsWithSeparator(List(gens0,PermSerialization),";"),"\n",
 "REPRESENTATION_SCHEMA\tD24C8-FROZEN-ORIGINAL-GENERATOR-IMAGES-V3\n",
 "CLASS_COLUMNS\tORDINAL\tREPRESENTATIVE_DISPLAY\tPC_EXPONENTS\tREPRESENTATIVE_SERIALIZATION\tCLASS_SIZE\tCENTRALIZER_SIZE\tORDER\tSTRUCTURAL_FILTER\n");

for i in [1..Length(c8)] do
 ac:=c8[i]; repAP:=Representative(ac); alpha:=PreImagesRepresentative(isoA,repAP);
 serialization:=AutomorphismSerialization(alpha,isoG,gens0);
 AppendTo(OUT,"CLASS\t",i,"\t",String(repAP),"\t",
  JoinStringsWithSeparator(List(ExponentsOfPcElement(pcgsAP,repAP),String),","),"\t",
  serialization,"\t",Size(ac),"\t",autOrder/Size(ac),"\t",Order(repAP),
  "\tORDER_EQ_8\n");
od;
AppendTo(OUT,"ORDINAL_844_CLASS_SIZE\t",Size(c8[844]),"\n",
 "ORDINAL_844_REPRESENTATIVE_SERIALIZATION_SHA256\t",
 HexSHA256Padded(AutomorphismSerialization(PreImagesRepresentative(isoA,Representative(c8[844])),isoG,gens0)),"\n",
 "DONE\n");
Print("FORENSIC_PASS\t",RUN_ID,"\tORDINAL844_SIZE\t",Size(c8[844]),"\n");
QUIT_GAP(0);
