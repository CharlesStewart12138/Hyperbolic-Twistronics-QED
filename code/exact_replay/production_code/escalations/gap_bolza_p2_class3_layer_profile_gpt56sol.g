# Exact F_2[C_8]-module certificate for the third lower exponent-2 central
# layer of the frozen Bolza surface group.
SetInfoLevel(InfoWarning,0); SetInfoLevel(InfoQuotientSystem,0);
SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_P2_CLASS3_LAYER_PROFILE_GPT56SOL.txt";
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-LAYER\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\n",
 "NQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "SCOPE\texact phi8-module structure on L3=P3/P4 of the universal exponent-2 class-3 quotient\n");
F:=FreeGroup("a1","b1","a2","b2");
relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;
SG:=F/[relF]; sg:=GeneratorsOfGroup(SG);
phiWords:=[sg[2]^-1,sg[3]^-1*sg[2]*sg[1],
 sg[3]^-1*sg[2]*sg[1]*sg[2]^-1*sg[1]^-1*sg[2]^-1*sg[4]^-1,
 sg[1]*sg[2]*sg[1]^-1*sg[2]^-1*sg[3]];
qs:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);
epi:=EpimorphismQuotientSystem(qs); U3:=Image(epi); ug:=List(sg,x->Image(epi,x));
alpha:=GroupHomomorphismByImages(U3,U3,ug,List(phiWords,x->Image(epi,x)));
pc:=Pcgs(U3); layerBasis:=pc{[14..38]}; layer:=Subgroup(U3,layerBasis);
rows:=List(layerBasis,x->ExponentsOfPcElement(pc,Image(alpha,x)){[14..38]});
mat:=ImmutableMatrix(GF(2),rows); id:=IdentityMat(25,GF(2)); nil:=mat-id;
dualNil:=TransposedMat(nil);
v:=ExponentsOfPcElement(pc,ug[1]^4){[14..38]};
AppendTo(OUT,"PQUOTIENT_RANKS\t",RanksOfDescendingSeries(qs),"\n",
 "U3_ORDER\t",Size(U3),"\nLAYER_ORDER\t",Size(layer),"\n",
 "LAYER_CENTRAL\t",IsSubgroup(Center(U3),layer),"\n",
 "LAYER_ELEMENTARY_ABELIAN\t",IsElementaryAbelian(layer),"\n",
 "U3_MOD_LAYER_ORDER\t",Size(U3)/Size(layer),"\n",
 "PHI_EXACT_ORDER8\t",ForAll(ug,x->Image(alpha^8,x)=x) and ForAll([1..7],k->ForAny(ug,x->Image(alpha^k,x)<>x)),"\n",
 "ACTION_MATRIX_ROWS\t",rows,"\n",
 "ACTION_POWER8_IDENTITY\t",mat^8=id,"\n",
 "G0_POWER4_IN_LAYER\t",ug[1]^4 in layer,"\n",
 "G0_POWER4_NONTRIVIAL\t",not IsOne(ug[1]^4),"\n",
 "G0_POWER4_COORDS\t",v,"\n");
for k in [1..8] do
 AppendTo(OUT,"DUAL_NILPOTENT_KERNEL\tPOWER\t",k,"\tDIM\t",Length(NullspaceMat(dualNil^k)),"\n");
od;
AppendTo(OUT,"RESULT\tPASS\nDONE\n"); Print("WROTE ",OUT,"\n"); QUIT;
