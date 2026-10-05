G:=TransitiveGroup(12,242);
C:=CyclicGroup(2);
t:=Runtime(); qs:=GQuotients(G,C);;
Print("N ",Length(qs)," MS ",Runtime()-t,"\n");
for q in qs do Print(List(GeneratorsOfGroup(G),x->Image(q,x)),"\n"); od;
QUIT;
