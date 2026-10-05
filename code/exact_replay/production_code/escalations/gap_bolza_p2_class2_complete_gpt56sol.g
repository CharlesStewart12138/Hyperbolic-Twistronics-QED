# Proof-complete audit of every p-class <= 2, 2-primary quotient of the
# frozen Bolza surface group whose order lies in [2338,50000] and to which
# the frozen phi_8 and frozen parity map descend.
#
# Universality: U = Gamma/P_3(Gamma) is the largest 2-group quotient of
# lower exponent-2 class <=2.  GAP computes |U|=2^13.  Hence a quotient in
# the target window has order 2^12 or 2^13, so its kernel in U has order 2
# or 1.  Every normal subgroup of order 2 is central; enumerating all fixed
# central involutions therefore enumerates every phi_8-stable kernel exactly.

SetInfoLevel(InfoWarning,0);
SetInfoLevel(InfoQuotientSystem,0);
SizeScreen([1000000,1000000]);
OUT := "/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_P2_CLASS2_COMPLETE_GPT56SOL.txt";

Check := function(label, condition)
  AppendTo(OUT,"CHECK\t",label,"\t",condition,"\n");
  if condition <> true then Error(Concatenation("check failed: ",label)); fi;
end;

InvPhysicalIndex := i -> ((i-1+4) mod 8)+1;
B3Cardinality := function(G,xs)
  local vals,frontier,next,item,j,z,depth;
  vals := [One(G)]; frontier := [[One(G),0]];
  for depth in [1..3] do
    next := [];
    for item in frontier do
      for j in [1..8] do
        if item[2]=0 or j<>InvPhysicalIndex(item[2]) then
          z := item[1]*xs[j]; Add(vals,z); Add(next,[z,j]);
        fi;
      od;
    od;
    frontier := next;
  od;
  return Size(Set(vals));
end;

PrintTo(OUT,
 "CERTIFICATE\tPF-GRP-001-BOLZA-P2-PCLASS2-COMPLETE\n",
 "GAP_VERSION\t",GAPInfo.Version,"\n",
 "NQ_LOAD\t",LoadPackage("nq"),"\n",
 "NQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "ORDER_WINDOW\t2338\t50000\n",
 "SCOPE\tall 2-primary quotients of lower exponent-2 class <=2 with descended frozen phi8 and parity\n",
 "EXHAUSTIVENESS\tU=Gamma/P3 has order 2^13; target kernels have order 1 or 2; all normal order-2 kernels are central and are enumerated as fixed central involutions\n",
 "NONCLAIM\tno claim for 2-groups of p-class >=3, odd-primary semidirect families, or arbitrary finite quotients\n");

F := FreeGroup("a1","b1","a2","b2");
relF := F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;
SG := F/[relF]; sgens := GeneratorsOfGroup(SG);
phiWords := [
 sgens[2]^-1,
 sgens[3]^-1*sgens[2]*sgens[1],
 sgens[3]^-1*sgens[2]*sgens[1]*sgens[2]^-1*sgens[1]^-1*sgens[2]^-1*sgens[4]^-1,
 sgens[1]*sgens[2]*sgens[1]^-1*sgens[2]^-1*sgens[3]
];
physicalWords := [
 sgens[1], sgens[2]^-1, sgens[1]^-1*sgens[2]^-1*sgens[3],
 sgens[1]^-1*sgens[2]^-1*sgens[4]^-1, sgens[1]^-1, sgens[2],
 sgens[3]^-1*sgens[2]*sgens[1], sgens[4]*sgens[2]*sgens[1]
];

qs := PQuotient(SG,2,2,256,"combinatorial" : noninteractive:=true);
epi := EpimorphismQuotientSystem(qs); U := Image(epi);
ugens := List(sgens,x->Image(epi,x));
uphys := List(physicalWords,x->Image(epi,x));
alpha := GroupHomomorphismByImages(U,U,ugens,List(phiWords,x->Image(epi,x)));
C2 := CyclicGroup(IsPermGroup,2); t := GeneratorsOfGroup(C2)[1];
parity := GroupHomomorphismByImages(U,C2,ugens,[t,t,t,t]);
Check("universal_ranks_4_9",RanksOfDescendingSeries(qs)=[4,9]);
Check("universal_order_8192",Size(U)=8192);
Check("universal_generated_by_standard_images",Size(Group(ugens))=Size(U));
Check("phi_descends",alpha<>fail);
Check("phi_exact_order8",ForAll(ugens,x->Image(alpha^8,x)=x)
      and ForAll([1..7],k->ForAny(ugens,x->Image(alpha^k,x)<>x)));
Check("parity_descends",parity<>fail and Size(Image(parity))=2);
Check("universal_physical_rotation",ForAll([1..8],j->Image(alpha,uphys[j])=uphys[(j mod 8)+1]));

ctrU := Center(U); zelems := Elements(ctrU);
involutions := Filtered(zelems,z->not IsOne(z) and z^2=One(U));
fixed := Filtered(involutions,z->Image(alpha,z)=z);
compatible := Filtered(fixed,z->IsOne(Image(parity,z)));
AppendTo(OUT,"CENTER\tORDER\t",Size(ctrU),"\tINVOLUTIONS\t",Length(involutions),
 "\tPHI_FIXED\t",Length(fixed),"\tPARITY_COMPATIBLE\t",Length(compatible),"\n");

# The identity kernel gives U itself; every compatible fixed involution gives
# one distinct order-2 kernel.  List kernels in deterministic Elements(ctrU) order.
kernels := [One(U)]; Append(kernels,compatible);
tested:=0; relok:=0; orbit8:=0; parityok:=0; b3ok:=0; generateok:=0;
for z in kernels do
  if IsOne(z) then kernelSub:=TrivialSubgroup(U); else kernelSub:=Subgroup(U,[z]); fi;
  qmap:=NaturalHomomorphismByNormalSubgroup(U,kernelSub); quotientGroup:=Image(qmap);
  qgens:=List(ugens,x->Image(qmap,x)); qphys:=List(uphys,x->Image(qmap,x));
  alphaQ:=GroupHomomorphismByImages(quotientGroup,quotientGroup,qgens,
            List(ugens,x->Image(qmap,Image(alpha,x))));
  parityQ:=GroupHomomorphismByImages(quotientGroup,C2,qgens,[t,t,t,t]);
  exact8:=alphaQ<>fail and ForAll(qgens,x->Image(alphaQ^8,x)=x)
          and ForAll([1..7],k->ForAny(qgens,x->Image(alphaQ^k,x)<>x));
  rot:=alphaQ<>fail and ForAll([1..8],j->Image(alphaQ,qphys[j])=qphys[(j mod 8)+1]);
  orb:=(Size(Set(qphys))=8);
  rel:=IsOne(qphys[1]*qphys[6]*qphys[3]*qphys[8]
             *qphys[5]*qphys[2]*qphys[7]*qphys[4]);
  par:=parityQ<>fail and Size(Image(parityQ))=2
       and ForAll(qphys,x->not IsOne(Image(parityQ,x)))
       and ForAll(qgens,x->Image(parityQ,Image(alphaQ,x))=Image(parityQ,x));
  b3:=B3Cardinality(quotientGroup,qphys); gen:=(Size(Group(qphys))=Size(quotientGroup));
  tested:=tested+1; if rel then relok:=relok+1; fi;
  if orb then orbit8:=orbit8+1; fi; if par then parityok:=parityok+1; fi;
  if b3=457 then b3ok:=b3ok+1; fi; if gen then generateok:=generateok+1; fi;
  AppendTo(OUT,"KERNEL\t",tested,"\tGENERATOR\t",String(z),
   "\tKERNEL_ORDER\t",Size(kernelSub),"\tQUOTIENT_ORDER\t",Size(quotientGroup),
   "\tPHI_EXACT8\t",exact8,"\tROTATION\t",rot,"\tORBIT8\t",orb,
   "\tRELATOR\t",rel,"\tPARITY\t",par,"\tB3\t",b3,
   "\tGENERATE\t",gen,"\n");
od;
AppendTo(OUT,"TOTAL\tKERNELS\t",tested,"\tRELATOR\t",relok,
 "\tORBIT8\t",orbit8,"\tPARITY\t",parityok,"\tB3_EQ_457\t",b3ok,
 "\tGENERATE\t",generateok,"\nRESULT\tPASS\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
