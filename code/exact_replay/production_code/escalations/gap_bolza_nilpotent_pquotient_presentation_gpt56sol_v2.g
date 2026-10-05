# Corrected frozen-presentation certificate.  V2 never uses mapping powers:
# every iterate of phi is explicit repeated Image(phi,-).
SetInfoLevel(InfoWarning,0);SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_NILPOTENT_PQUOTIENT_PRESENTATION_GPT56SOL_V2.txt";
Check:=function(label,c)AppendTo(OUT,"CHECK\t",label,"\t",c,"\n");if c<>true then Error(Concatenation("check failed: ",label));fi;end;
IterImage:=function(h,x,n)local i,y;y:=x;for i in [1..n]do y:=Image(h,y);od;return y;end;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-NILPOTENT-PQUOTIENT-PRESENTATION-V2\n",
 "SUPERSEDES\tGAP_BOLZA_NILPOTENT_PQUOTIENT_PRESENTATION_GPT56SOL_SUPERSEDED_INVALID_MAPPING_POWER.txt\n",
 "CORRECTION\texplicit repeated Image iteration replaces invalid general-mapping exponent syntax\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "WORD_CONVENTION\tleft-to-right group multiplication as written\n",
 "STANDARD_PRESENTATION\t<a1,b1,a2,b2 | a1*b1*a1^-1*b1^-1*a2*b2*a2^-1*b2^-1>\n",
 "PARITY\ta1,b1,a2,b2 all map to the nonidentity element of C2\n",
 "SCOPE\tpresentation/map/filter interface only; no finite-quotient exhaustiveness asserted\n");
F:=FreeGroup("a1","b1","a2","b2");fa1:=F.1;;fb1:=F.2;;fa2:=F.3;;fb2:=F.4;;
relF:=fa1*fb1*fa1^-1*fb1^-1*fa2*fb2*fa2^-1*fb2^-1;SG:=F/[relF];gg:=GeneratorsOfGroup(SG);
a1:=gg[1];;b1:=gg[2];;a2:=gg[3];;b2:=gg[4];;
phiImages:=[b1^-1,a2^-1*b1*a1,a2^-1*b1*a1*b1^-1*a1^-1*b1^-1*b2^-1,a1*b1*a1^-1*b1^-1*a2];
phiInverseImages:=[b2*b1*a1,a1^-1,a1^-1*b2*b1*a1*b1^-1,a2^-1*b2^-1*a1];
phi:=GroupHomomorphismByImages(SG,SG,gg,phiImages);phiInv:=GroupHomomorphismByImages(SG,SG,gg,phiInverseImages);
Check("phi_map_constructed",phi<>fail);Check("phi_is_homomorphism",IsGroupHomomorphism(phi));
Check("phi_inverse_map_constructed",phiInv<>fail);Check("phi_inverse_is_homomorphism",IsGroupHomomorphism(phiInv));
Check("phi_inverse_right",ForAll(gg,x->Image(phiInv,Image(phi,x))=x));
Check("phi_inverse_left",ForAll(gg,x->Image(phi,Image(phiInv,x))=x));
Check("phi_iterate_8_identity",ForAll(gg,x->IterImage(phi,x,8)=x));
for k in [1..7]do Check(Concatenation("phi_iterate_",String(k),"_nonidentity"),ForAny(gg,x->IterImage(phi,x,k)<>x));od;
physical:=[a1,b1^-1,a1^-1*b1^-1*a2,a1^-1*b1^-1*b2^-1,a1^-1,b1,a2^-1*b1*a1,b2*b1*a1];
Check("physical_inverse_pairing",ForAll([1..4],j->physical[j+4]=physical[j]^-1));
Check("physical_phi_rotation",ForAll([1..8],j->Image(phi,physical[j])=physical[(j mod 8)+1]));
Check("physical_boundary_relator",IsOne(physical[1]*physical[6]*physical[3]*physical[8]*physical[5]*physical[2]*physical[7]*physical[4]));
h:=[physical[1],physical[2]^-1,physical[3],physical[4]^-1];
Check("geometric_boundary_relator",IsOne(h[1]*h[2]*h[3]*h[4]*h[1]^-1*h[2]^-1*h[3]^-1*h[4]^-1));
Check("standard_from_geometric_a1",h[1]=a1);Check("standard_from_geometric_b1",h[2]=b1);
Check("standard_from_geometric_a2",h[2]*h[1]*h[3]=a2);Check("standard_from_geometric_b2",h[4]*h[1]^-1*h[2]^-1=b2);
C2:=CyclicGroup(IsPermGroup,2);t:=GeneratorsOfGroup(C2)[1];parity:=GroupHomomorphismByImages(SG,C2,gg,[t,t,t,t]);
Check("parity_map_constructed",parity<>fail);Check("parity_surjective",Size(Image(parity))=2);
Check("all_physical_generators_odd",ForAll(physical,x->not IsOne(Image(parity,x))));
Check("phi_preserves_parity",ForAll(gg,x->Image(parity,Image(phi,x))=Image(parity,x)));
AppendTo(OUT,"PHI8_STANDARD_IMAGES\t",List(phiImages,String),"\nPHI8_INVERSE_STANDARD_IMAGES\t",List(phiInverseImages,String),"\nPHYSICAL_STANDARD_WORDS\t",List(physical,String),"\nRESULT\tPASS\nDONE\n");
Print("WROTE ",OUT,"\n");QUIT;
