G := TransitiveGroup(24, 12116);;
if Size(G) <> 14400 then Error("24T12116 order mismatch"); fi;
A := AutomorphismGroup(G);;
if Size(A) <> 28800 then Error("24T12116 automorphism order mismatch"); fi;
C := Filtered(ConjugacyClasses(A), c -> Order(Representative(c)) = 8);;
if Length(C) <> 1 then Error("24T12116 order-8 class mismatch"); fi;
Print("NATIVE_NATIVE_ROUTE_PASS\n");
QUIT_GAP(0);
