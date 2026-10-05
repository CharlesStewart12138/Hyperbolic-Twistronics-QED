# Export the ten Aut-centralizer orbit representatives surviving the exact
# TransitiveGroup(15,79) C8/B3/generation/parity scan as numeric permutations.

SetInfoLevel(InfoWarning,0);
SizeScreen([1000000,1000000]);
OUT := "/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_15T79_C8_CANDIDATES_GPT56SOL.dat";

InvPhysicalIndex := i -> ((i-1+4) mod 8)+1;
PhysicalOrbit := function(alpha,x)
  local xs,j;
  xs:=[x]; for j in [2..8] do Add(xs,Image(alpha,xs[j-1])); od;
  return xs;
end;
RelatorHolds := function(G,xs)
  return IsOne(xs[1]*xs[6]*xs[3]*xs[8]*xs[5]*xs[2]*xs[7]*xs[4]);
end;
B3Cardinality := function(G,xs)
  local vals,frontier,next,item,j,z,depth;
  vals:=[One(G)]; frontier:=[[One(G),0]];
  for depth in [1..3] do
    next:=[];
    for item in frontier do for j in [1..8] do
      if item[2]=0 or j<>InvPhysicalIndex(item[2]) then
        z:=item[1]*xs[j]; Add(vals,z); Add(next,[z,j]);
      fi;
    od; od;
    frontier:=next;
  od;
  return Size(Set(vals));
end;
HasFrozenParity := function(maps,xs)
  local f;
  for f in maps do
    if ForAll(xs,x->not IsOne(Image(f,x))) then return true; fi;
  od;
  return false;
end;

G:=TransitiveGroup(15,79); n:=Size(G); A:=AutomorphismGroup(G);
classes:=Filtered(ConjugacyClasses(A),c->Order(Representative(c))=8);
maps:=GQuotients(G,CyclicGroup(2)); elems:=Elements(G);
records:=[]; alphaNo:=0;
for ac in classes do
  alphaNo:=alphaNo+1; alpha:=Representative(ac); a4:=alpha^4; survivors:=[];
  for x in elems do
    if Image(a4,x)=x^-1 then
      xs:=PhysicalOrbit(alpha,x);
      if Size(Set(xs))=8 and RelatorHolds(G,xs) and B3Cardinality(G,xs)=457
         and Size(Group(xs))=n and HasFrozenParity(maps,xs) then Add(survivors,x); fi;
    fi;
  od;
  C:=Centralizer(A,alpha); todo:=ShallowCopy(survivors); repNo:=0;
  while Length(todo)>0 do
    x:=todo[1]; repNo:=repNo+1; xs:=PhysicalOrbit(alpha,x);
    Add(records,[alphaNo,repNo,xs]);
    orb:=Orbit(C,x,function(y,c) return Image(c,y); end);
    todo:=Filtered(todo,y->not y in orb);
  od;
od;

PrintTo(OUT,"BOLZA15T79\t",Length(records),"\t",n,"\n");
for row in records do
  AppendTo(OUT,row[1],"\t",row[2]);
  for p in row[3] do for i in [1..15] do AppendTo(OUT,"\t",i^p-1); od; od;
  AppendTo(OUT,"\n");
od;
Print("WROTE ",OUT," RECORDS ",Length(records),"\n");
QUIT;
