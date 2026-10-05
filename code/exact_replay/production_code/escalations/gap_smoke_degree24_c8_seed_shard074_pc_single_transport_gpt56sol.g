LoadPackage("transgrp");;
G0:=TransitiveGroup(24,11363);;
if Size(G0)<>12288 then Error("24T11363 original order"); fi;
maps0:=GQuotients(G0,CyclicGroup(2));;
isoG:=IsomorphismPcGroup(G0);; P:=Image(isoG);;
if Size(P)<>12288 then Error("24T11363 pc transport order"); fi;
mapsP:=GQuotients(P,CyclicGroup(2));;
if Length(maps0)<>7 or Length(mapsP)<>7 then Error("24T11363 parity transport"); fi;
A:=AutomorphismGroup(P);;
if Size(A)<>754974720 or IsSolvableGroup(A) then Error("24T11363 native Aut route"); fi;
cc:=ConjugacyClasses(A);; c8:=Filtered(cc,c->Order(Representative(c))=8);;
if Length(c8)<>294 or Size(P)*Length(c8)<>3612672 then Error("24T11363 class/raw identity"); fi;
alpha:=Representative(c8[1]);; x:=GeneratorsOfGroup(P)[1];;
xs:=List([0..7],j->Image(alpha^j,x));;
ys:=List(xs,y->PreImagesRepresentative(isoG,y));;
if Length(ys)<>8 or not ForAll(ys,y->y in G0) then Error("24T11363 output transport"); fi;
Print("SHARD074_PC_SINGLE_TRANSPORT_SEMANTIC_PASS\tKEY\t24T11363\tORDER\t",Size(P),
 "\tPARITY_G\t",Length(maps0),"\tPARITY_P\t",Length(mapsP),"\tAUT_ORDER\t",Size(A),
 "\tORDER8_CLASSES\t",Length(c8),"\tRAW_PAIRS\t",Size(P)*Length(c8),"\n");
QUIT_GAP(0);
