# Independent direct-GAP verification of all 512 C++-classified/scanned
# quotient planes.  V2 replays each candidate's own shortest depth-8 witness;
# it makes no common-witness assumption and reads no transition/collision data.
SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);SizeScreen([1000000,1000000]);
CLASSIFIER:="/mnt/d/work/revise/production_code/escalations/BOLZA_P2_CLASS3_MODULE_QUOTIENTS_GPT56SOL.txt";
SCANNER:="/mnt/d/work/revise/production_code/escalations/BOLZA_P2_CLASS3_MODULE_BASED_SCAN_GPT56SOL.txt";
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_VERIFY_BOLZA_P2_CLASS3_512_INDEPENDENT_GPT56SOL_V2.txt";
Check:=function(label,c)AppendTo(OUT,"CHECK\t",label,"\t",c,"\n");if c<>true then Error(Concatenation("check failed: ",label));fi;end;
IterImage:=function(h,x,n)local i,y;y:=x;for i in [1..n]do y:=Image(h,y);od;return y;end;
BitVector:=s->List([1..Length(s)],i->Int(s{[i]}));
BitsString:=v->Concatenation(List(v,String));
XorVector:=function(a,b)return List([1..Length(a)],i->(a[i]+b[i]) mod 2);end;
Dot:=function(a,b)return Sum([1..Length(a)],i->a[i]*b[i]) mod 2;end;
DualApply:=function(rows,f)return List(rows,r->Dot(r,f));end;
InPlane:=function(z,f1,f2)return ForAll(z,x->x=0) or z=f1 or z=f2 or z=XorVector(f1,f2);end;
PlaneKey:=function(f1,f2)local q;q:=[BitsString(f1),BitsString(f2),BitsString(XorVector(f1,f2))];Sort(q);return Concatenation(q[1],"/",q[2],"/",q[3]);end;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS3-512-INDEPENDENT-GAP-VERIFY-V2\n",
 "SUPERSEDES\tGAP_VERIFY_BOLZA_P2_CLASS3_512_INDEPENDENT_GPT56SOL_FAILED_COMMON_WITNESS_ASSUMPTION.txt\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "INDEPENDENCE\tdirect U3 pc evaluation; does not read C++ transition table, GAP B3 collision export, or propagated based-tree states\n");
F:=FreeGroup("a1","b1","a2","b2");relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[relF];sg:=GeneratorsOfGroup(SG);
phiWords:=[sg[2]^-1,sg[3]^-1*sg[2]*sg[1],sg[3]^-1*sg[2]*sg[1]*sg[2]^-1*sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]*sg[2]*sg[1]^-1*sg[2]^-1*sg[3]];
physicalWords:=[sg[1],sg[2]^-1,sg[1]^-1*sg[2]^-1*sg[3],sg[1]^-1*sg[2]^-1*sg[4]^-1,sg[1]^-1,sg[2],sg[3]^-1*sg[2]*sg[1],sg[4]*sg[2]*sg[1]];
qs:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);epi:=EpimorphismQuotientSystem(qs);U3:=Image(epi);ug:=List(sg,x->Image(epi,x));uphys:=List(physicalWords,x->Image(epi,x));pc:=Pcgs(U3);basis:=pc{[14..38]};layer:=Subgroup(U3,basis);
alpha:=GroupHomomorphismByImages(U3,U3,ug,List(phiWords,x->Image(epi,x)));rows:=List(basis,x->ExponentsOfPcElement(pc,Image(alpha,x)){[14..38]});
Check("u3_order_2pow38",Size(U3)=2^38);Check("layer_central_order_2pow25",IsSubgroup(Center(U3),layer) and Size(layer)=2^25);
Check("phi_explicit_exact_order8",ForAll(ug,x->IterImage(alpha,x,8)=x) and ForAll([1..7],k->ForAny(ug,x->IterImage(alpha,x,k)<>x)));
Check("physical_rotation",ForAll([1..8],j->Image(alpha,uphys[j])=uphys[(j mod 8)+1]));Check("physical_generate",Size(Group(uphys))=Size(U3));
C2:=CyclicGroup(IsPermGroup,2);t:=GeneratorsOfGroup(C2)[1];parity:=GroupHomomorphismByImages(U3,C2,ug,[t,t,t,t]);
Check("parity_and_layer_kernel",parity<>fail and Size(Image(parity))=2 and ForAll(basis,x->IsOne(Image(parity,x))) and ForAll(uphys,x->not IsOne(Image(parity,x))));
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;vals:=[One(U3)];frontier:=[[One(U3),0]];
for depth in [1..3]do next:=[];for item in frontier do for j in [1..8]do if item[2]=0 or j<>InvPhysicalIndex(item[2])then z:=item[1]*uphys[j];Add(vals,z);Add(next,[z,j]);fi;od;od;frontier:=next;od;
Check("direct_u3_b3_457",Length(vals)=457 and Size(Set(vals))=457);valex:=List(vals,x->ExponentsOfPcElement(pc,x));
# Classifier survivor planes.
inp:=InputTextFile(CLASSIFIER);classes:=[];line:=ReadLine(inp);
while line<>fail do if Length(line)>=11 and line{[1..11]}="B3_SURVIVOR"then tok:=SplitString(line,"\t","\r\n");Add(classes,rec(type:=tok[5],f1:=BitVector(tok[9]),f2:=BitVector(tok[11])));fi;line:=ReadLine(inp);od;CloseStream(inp);
# Scanner records, including each candidate's own witness and exact layer mask.
inp:=InputTextFile(SCANNER);scans:=[];line:=ReadLine(inp);
while line<>fail do if Length(line)>=9 and line{[1..9]}="CANDIDATE"then tok:=SplitString(line,"\t","\r\n");letters:=List(tok{[20..27]},s->Int(s{[2..Length(s)]})+1);
 Add(scans,rec(index:=Int(tok[2]),type:=tok[4],f1:=BitVector(tok[8]),f2:=BitVector(tok[10]),id:=Int(tok[14]),depth:=Int(tok[16]),mask:=BitVector(tok[18]),letters:=letters));fi;line:=ReadLine(inp);od;CloseStream(inp);
Check("parsed_512_classifier_records",Length(classes)=512);Check("parsed_512_scanner_records",Length(scans)=512);
classKeys:=List(classes,r->PlaneKey(r.f1,r.f2));scanKeys:=List(scans,r->PlaneKey(r.f1,r.f2));Check("all_512_planes_unique_both_inputs",Length(Set(classKeys))=512 and Length(Set(scanKeys))=512);
Check("classifier_scanner_plane_order_agrees",classKeys=scanKeys);Check("type_split_256_256",Number(classes,r->r.type="J1+J1")=256 and Number(classes,r->r.type="J2")=256);
allInvariant:=true;allB3:=true;allWitness:=true;b3Count:=0;witnessCount:=0;h908441:=0;h911401:=0;h912073:=0;
for n in [1..512]do r:=classes[n];srec:=scans[n];tf1:=DualApply(rows,r.f1);tf2:=DualApply(rows,r.f2);inv:=InPlane(tf1,r.f1,r.f2) and InPlane(tf2,r.f1,r.f2);if not inv then allInvariant:=false;fi;
 wordKeys:=Set(List(valex,e->Concatenation(String(e{[1..13]}),"/",String(Dot(e{[14..38]},r.f1)),String(Dot(e{[14..38]},r.f2)))));b3:=Length(wordKeys);if b3=457 then b3Count:=b3Count+1;else allB3:=false;fi;
 direct:=One(U3);for j in srec.letters do direct:=direct*uphys[j];od;dex:=ExponentsOfPcElement(pc,direct);
 reduced:=ForAll([2..Length(srec.letters)],j->srec.letters[j]<>InvPhysicalIndex(srec.letters[j-1]));
 wzero:=srec.index=n and srec.depth=8 and Length(srec.letters)=8 and reduced and ForAll(dex{[1..13]},x->x=0) and dex{[14..38]}=srec.mask and Dot(dex{[14..38]},r.f1)=0 and Dot(dex{[14..38]},r.f2)=0;
 if wzero then witnessCount:=witnessCount+1;else allWitness:=false;fi;
 if srec.id=908441 and srec.letters=[1,1,2,5,2,2,5,2]then h908441:=h908441+1;elif srec.id=911401 and srec.letters=[1,1,3,6,1,1,2,7]then h911401:=h911401+1;elif srec.id=912073 and srec.letters=[1,1,3,6,5,5,2,7]then h912073:=h912073+1;else allWitness:=false;fi;
 AppendTo(OUT,"KERNEL_CHECK\t",n,"\tTYPE\t",r.type,"\tINVARIANT\t",inv,"\tB3\t",b3,"\tWITNESS_ID\t",srec.id,"\tDIRECT_MASK\t",BitsString(dex{[14..38]}),"\tWITNESS_ZERO\t",wzero,"\n");
od;
Check("all_512_planes_phi_invariant",allInvariant);Check("all_512_direct_b3_equal457",allB3 and b3Count=512);Check("each_candidate_own_witness_directly_zero",allWitness and witnessCount=512);
Check("exact_shortest_witness_histogram",h908441=192 and h911401=128 and h912073=192);
AppendTo(OUT,"WITNESS_HISTOGRAM\tID\t908441\tDEPTH\t8\tCOUNT\t",h908441,"\tWORD\tg0 g0 g1 g4 g1 g1 g4 g1\n",
 "WITNESS_HISTOGRAM\tID\t911401\tDEPTH\t8\tCOUNT\t",h911401,"\tWORD\tg0 g0 g2 g5 g0 g0 g1 g6\n",
 "WITNESS_HISTOGRAM\tID\t912073\tDEPTH\t8\tCOUNT\t",h912073,"\tWORD\tg0 g0 g2 g5 g4 g4 g1 g6\n",
 "TOTAL\tKERNELS\t512\tUNIQUE_PLANES\t",Length(Set(classKeys)),"\tB3_EQ_457\t",b3Count,"\tDIRECT_WITNESS_ZERO\t",witnessCount,"\nRESULT\tPASS\nDONE\n");
Print("WROTE ",OUT,"\n");QUIT;
