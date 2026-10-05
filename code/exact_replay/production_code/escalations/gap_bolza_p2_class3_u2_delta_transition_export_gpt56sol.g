# Exact multiplication decomposition for U3 as 8192 canonical U2 states plus
# a central 25-bit L3 coordinate.  One table supports all 512 B3-surviving
# two-dimensional module quotients in a single frozen based-tree pass.
SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_P2_CLASS3_U2_DELTA_TRANSITIONS_GPT56SOL.txt";
Check:=function(label,c)AppendTo(OUT,"CHECK\t",label,"\t",c,"\n");if c<>true then Error(Concatenation("check failed: ",label));fi;end;
BitsString:=v->Concatenation(List(v,String));
Code13:=v->Sum([1..13],i->v[i]*2^(i-1));
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-U2-DELTA-TRANSITIONS\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "SCOPE\texact right-multiplication table (u,g_j)->(u_prime,delta_L3) for all 8192 canonical lower-13 states\n");
F:=FreeGroup("a1","b1","a2","b2");relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[relF];sg:=GeneratorsOfGroup(SG);
physicalWords:=[sg[1],sg[2]^-1,sg[1]^-1*sg[2]^-1*sg[3],sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]^-1,sg[2],sg[3]^-1*sg[2]*sg[1],sg[4]*sg[2]*sg[1]];
qs:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);epi:=EpimorphismQuotientSystem(qs);U3:=Image(epi);ug:=List(sg,x->Image(epi,x));uphys:=List(physicalWords,x->Image(epi,x));pc:=Pcgs(U3);basis:=pc{[14..38]};layer:=Subgroup(U3,basis);
Check("ranks_4_9_25",RanksOfDescendingSeries(qs)=[4,9,25]);Check("u3_order_2pow38",Size(U3)=2^38);Check("layer_order_2pow25",Size(layer)=2^25);
Check("layer_central",IsSubgroup(Center(U3),layer));Check("all_layer_basis_order2",ForAll(basis,x->Order(x)=2));
Check("physical_generate",Size(Group(uphys))=Size(U3));
C2:=CyclicGroup(IsPermGroup,2);t:=GeneratorsOfGroup(C2)[1];parity:=GroupHomomorphismByImages(U3,C2,ug,[t,t,t,t]);
Check("parity_descends_to_u3",parity<>fail and Size(Image(parity))=2);Check("layer_in_parity_kernel",ForAll(basis,x->IsOne(Image(parity,x))));Check("physical_all_odd",ForAll(uphys,x->not IsOne(Image(parity,x))));
canon:=[];
for code in [0..8191]do z:=One(U3);for i in [1..13]do if (QuoInt(code,2^(i-1)) mod 2)=1 then z:=z*pc[i];fi;od;Add(canon,z);od;
Check("canonical_count_8192",Length(Set(canon))=8192);Check("canonical_zero_identity",IsOne(canon[1]));
AppendTo(OUT,"TABLE_ROWS\t",8192*8,"\n");
for code in [0..8191]do for j in [1..8]do ex:=ExponentsOfPcElement(pc,canon[code+1]*uphys[j]);CheckBits:=ForAll(ex,x->x=0 or x=1);if not CheckBits then Error("nonbinary pc coordinate");fi;
 AppendTo(OUT,"TRANS\t",code,"\t",j-1,"\t",Code13(ex{[1..13]}),"\t",BitsString(ex{[14..38]}),"\n");
od;od;
# 457 direct U3 states with parent/generator records independently validate
# table propagation in the C++ consumer.
vals:=[One(U3)];parents:=[-1];letters:=[-1];lastLetters:=[0];frontier:=[1];
for depth in [1..3]do next:=[];for idx in frontier do for j in [1..8]do if lastLetters[idx]=0 or j<>InvPhysicalIndex(lastLetters[idx]) then
 z:=vals[idx]*uphys[j];Add(vals,z);Add(parents,idx-1);Add(letters,j-1);Add(lastLetters,j);Add(next,Length(vals));fi;od;od;frontier:=next;od;
Check("b3_formal_count_457",Length(vals)=457);Check("u3_b3_457",Size(Set(vals))=457);
AppendTo(OUT,"B3_ROWS\t457\n");for idx in [1..457]do ex:=ExponentsOfPcElement(pc,vals[idx]);AppendTo(OUT,"B3STATE\t",idx-1,"\t",parents[idx],"\t",letters[idx],"\t",Code13(ex{[1..13]}),"\t",BitsString(ex{[14..38]}),"\n");od;
AppendTo(OUT,"RESULT\tPASS\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
