SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);LoadPackage("nq");
Iter:=function(h,x,n)local j,y;y:=x;for j in [1..n]do y:=Image(h,y);od;return y;end;
F:=FreeGroup("a1","b1","a2","b2");r:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[r];s:=GeneratorsOfGroup(SG);
w:=[s[2]^-1,s[3]^-1*s[2]*s[1],s[3]^-1*s[2]*s[1]*s[2]^-1*s[1]^-1*s[2]^-1*s[4]^-1,s[1]*s[2]*s[1]^-1*s[2]^-1*s[3]];
q:=PQuotient(SG,2,3,256,"combinatorial":noninteractive:=true);e:=EpimorphismQuotientSystem(q);u:=Image(e);g:=List(s,x->Image(e,x));a:=GroupHomomorphismByImages(u,u,g,List(w,x->Image(e,x)));pc:=Pcgs(u);b:=pc{[14..38]};l:=Subgroup(u,b);
rows:=List(b,x->ExponentsOfPcElement(pc,Image(a,x)){[14..38]});m:=Matrix(GF(2),rows);ii:=IdentityMat(25,GF(2));
Print("iter8 gens=",ForAll(g,x->Iter(a,x,8)=x)," iter8 layer=",ForAll(b,x->Iter(a,x,8)=x)," matrix8=",m^8=ii,"\n");
for k in [1..8]do Print("k=",k," iterfixed=",ForAll(g,x->Iter(a,x,k)=x),"\n");od;
QUIT;
