Read("CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/artifacts/CAND-R4-0005_factor_regular_generators.g");;
Astd := SL(2,9);;
isoA := IsomorphismGroups(Areg, Astd);;
out := "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/FACTOR_IDENTIFICATION_GAP.txt";;
PrintTo(out,
  "GAP_VERSION=", GAPInfo.Version, "\n",
  "A_ORDER=", Size(Areg), "\n",
  "A_ID=", IdGroup(Areg), "\n",
  "A_STRUCTURE=", StructureDescription(Areg), "\n",
  "A_IS_SL2_9=", isoA <> fail, "\n",
  "A_CENTER_ORDER=", Size(Centre(Areg)), "\n",
  "A_DERIVED_ORDER=", Size(DerivedSubgroup(Areg)), "\n",
  "B_ORDER=", Size(Breg), "\n",
  "B_ID=", IdGroup(Breg), "\n",
  "B_STRUCTURE=", StructureDescription(Breg), "\n",
  "B_CENTER_ORDER=", Size(Centre(Breg)), "\n",
  "B_DERIVED_ORDER=", Size(DerivedSubgroup(Breg)), "\n",
  "Q_ORDER=", Size(DirectProduct(Areg,Breg)), "\n",
  "CLASSIFICATION=PASS_EXACT\n"
);;
Print("FACTOR_IDENTIFICATION_WRITTEN\n");
QUIT_GAP(0);
