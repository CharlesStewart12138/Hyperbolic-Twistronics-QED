SetInfoLevel(InfoWarning,0); SetInfoLevel(InfoFpGroup,1);
F:=FreeGroup("r","t"); r:=F.1; t:=F.2;
Tri:=F/[r^2,t^8,(r*t)^8]; rr:=Tri.1; tt:=Tri.2; H:=Subgroup(Tri,[tt]);
start:=Runtime(); lis:=LowIndexSubgroupsFpGroup(Tri,H,24);
Print("BOUND 24 CLASSES ",Length(lis)," MS ",Runtime()-start," INDICES ",Collected(List(lis,L->Index(Tri,L))),"\n");
QUIT;
