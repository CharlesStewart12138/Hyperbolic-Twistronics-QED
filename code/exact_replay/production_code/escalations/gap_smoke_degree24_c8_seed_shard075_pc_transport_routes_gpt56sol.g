SizeScreen([1000000,1000000]);;
SetInfoLevel(InfoWarning,0);;
LoadPackage("transgrp");;

# Exact pc/pc_transport reconstruction for sealed profile key 24T11365.
G0:=TransitiveGroup(24,11365);;
if Size(G0)<>12288 then Error("24T11365 original order"); fi;
maps0:=GQuotients(G0,CyclicGroup(2));;
isoG:=IsomorphismPcGroup(G0);; P:=Image(isoG);;
mapsP:=GQuotients(P,CyclicGroup(2));;
if Size(P)<>12288 or Length(maps0)<>3 or Length(mapsP)<>3 then Error("24T11365 group transport"); fi;
A:=AutomorphismGroup(P);;
if Size(A)<>393216 then Error("24T11365 Aut order"); fi;
isoA:=IsomorphismPcGroup(A);; AP:=Image(isoA);;
cc:=ConjugacyClasses(AP);; c8:=Filtered(cc,c->Order(Representative(c))=8);;
if Length(c8)<>76 or Size(P)*Length(c8)<>933888 then Error("24T11365 class/raw identity"); fi;
alpha:=PreImagesRepresentative(isoA,Representative(c8[1]));;
if alpha=fail or not alpha in A or Order(alpha)<>8 then Error("24T11365 alpha lift"); fi;
x:=GeneratorsOfGroup(P)[1];; sx:=List([0..7],j->Image(alpha^j,x));;
ox:=List(sx,y->PreImagesRepresentative(isoG,y));;
if ForAny(ox,y->y=fail or not IsPerm(y) or not (y in G0)) or not ForAll([1..8],j->Image(isoG,ox[j])=sx[j]) then Error("24T11365 candidate pullback"); fi;

# Exact native/pc_transport reconstruction for sealed profile key 24T11383.
H0:=TransitiveGroup(24,11383);;
if Size(H0)<>12288 then Error("24T11383 original order"); fi;
hmaps0:=GQuotients(H0,CyclicGroup(2));;
isoH:=IsomorphismPcGroup(H0);; Q:=Image(isoH);;
hmapsQ:=GQuotients(Q,CyclicGroup(2));;
if Size(Q)<>12288 or Length(hmaps0)<>7 or Length(hmapsQ)<>7 then Error("24T11383 group transport"); fi;
B:=AutomorphismGroup(Q);;
if Size(B)<>990904320 then Error("24T11383 Aut order"); fi;
hcc:=ConjugacyClasses(B);; hc8:=Filtered(hcc,c->Order(Representative(c))=8);;
if Length(hc8)<>56 or Size(Q)*Length(hc8)<>688128 then Error("24T11383 class/raw identity"); fi;
beta:=Representative(hc8[1]);; y:=GeneratorsOfGroup(Q)[1];;
sy:=List([0..7],j->Image(beta^j,y));; oy:=List(sy,z->PreImagesRepresentative(isoH,z));;
if ForAny(oy,z->z=fail or not IsPerm(z) or not (z in H0)) or not ForAll([1..8],j->Image(isoH,oy[j])=sy[j]) then Error("24T11383 candidate pullback"); fi;

Print("SHARD075_PC_TRANSPORT_ROUTES_SEMANTIC_PASS\tPC_KEY\t24T11365\tPC_CLASSES\t",Length(c8),
 "\tPC_RAW\t",Size(P)*Length(c8),"\tNATIVE_KEY\t24T11383\tNATIVE_CLASSES\t",Length(hc8),
 "\tNATIVE_RAW\t",Size(Q)*Length(hc8),"\n");
QUIT_GAP(0);
