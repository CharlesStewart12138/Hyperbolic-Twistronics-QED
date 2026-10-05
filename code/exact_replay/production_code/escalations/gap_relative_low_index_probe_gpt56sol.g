SetInfoLevel(InfoWarning,0); SetInfoLevel(InfoFpGroup,1);
F:=FreeGroup("r","t"); r:=F.1; t:=F.2;
E:=F/[r^2,t^8,(r*t)^8]; rr:=E.1; tt:=E.2; H:=Subgroup(E,[tt]);
start:=Runtime(); lis:=LowIndexSubgroupsFpGroup(E,H,24);
Print("BOUND 24 CLASSES ",Length(lis)," MS ",Runtime()-start," INDICES ",Collected(List(lis,L->Index(E,L))),"\n");
QUIT;
