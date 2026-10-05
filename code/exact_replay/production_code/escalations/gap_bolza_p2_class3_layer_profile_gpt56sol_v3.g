# Corrected exact F_2[C_8]-module certificate for L3=P3/P4.
# All group-map powers are explicit iterations; MatrixObj identity is tested
# with IsOne, not representation-sensitive equality.
SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_P2_CLASS3_LAYER_PROFILE_GPT56SOL_V3.txt";
Check:=function(label,c)AppendTo(OUT,"CHECK\t",label,"\t",c,"\n");if c<>true then Error(Concatenation("check failed: ",label));fi;end;
IterImage:=function(h,x,n)local i,y;y:=x;for i in [1..n]do y:=Image(h,y);od;return y;end;
VecTimesRows:=function(v,m)local i,j,o;o:=[];for j in [1..Length(v)]do Add(o,Sum([1..Length(v)],i->v[i]*m[i][j]) mod 2);od;return o;end;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-LAYER-V3\n",
 "SUPERSEDES\tGAP_BOLZA_P2_CLASS3_LAYER_PROFILE_GPT56SOL_SUPERSEDED_INVALID_MAPPING_POWER.txt\n",
 "CORRECTION\texplicit Image iteration; integer coordinates coerced entrywise to GF(2); MatrixObj identity via IsOne; full-basis action cross-check\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "SCOPE\texact phi8-module structure on L3=P3/P4 of the universal exponent-2 class-3 quotient\n");
F:=FreeGroup("a1","b1","a2","b2");relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[relF];sg:=GeneratorsOfGroup(SG);
phiWords:=[sg[2]^-1,sg[3]^-1*sg[2]*sg[1],sg[3]^-1*sg[2]*sg[1]*sg[2]^-1*sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]*sg[2]*sg[1]^-1*sg[2]^-1*sg[3]];
qs:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);epi:=EpimorphismQuotientSystem(qs);U3:=Image(epi);ug:=List(sg,x->Image(epi,x));
alpha:=GroupHomomorphismByImages(U3,U3,ug,List(phiWords,x->Image(epi,x)));pc:=Pcgs(U3);layerBasis:=pc{[14..38]};layer:=Subgroup(U3,layerBasis);
rows:=List(layerBasis,x->ExponentsOfPcElement(pc,Image(alpha,x)){[14..38]});fieldRows:=List(rows,row->List(row,z->z*One(GF(2))));mat:=Matrix(GF(2),fieldRows);oneMat:=One(mat);nil:=mat-oneMat;dualNil:=TransposedMat(nil);
Check("pquotient_ranks_4_9_25",RanksOfDescendingSeries(qs)=[4,9,25]);
Check("u3_order_2pow38",Size(U3)=2^38);Check("pcgs_length_38",Length(pc)=38);
Check("layer_order_2pow25",Size(layer)=2^25);Check("layer_central",IsSubgroup(Center(U3),layer));Check("layer_elementary_abelian",IsElementaryAbelian(layer));
Check("u3_mod_layer_order_8192",Size(U3)/Size(layer)=8192);Check("layer_phi_invariant",ForAll(layerBasis,x->Image(alpha,x) in layer));
Check("alpha_homomorphism",IsGroupHomomorphism(alpha));Check("alpha_bijective",IsBijective(alpha));
Check("phi_iterate8_identity_on_generators",ForAll(ug,x->IterImage(alpha,x,8)=x));
for k in [1..7]do Check(Concatenation("phi_iterate_",String(k),"_nonidentity"),ForAny(ug,x->IterImage(alpha,x,k)<>x));od;
Check("source_field_rows_are_GF2",ForAll(fieldRows,row->ForAll(row,IsFFE)));Check("matrix_entries_are_GF2",ForAll(Flat(mat),IsFFE));Check("action_matrix_rank25",RankMat(mat)=25);Check("action_matrix_power8_identity",IsOne(mat^8));
Check("action_nilpotent_power4_zero",IsZero(nil^4));
consistent:=true;
for i in [1..25]do expected:=List([1..25],j->0);expected[i]:=1;
 for k in [1..8]do expected:=VecTimesRows(expected,rows);actual:=ExponentsOfPcElement(pc,IterImage(alpha,layerBasis[i],k)){[14..38]};if expected<>actual then consistent:=false;fi;od;
od;
Check("all_25_basis_vectors_steps_1_to_8_match_group_action",consistent);
v:=ExponentsOfPcElement(pc,ug[1]^4){[14..38]};Check("g0_power4_in_layer",ug[1]^4 in layer);Check("g0_power4_nontrivial",not IsOne(ug[1]^4));
AppendTo(OUT,"PQUOTIENT_RANKS\t",RanksOfDescendingSeries(qs),"\nU3_ORDER\t",Size(U3),"\nLAYER_ORDER\t",Size(layer),"\n",
 "ACTION_MATRIX_ROWS\t",rows,"\nG0_POWER4_COORDS\t",v,"\n");
for k in [1..8]do AppendTo(OUT,"DUAL_NILPOTENT_KERNEL\tPOWER\t",k,"\tDIM\t",Length(NullspaceMat(dualNil^k)),"\n");od;
AppendTo(OUT,"RESULT\tPASS\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
