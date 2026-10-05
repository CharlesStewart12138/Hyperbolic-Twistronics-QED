# Export one authoritative Route-B Degree-24 C8 class manifest source.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(KEY_RECORD) or not IsBound(AUTHOR_SEED) or not IsBound(OUT) then Error("manifest wrapper variables missing"); fi;
if IsExistingFile(OUT) then Error("refusing to overwrite raw manifest source"); fi;
HexSHA256Padded:=function(value) local result;
 result:=HexSHA256(value); while Length(result)<64 do result:=Concatenation("0",result); od;
 if Length(result)<>64 then Error("SHA256 width"); fi; return LowercaseString(result);
end;
PermSerialization:=function(p) return JoinStringsWithSeparator(List([1..24],i->String(i^p)),","); end;
Reset(GlobalRandomSource,AUTHOR_SEED); Reset(GlobalMersenneTwister,AUTHOR_SEED);
rngLegacyBefore:=HexSHA256Padded(String(State(GlobalRandomSource)));
rngMtBefore:=HexSHA256Padded(String(State(GlobalMersenneTwister)));
r:=KEY_RECORD; G0:=TransitiveGroup(24,r.k); gens0:=GeneratorsOfGroup(G0); n:=Size(G0);
if n<>r.order then Error("group order mismatch"); fi;
transportG:=r.representation="pc_single" or r.representation="pc_transport";
if transportG then isoG:=IsomorphismPcGroup(G0); G:=Image(isoG); else G:=G0; fi;
maps:=GQuotients(G,CyclicGroup(2)); if Length(maps)<>r.parity then Error("parity-map mismatch"); fi;
A:=AutomorphismGroup(G); if Size(A)<>r.autOrder then Error("Aut order mismatch"); fi;
if r.route="pc" then
 if not IsSolvableGroup(A) then Error("pc route mismatch"); fi;
 isoA:=IsomorphismPcGroup(A); AP:=Image(isoA); allcc:=ConjugacyClasses(AP); pcgsAP:=Pcgs(AP);
elif r.route="native" then
 if IsSolvableGroup(A) then Error("native route mismatch"); fi;
 AP:=A; allcc:=ConjugacyClasses(A);
else Error("unknown route"); fi;
c8:=Filtered(allcc,c->Order(Representative(c))=8);
if Length(c8)<>r.classes then Error("C8 class count mismatch"); fi;
rngLegacyAfter:=HexSHA256Padded(String(State(GlobalRandomSource)));
rngMtAfter:=HexSHA256Padded(String(State(GlobalMersenneTwister)));
generatorSerialization:=JoinStringsWithSeparator(List(gens0,PermSerialization),";");
PrintTo(OUT,"MANIFEST_SOURCE_SCHEMA\tDEG24_KEY_CLASS_MANIFEST_SOURCE_V3\n",
 "KEY_ID\t24T",r.k,"\nGAP_VERSION\t",GAPInfo.Version,"\nAUTHOR_SEED\t",AUTHOR_SEED,"\n",
 "RANDOM_SOURCE_CONFIGURATION\tGLOBAL_RANDOM_SOURCE_AND_GLOBAL_MERSENNE_TWISTER_RESET\n",
 "GLOBAL_RANDOM_SOURCE_STATE_BEFORE_SHA256\t",rngLegacyBefore,"\n",
 "GLOBAL_MERSENNE_TWISTER_STATE_BEFORE_SHA256\t",rngMtBefore,"\n",
 "GLOBAL_RANDOM_SOURCE_STATE_AFTER_SHA256\t",rngLegacyAfter,"\n",
 "GLOBAL_MERSENNE_TWISTER_STATE_AFTER_SHA256\t",rngMtAfter,"\n",
 "GROUP_ORDER\t",n,"\nAUTOMORPHISM_GROUP_ORDER\t",Size(A),"\nPARITY_MAPS\t",Length(maps),"\n",
 "ROUTE\t",r.route,"\nREPRESENTATION\t",r.representation,"\nPC_ORDER\t",r.pcOrder,"\n",
 "ORDER8_CLASS_COUNT\t",Length(c8),"\nGENERATOR_COUNT\t",Length(gens0),"\n",
 "GENERATOR_SERIALIZATION\t",generatorSerialization,"\n",
 "REPRESENTATION_SCHEMA\tD24C8-FROZEN-ORIGINAL-GENERATOR-IMAGES-V3\n",
 "CLASS_COLUMNS\tORDINAL_DIAGNOSTIC\tREPRESENTATIVE_DISPLAY_DIAGNOSTIC\tPC_EXPONENTS_DIAGNOSTIC\tREPRESENTATIVE_SERIALIZATION\tCLASS_SIZE\tCENTRALIZER_SIZE\tORDER\tSTRUCTURAL_FILTERS\n");
for i in [1..Length(c8)] do
 ac:=c8[i]; rep:=Representative(ac);
 if r.route="pc" then alpha:=PreImagesRepresentative(isoA,rep); pcExp:=JoinStringsWithSeparator(List(ExponentsOfPcElement(pcgsAP,rep),String),",");
 else alpha:=rep; pcExp:="NA"; fi;
 if transportG then imgs:=List(gens0,g0->PreImagesRepresentative(isoG,Image(alpha,Image(isoG,g0))));
 else imgs:=List(gens0,g0->Image(alpha,g0)); fi;
 if ForAny(imgs,p->p=fail or not IsPerm(p)) then Error("representative image serialization failure"); fi;
 serialization:=JoinStringsWithSeparator(List(imgs,PermSerialization),";");
 AppendTo(OUT,"CLASS\t",i,"\t",String(rep),"\t",pcExp,"\t",serialization,"\t",
  Size(ac),"\t",Size(A)/Size(ac),"\t",Order(rep),
  "\tORDER_EQ_8;KEY_PARITY_MAPS_POSITIVE;GROUP_ORDER_WINDOW\n");
od;
AppendTo(OUT,"DONE\n");
Print("MANIFEST_SOURCE_PASS\t24T",r.k,"\tCLASSES\t",Length(c8),"\n"); QUIT_GAP(0);
