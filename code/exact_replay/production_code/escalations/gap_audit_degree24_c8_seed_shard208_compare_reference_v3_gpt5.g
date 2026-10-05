# Map both process-history traces into one fixed Aut(G) pc representation.
# Exact pc exponent vectors of canonical conjugacy-class representatives are
# used internally (not just hashes), so set equality is collision-free.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
Read("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD208_TRACE_PREFIX_HISTORY_V3_GPT5.g");
oldTrace:=ShallowCopy(TRACE); Unbind(TRACE);
Read("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD208_TRACE_FRESH_V3_GPT5.g");
freshTrace:=ShallowCopy(TRACE); Unbind(TRACE);
if Length(oldTrace)<>844 or Length(freshTrace)<>844 then Error("trace length"); fi;
G0:=TransitiveGroup(24,13493); isoG:=IsomorphismPcGroup(G0); G:=Image(isoG);
A:=AutomorphismGroup(G); isoA:=IsomorphismPcGroup(A); AP:=Image(isoA);
c8:=Filtered(ConjugacyClasses(AP),c->Order(Representative(c))=8);
if Length(c8)<>1976 then Error("reference class count"); fi;
gens0:=GeneratorsOfGroup(G0); gensG:=List(gens0,g->Image(isoG,g)); pcgsAP:=Pcgs(AP);
RefClassCode:=function(r)
 local imgs0,a0,imgsG,aG,ap,cc,can;
 imgs0:=List(r.images,PermList);
 a0:=GroupHomomorphismByImages(G0,G0,gens0,imgs0);
 if a0=fail or not IsBijective(a0) then Error("invalid original action"); fi;
 imgsG:=List(imgs0,x->Image(isoG,x));
 aG:=GroupHomomorphismByImages(G,G,gensG,imgsG);
 if aG=fail or not IsBijective(aG) or not (aG in A) then Error("transport not in reference Aut(G)"); fi;
 ap:=Image(isoA,aG);
 if Order(ap)<>8 then Error("transported order mismatch"); fi;
 cc:=ConjugacyClass(AP,ap);
 if Size(cc)<>r.size then Error("class size mismatch"); fi;
 can:=CanonicalRepresentativeOfExternalSet(cc);
 return Immutable(ExponentsOfPcElement(pcgsAP,can));
end;
oldCodes:=List(oldTrace,RefClassCode); freshCodes:=List(freshTrace,RefClassCode);
if oldTrace[844].size<>192 then Error("old alpha844 anchor"); fi;
if freshTrace[844].size<>48 then Error("fresh alpha844 anchor"); fi;
oldPrefix:=Set(oldCodes{[1..843]}); freshPrefix:=Set(freshCodes{[1..843]});
intersection:=Intersection(oldPrefix,freshPrefix);
oldOnly:=Difference(oldPrefix,freshPrefix); freshOnly:=Difference(freshPrefix,oldPrefix);
PrintTo("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD208_BOUNDARY_REFERENCE_AUDIT_V3_GPT5.txt",
 "CERTIFICATE\tPF-GRP-001-C8-DEGREE24-SEED-SHARD208-BOUNDARY-REFERENCE-V3\n",
 "REFERENCE_ORDER8_CLASSES\t",Length(c8),"\n",
 "OLD_PREFIX_UNIQUE\t",Length(oldPrefix),"\n",
 "FRESH_PREFIX_UNIQUE\t",Length(freshPrefix),"\n",
 "PREFIX_INTERSECTION\t",Length(intersection),"\n",
 "OLD_ONLY\t",Length(oldOnly),"\n",
 "FRESH_ONLY\t",Length(freshOnly),"\n",
 "OLD_UNCOMMITTED_ALPHA844_CLASS_SIZE\t",oldTrace[844].size,"\n",
 "FRESH_COMMITTED_ALPHA844_CLASS_SIZE\t",freshTrace[844].size,"\n",
 "STATUS\t",(Length(oldOnly)=0 and Length(freshOnly)=0) and "PASS_ZERO_OVERLAP_ZERO_OMISSION" or "FAIL_SPLICE_SET_MISMATCH","\nDONE\n");
if Length(oldPrefix)<>843 or Length(freshPrefix)<>843 or Length(oldOnly)<>0 or Length(freshOnly)<>0 then Error("split fingerprint set mismatch"); fi;
Print("SHARD208_BOUNDARY_REFERENCE_AUDIT_V3_PASS\n");
QUIT_GAP(0);
