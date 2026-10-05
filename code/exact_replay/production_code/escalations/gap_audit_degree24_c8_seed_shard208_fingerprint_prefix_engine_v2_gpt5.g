# Exact class-set seam audit for 24T13493.  Fingerprints are minimized over
# every element in each Aut(G)-conjugacy class after transport to the fixed
# original permutation representation, hence are independent of pc labels.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(AUDIT_MODE) or not IsBound(OUT) then Error("audit wrapper variables missing"); fi;
HexSHA256Padded:=function(value) local result;
 result:=HexSHA256(value);
 while Length(result)<64 do result:=Concatenation("0",result); od;
 if Length(result)<>64 then Error("SHA256 width"); fi;
 return LowercaseString(result);
end;
BuildC8:=function(k)
 local G0,isoG,G,A,isoA,AP,allcc,c8;
 G0:=TransitiveGroup(24,k); isoG:=IsomorphismPcGroup(G0); G:=Image(isoG);
 A:=AutomorphismGroup(G); isoA:=IsomorphismPcGroup(A); AP:=Image(isoA);
 allcc:=ConjugacyClasses(AP); c8:=Filtered(allcc,c->Order(Representative(c))=8);
 return rec(G0:=G0,isoG:=isoG,G:=G,A:=A,isoA:=isoA,AP:=AP,c8:=c8);
end;
ActionEncoding:=function(ctx,apElement)
 local a,gens0,g0,pcg,imgPc,img0,parts;
 a:=PreImagesRepresentative(ctx.isoA,apElement);
 gens0:=GeneratorsOfGroup(ctx.G0); parts:=[];
 for g0 in gens0 do
  pcg:=Image(ctx.isoG,g0); imgPc:=Image(a,pcg);
  img0:=PreImagesRepresentative(ctx.isoG,imgPc);
  Add(parts,String(ListPerm(img0,24)));
 od;
 return JoinStringsWithSeparator(parts,"|");
end;
ClassFingerprint:=function(ctx,cc)
 local best,s,elt;
 best:=fail;
 for elt in Elements(cc) do
  s:=ActionEncoding(ctx,elt);
  if best=fail or s<best then best:=s; fi;
 od;
 if best=fail then Error("empty conjugacy class"); fi;
 return HexSHA256Padded(best);
end;
if AUDIT_MODE="PREFIX_HISTORY" then
 prior:=BuildC8(13489); if Length(prior.c8)<>1088 then Error("24T13489 class count"); fi;
 prior:=BuildC8(13490); if Length(prior.c8)<>142 then Error("24T13490 class count"); fi;
elif AUDIT_MODE<>"FRESH" then Error("unknown AUDIT_MODE"); fi;
ctx:=BuildC8(13493); c8:=ctx.c8;
if Length(c8)<>1976 then Error("24T13493 order-eight class count"); fi;
auditLimit:=844;
PrintTo(OUT,"CERTIFICATE_CLASS_FINGERPRINT_PREFIX\t24T13493\tMODE\t",AUDIT_MODE,
 "\tFULL_CLASSES\t",Length(c8),"\tAUDITED_PREFIX\t",auditLimit,"\n");
for i in [1..auditLimit] do
 fp:=ClassFingerprint(ctx,c8[i]);
 AppendTo(OUT,"CLASS\t",i,"\tSIZE\t",Size(c8[i]),"\tFINGERPRINT\t",fp,"\n");
od;
AppendTo(OUT,"DONE\n");
Print("SHARD208_FINGERPRINT_PREFIX_AUDIT_",AUDIT_MODE,"_PASS\n");
QUIT_GAP(0);
