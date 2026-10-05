# Proof-complete C8-equivariant seed enumeration for the two order-7200
# A5-square parity targets:
#   (1) (A5 x A5) x C2 (external physical parity), and
#   (2) (A5 x A5) : C2 with the top involution swapping the factors.
# Every exact-order-eight automorphism class and every odd seed in the
# alpha^4-twisted inverse locus is tested by the frozen relator, B3, and
# generation gates.  Centralizer orbits are reported exactly.

SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
OUT := "/mnt/d/work/revise/production_code/escalations/GAP_A5_SQUARE_FACTOR_SWAP_C8_GPT56SOL.txt";
PrintTo(OUT,
 "CERTIFICATE\tPF-GRP-001-C8-A5-SQUARE-FACTOR-SWAP\n",
 "GAP_VERSION\t",GAPInfo.Version,"\n",
 "SCOPE\tAll Aut(Q)-classes of exact order 8 and all odd seeds for both explicit order-7200 parity targets.\n");

InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(alpha,x) local xs,j;
 xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od;
 return xs;
end;
RelatorHolds:=xs->IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]);
B3Cardinality:=function(G,xs)
 local vals,frontier,next,item,j,z,depth;
 vals:=[One(G)]; frontier:=[[One(G),0]];
 for depth in [1..3] do
  next:=[];
  for item in frontier do
   for j in [1..8] do
    if item[2]=0 or j<>InvPhysicalIndex(item[2]) then
     z:=item[1]*xs[j]; Add(vals,z); Add(next,[z,j]);
    fi;
   od;
  od;
  frontier:=next;
 od;
 return Size(Set(vals));
end;
InvariantParityMaps:=function(G,alpha,maps) local gens;
 gens:=GeneratorsOfGroup(G);
 return Filtered(maps,f->ForAll(gens,g->Image(f,Image(alpha,g))=Image(f,g)));
end;
SeedIsOdd:=function(maps,x)
 return ForAny(maps,f->not IsOne(Image(f,x)));
end;

ScanTarget:=function(label,G)
 local n,maps,A,allcc,c8,elems,alphaNo,ac,alpha,invmaps,beta,locus,x,xs,b,
       inv,odd,orb8,rel,b3,gen,maxb,survivors,C,todo,reps,co,rep,totalStart;
 n:=Size(G); maps:=GQuotients(G,CyclicGroup(2)); A:=AutomorphismGroup(G);
 allcc:=ConjugacyClasses(A); c8:=Filtered(allcc,c->Order(Representative(c))=8);
 elems:=Elements(G); alphaNo:=0; totalStart:=Runtime();
 AppendTo(OUT,"TARGET\t",label,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),
  "\tPARITY_MAPS\t",Length(maps),"\tORDER8_CLASSES\t",Length(c8),"\n");
 for ac in c8 do
  alphaNo:=alphaNo+1; alpha:=Representative(ac);
  invmaps:=InvariantParityMaps(G,alpha,maps); beta:=alpha^4;
  locus:=Filtered(elems,x->Image(beta,x)=x^-1);
  inv:=Length(locus); odd:=0; orb8:=0; rel:=0; b3:=0; gen:=0; maxb:=0; survivors:=[];
  for x in locus do
   if SeedIsOdd(invmaps,x) then
    odd:=odd+1; xs:=PhysicalOrbit(alpha,x);
    if Size(Set(xs))=8 then
     orb8:=orb8+1;
     if RelatorHolds(xs) then
      rel:=rel+1; b:=B3Cardinality(G,xs); if b>maxb then maxb:=b; fi;
      if b=457 then
       b3:=b3+1;
       if Size(Group(xs))=n then gen:=gen+1; Add(survivors,x); fi;
      fi;
     fi;
    fi;
   fi;
  od;
  reps:=[];
  if Length(survivors)>0 then
   C:=Centralizer(A,alpha); todo:=ShallowCopy(survivors);
   while Length(todo)>0 do
    x:=todo[1]; Add(reps,x);
    co:=Orbit(C,x,function(y,a) return Image(a,y); end);
    todo:=Filtered(todo,y->not y in co);
   od;
  fi;
  AppendTo(OUT,"ALPHA\t",label,"\t",alphaNo,"\tCLASS_SIZE\t",Size(ac),
   "\tINVARIANT_PARITY_MAPS\t",Length(invmaps),"\tINVERSE\t",inv,
   "\tINVERSE_ODD\t",odd,"\tORBIT8\t",orb8,"\tRELATOR\t",rel,
   "\tMAX_B3\t",maxb,"\tB3\t",b3,"\tGENERATE\t",gen,
   "\tCENTRALIZER_ORBITS\t",Length(reps),"\n");
  rep:=0;
  for x in reps do
   rep:=rep+1;
   AppendTo(OUT,"CANDIDATE\t",label,"\t",alphaNo,"\t",rep,"\tSEED\t",x,"\n");
  od;
 od;
 AppendTo(OUT,"TARGET_DONE\t",label,"\tMS\t",Runtime()-totalStart,"\n");
end;

A5:=AlternatingGroup(5); C2:=CyclicGroup(IsPermGroup,2);
Qexternal:=DirectProduct(A5,A5,C2);
ScanTarget("A5xA5xC2_external",Qexternal);

# Natural imprimitive wreath product; its canonical top quotient supplies the
# internal parity.  GQuotients makes the test representation-independent.
Qswap:=WreathProduct(A5,Group((1,2)));
ScanTarget("A5wrC2_internal_swap",Qswap);

AppendTo(OUT,"DONE\n");
Print("WROTE ",OUT,"\n");
QUIT;
