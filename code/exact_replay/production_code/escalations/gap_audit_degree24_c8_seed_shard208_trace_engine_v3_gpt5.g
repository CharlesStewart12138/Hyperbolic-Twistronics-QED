# Export representative actions for the two process histories at the shard208 seam.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
if GAPInfo.Version<>"4.12.1" then Error("GAP version mismatch"); fi;
if not IsBound(AUDIT_MODE) or not IsBound(OUT) then Error("audit wrapper variables missing"); fi;
BuildC8:=function(k)
 local G0,isoG,G,A,isoA,AP,allcc,c8;
 G0:=TransitiveGroup(24,k); isoG:=IsomorphismPcGroup(G0); G:=Image(isoG);
 A:=AutomorphismGroup(G); isoA:=IsomorphismPcGroup(A); AP:=Image(isoA);
 allcc:=ConjugacyClasses(AP); c8:=Filtered(allcc,c->Order(Representative(c))=8);
 return rec(G0:=G0,isoG:=isoG,G:=G,A:=A,isoA:=isoA,AP:=AP,c8:=c8);
end;
if AUDIT_MODE="PREFIX_HISTORY" then
 prior:=BuildC8(13489); if Length(prior.c8)<>1088 then Error("24T13489 class count"); fi;
 prior:=BuildC8(13490); if Length(prior.c8)<>142 then Error("24T13490 class count"); fi;
elif AUDIT_MODE<>"FRESH" then Error("unknown AUDIT_MODE"); fi;
ctx:=BuildC8(13493); c8:=ctx.c8;
if Length(c8)<>1976 then Error("24T13493 order-eight class count"); fi;
gens0:=GeneratorsOfGroup(ctx.G0);
PrintTo(OUT,"TRACE:=[\n");
for i in [1..844] do
 alpha:=PreImagesRepresentative(ctx.isoA,Representative(c8[i]));
 imgs:=List(gens0,g0->PreImagesRepresentative(ctx.isoG,Image(alpha,Image(ctx.isoG,g0))));
 AppendTo(OUT,"rec(i:=",i,",size:=",Size(c8[i]),",images:=[");
 for j in [1..Length(imgs)] do
  if j>1 then AppendTo(OUT,","); fi;
  AppendTo(OUT,String(ListPerm(imgs[j],24)));
 od;
 if i<844 then AppendTo(OUT,"]),\n"); else AppendTo(OUT,"])\n"); fi;
od;
AppendTo(OUT,"];\n");
Print("SHARD208_TRACE_",AUDIT_MODE,"_PASS\n");
QUIT_GAP(0);
