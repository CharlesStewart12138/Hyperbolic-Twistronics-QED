# Independent GAP verification of the 512 C++-classified module quotients.
# It does not consume the C++ transition table or collision edges: every B3
# key and the common depth-8 witness are recomputed directly in U3.
SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);SizeScreen([1000000,1000000]);
INPATH:="/mnt/d/work/revise/production_code/escalations/BOLZA_P2_CLASS3_MODULE_QUOTIENTS_GPT56SOL.txt";
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_VERIFY_BOLZA_P2_CLASS3_512_INDEPENDENT_GPT56SOL.txt";
Check:=function(label,c)AppendTo(OUT,"CHECK\t",label,"\t",c,"\n");if c<>true then Error(Concatenation("check failed: ",label));fi;end;
IterImage:=function(h,x,n)local i,y;y:=x;for i in [1..n]do y:=Image(h,y);od;return y;end;
BitVector:=s->List([1..Length(s)],i->Int(s{[i]}));
XorVector:=function(a,b) return List([1..Length(a)],i->(a[i]+b[i]) mod 2); end;
Dot:=function(a,b) return Sum([1..Length(a)],i->a[i]*b[i]) mod 2; end;
DualApply:=function(rows,f)return List(rows,r->Dot(r,f));end;
InPlane:=function(z,f1,f2)return ForAll(z,x->x=0) or z=f1 or z=f2 or z=XorVector(f1,f2);end;
PlaneKey:=function(f1,f2)local q;q:=[Concatenation(List(f1,String)),Concatenation(List(f2,String)),Concatenation(List(XorVector(f1,f2),String))];Sort(q);return Concatenation(q[1],"/",q[2],"/",q[3]);end;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-512-INDEPENDENT-GAP-VERIFY\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "INDEPENDENCE\tdirect U3 pc evaluation; does not read C++ transition table, B3 collision export, or based-scan state\n");
F:=FreeGroup("a1","b1","a2","b2");relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[relF];sg:=GeneratorsOfGroup(SG);
phiWords:=[sg[2]^-1,sg[3]^-1*sg[2]*sg[1],sg[3]^-1*sg[2]*sg[1]*sg[2]^-1*sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]*sg[2]*sg[1]^-1*sg[2]^-1*sg[3]];
physicalWords:=[sg[1],sg[2]^-1,sg[1]^-1*sg[2]^-1*sg[3],sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]^-1,sg[2],sg[3]^-1*sg[2]*sg[1],sg[4]*sg[2]*sg[1]];
qs:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);epi:=EpimorphismQuotientSystem(qs);U3:=Image(epi);ug:=List(sg,x->Image(epi,x));uphys:=List(physicalWords,x->Image(epi,x));pc:=Pcgs(U3);basis:=pc{[14..38]};layer:=Subgroup(U3,basis);
alpha:=GroupHomomorphismByImages(U3,U3,ug,List(phiWords,x->Image(epi,x)));rows:=List(basis,x->ExponentsOfPcElement(pc,Image(alpha,x)){[14..38]});
Check("u3_order_2pow38",Size(U3)=2^38);Check("layer_central_order_2pow25",IsSubgroup(Center(U3),layer) and Size(layer)=2^25);
Check("phi_explicit_exact_order8",ForAll(ug,x->IterImage(alpha,x,8)=x) and ForAll([1..7],k->ForAny(ug,x->IterImage(alpha,x,k)<>x)));
Check("physical_rotation",ForAll([1..8],j->Image(alpha,uphys[j])=uphys[(j mod 8)+1]));Check("physical_generate",Size(Group(uphys))=Size(U3));
# Direct formal radius-three list.
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;vals:=[One(U3)];frontier:=[[One(U3),0]];
for depth in [1..3]do next:=[];for item in frontier do for j in [1..8]do if item[2]=0 or j<>InvPhysicalIndex(item[2])then z:=item[1]*uphys[j];Add(vals,z);Add(next,[z,j]);fi;od;od;frontier:=next;od;
Check("direct_u3_b3_457",Length(vals)=457 and Size(Set(vals))=457);
# Parse exactly the survivor records emitted by the independent C++ classifier.
inp:=InputTextFile(INPATH);records:=[];line:=ReadLine(inp);
while line<>fail do if Length(line)>=11 and line{[1..11]}="B3_SURVIVOR" then tok:=SplitString(line,"\t","\r\n");
 Add(records,rec(type:=tok[5],f1:=BitVector(tok[9]),f2:=BitVector(tok[11])));fi;line:=ReadLine(inp);od;CloseStream(inp);
Check("parsed_512_records",Length(records)=512);Check("all_masks_length25",ForAll(records,r->Length(r.f1)=25 and Length(r.f2)=25));
keys:=List(records,r->PlaneKey(r.f1,r.f2));Check("all_512_quotient_planes_unique",Length(Set(keys))=512);
Check("type_split_256_256",Number(records,r->r.type="J1+J1")=256 and Number(records,r->r.type="J2")=256);
# Common based witness g0 g0 g2 g5 g4 g4 g1 g6, evaluated directly.
witness:=uphys[1]*uphys[1]*uphys[3]*uphys[6]*uphys[5]*uphys[5]*uphys[2]*uphys[7];wex:=ExponentsOfPcElement(pc,witness);
expectedWitnessMask:=BitVector("0000000000000000010000000");
Check("witness_nonidentity_in_u3",not IsOne(witness));Check("witness_lies_in_l3",witness in layer and ForAll(wex{[1..13]},x->x=0));
Check("witness_layer_mask_matches_cpp",wex{[14..38]}=expectedWitnessMask);
allInvariant:=true;allB3:=true;allWitness:=true;b3Count:=0;witnessCount:=0;
for n in [1..Length(records)]do r:=records[n];tf1:=DualApply(rows,r.f1);tf2:=DualApply(rows,r.f2);inv:=InPlane(tf1,r.f1,r.f2) and InPlane(tf2,r.f1,r.f2);if not inv then allInvariant:=false;fi;
 wordKeys:=Set(List(vals,x->Concatenation(String(ExponentsOfPcElement(pc,x){[1..13]}),"/",String(Dot(ExponentsOfPcElement(pc,x){[14..38]},r.f1)),String(Dot(ExponentsOfPcElement(pc,x){[14..38]},r.f2)))));
 b3:=Length(wordKeys);if b3<>457 then allB3:=false;else b3Count:=b3Count+1;fi;wzero:=Dot(wex{[14..38]},r.f1)=0 and Dot(wex{[14..38]},r.f2)=0;if not wzero then allWitness:=false;else witnessCount:=witnessCount+1;fi;
 AppendTo(OUT,"KERNEL_CHECK\t",n,"\tTYPE\t",r.type,"\tINVARIANT\t",inv,"\tB3\t",b3,"\tWITNESS_ZERO\t",wzero,"\n");
od;
Check("all_512_planes_phi_invariant",allInvariant);Check("all_512_direct_b3_equal457",allB3);Check("common_witness_zero_in_all_512_quotients",allWitness);
AppendTo(OUT,"COMMON_WITNESS\tTREE_ID\t912073\tDEPTH\t8\tLAYER_MASK\t",Concatenation(List(wex{[14..38]},String)),"\tWORD\tg0 g0 g2 g5 g4 g4 g1 g6\n",
 "TOTAL\tKERNELS\t512\tUNIQUE_PLANES\t",Length(Set(keys)),"\tB3_EQ_457\t",b3Count,"\tWITNESS_ZERO\t",witnessCount,"\nRESULT\tPASS\nDONE\n");
Print("WROTE ",OUT,"\n");QUIT;
