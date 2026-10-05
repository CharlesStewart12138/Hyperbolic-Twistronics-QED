Read("CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/artifacts/CAND-R4-0005_factor_regular_generators.g");;

Print("GAP_VERSION=", GAPInfo.Version, "\n");
Print("A_ORDER=", Size(Areg), "\n");
Print("B_ORDER=", Size(Breg), "\n");
Print("A_ID=", IdGroup(Areg), "\n");
Print("B_ID=", IdGroup(Breg), "\n");
Print("A_STRUCTURE=", StructureDescription(Areg), "\n");
Print("B_STRUCTURE=", StructureDescription(Breg), "\n");
Print("A_CENTER=", Size(Centre(Areg)), "\n");
Print("B_CENTER=", Size(Centre(Breg)), "\n");
Print("A_DERIVED=", Size(DerivedSubgroup(Areg)), "\n");
Print("B_DERIVED=", Size(DerivedSubgroup(Breg)), "\n");
Print("A_EXPONENT=", Exponent(Areg), "\n");
Print("B_EXPONENT=", Exponent(Breg), "\n");
Print("B_NILPOTENCY_CLASS=", NilpotencyClassOfGroup(Breg), "\n");

Astd := SL(2,9);;
isoA := IsomorphismGroups(Areg, Astd);;
Print("A_IS_SL2_9=", isoA <> fail, "\n");

Qreg := DirectProduct(Areg, Breg);;
Print("Q_ORDER=", Size(Qreg), "\n");
QUIT_GAP(0);
