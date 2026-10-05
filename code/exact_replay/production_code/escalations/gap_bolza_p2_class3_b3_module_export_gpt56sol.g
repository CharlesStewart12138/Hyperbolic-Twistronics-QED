# Exact export of the class-3 layer action and every radius-3 collision whose
# difference lies in L3.  This is the complete input for the dimension <= 2
# invariant-module quotient classifier.
SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_P2_CLASS3_B3_MODULE_EXPORT_GPT56SOL.txt";
Check:=function(label,c)AppendTo(OUT,"CHECK\t",label,"\t",c,"\n");if c<>true then Error(Concatenation("check failed: ",label));fi;end;
IterImage:=function(h,x,n)local i,y;y:=x;for i in [1..n]do y:=Image(h,y);od;return y;end;
Bits:=function(v)local z;for z in v do AppendTo(OUT,String(z));od;end;
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-B3-MODULE-EXPORT\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "SCOPE\texact L3 action plus every pair among the 457 reduced radius<=3 words whose difference is in L3\n");
F:=FreeGroup("a1","b1","a2","b2");relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[relF];sg:=GeneratorsOfGroup(SG);
phiWords:=[sg[2]^-1,sg[3]^-1*sg[2]*sg[1],sg[3]^-1*sg[2]*sg[1]*sg[2]^-1*sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]*sg[2]*sg[1]^-1*sg[2]^-1*sg[3]];
physicalWords:=[sg[1],sg[2]^-1,sg[1]^-1*sg[2]^-1*sg[3],sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]^-1,sg[2],sg[3]^-1*sg[2]*sg[1],sg[4]*sg[2]*sg[1]];
qs:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);epi:=EpimorphismQuotientSystem(qs);U3:=Image(epi);ug:=List(sg,x->Image(epi,x));uphys:=List(physicalWords,x->Image(epi,x));
alpha:=GroupHomomorphismByImages(U3,U3,ug,List(phiWords,x->Image(epi,x)));pc:=Pcgs(U3);basis:=pc{[14..38]};layer:=Subgroup(U3,basis);
rows:=List(basis,x->ExponentsOfPcElement(pc,Image(alpha,x)){[14..38]});fieldRows:=List(rows,row->List(row,z->z*One(GF(2))));mat:=Matrix(GF(2),fieldRows);
Check("ranks_4_9_25",RanksOfDescendingSeries(qs)=[4,9,25]);Check("layer_order_2pow25",Size(layer)=2^25);Check("layer_central",IsSubgroup(Center(U3),layer));
Check("matrix_entries_GF2",ForAll(Flat(mat),IsFFE));Check("matrix_rank25",RankMat(mat)=25);Check("matrix_power8_identity",IsOne(mat^8));
Check("phi_iterate8_identity",ForAll(ug,x->IterImage(alpha,x,8)=x));Check("physical_rotation",ForAll([1..8],j->Image(alpha,uphys[j])=uphys[(j mod 8)+1]));
Check("physical_generate_u3",Size(Group(uphys))=Size(U3));
vals:=[One(U3)];frontier:=[[One(U3),0]];
for depth in [1..3]do next:=[];for item in frontier do for j in [1..8]do if item[2]=0 or j<>InvPhysicalIndex(item[2]) then z:=item[1]*uphys[j];Add(vals,z);Add(next,[z,j]);fi;od;od;frontier:=next;od;
Check("formal_radius3_word_count_457",Length(vals)=457);Check("u3_b3_is_457",Size(Set(vals))=457);
qmap:=NaturalHomomorphismByNormalSubgroup(U3,layer);Check("u2_order_8192",Size(Image(qmap))=8192);Check("u2_b3_is_325",Size(Set(List(vals,x->Image(qmap,x))))=325);
AppendTo(OUT,"DIM\t25\n");for i in [1..25]do AppendTo(OUT,"ROW\t",i,"\t");Bits(rows[i]);AppendTo(OUT,"\n");od;
v:=ExponentsOfPcElement(pc,ug[1]^4){[14..38]};AppendTo(OUT,"G0POWER4\t");Bits(v);AppendTo(OUT,"\nWORDS\t",Length(vals),"\n");
edges:=0;zeroedges:=0;
for i in [1..Length(vals)-1]do for j in [i+1..Length(vals)]do d:=vals[i]*vals[j]^-1;if d in layer then coords:=ExponentsOfPcElement(pc,d){[14..38]};
 edges:=edges+1;if ForAll(coords,x->x=0)then zeroedges:=zeroedges+1;fi;AppendTo(OUT,"EDGE\t",i-1,"\t",j-1,"\t");Bits(coords);AppendTo(OUT,"\n");fi;od;od;
AppendTo(OUT,"EDGE_TOTAL\t",edges,"\nZERO_EDGE_TOTAL\t",zeroedges,"\nRESULT\tPASS\nDONE\n");Print("WROTE ",OUT," edges=",edges,"\n");QUIT;
