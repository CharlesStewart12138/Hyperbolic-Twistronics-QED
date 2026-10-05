SetInfoLevel(InfoWarning,0);;
for k in [1514,1524] do
 G:=TransitiveGroup(16,k);; t:=Runtime(); A:=AutomorphismGroup(G);; t1:=Runtime();
 Print("AUT ",k," solv ",IsSolvableGroup(A)," order ",Size(A)," ms ",t1-t,"\n");
 iso:=IsomorphismPcGroup(A);; P:=Image(iso);; t2:=Runtime(); cc:=ConjugacyClasses(P);; t3:=Runtime();
 Print("PC ",k," iso_ms ",t2-t1," class_ms ",t3-t2," classes ",Length(cc)," c8 ",Length(Filtered(cc,c->Order(Representative(c))=8)),"\n");
od; QUIT;
