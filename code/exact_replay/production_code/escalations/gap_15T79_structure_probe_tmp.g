G:=TransitiveGroup(15,79);
Print("SIZE ",Size(G)," STRUCTURE ",StructureDescription(G)," PERFECT ",IsPerfectGroup(G)," DERIVED ",Size(DerivedSubgroup(G))," ABELIANIZATION ",AbelianInvariants(G),"\n");
Print("GENERATORS ",GeneratorsOfGroup(G),"\n");
QUIT;
