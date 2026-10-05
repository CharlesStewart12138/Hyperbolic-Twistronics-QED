Print("DATABASE ",NrTransitiveGroups(17),"\n");
for k in [1..NrTransitiveGroups(17)] do G:=TransitiveGroup(17,k); n:=Size(G); if n>=2338 and n<=50000 then Print("ENTRY 17T",k," ORDER ",n," PARITY_MAPS ",Length(GQuotients(G,CyclicGroup(2))),"\n"); fi; od; QUIT;
