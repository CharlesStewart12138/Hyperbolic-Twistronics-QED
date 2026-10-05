Read("CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/artifacts/CAND-R4-0005_factor_regular_generators.g");;

classes := ConjugacyClassesSubgroups(Areg);;
z := Centre(Areg);;
out := "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/SL2_9_SUBGROUP_CLASSES_RAW.tsv";;
PrintTo(out, "class_index\torder\tindex_in_A\tcontains_center\tcore_order\tstructure\tgenerator_element_ids\telement_ids\n");;

maxOrder := 0;;
maxClass := fail;;
for i in [1..Length(classes)] do
    h := Representative(classes[i]);;
    ids := SortedList(List(Elements(h), x -> 1^x - 1));;
    genids := List(GeneratorsOfGroup(h), x -> 1^x - 1);;
    containsZ := IsSubgroup(h, z);;
    coreOrder := Size(Core(Areg, h));;
    AppendTo(out,
        i, "\t", Size(h), "\t", Index(Areg,h), "\t", containsZ,
        "\t", coreOrder, "\t", StructureDescription(h), "\t",
        JoinStringsWithSeparator(List(genids,String), ","), "\t",
        JoinStringsWithSeparator(List(ids,String), ","), "\n");;
    if not containsZ and Size(h) > maxOrder then
        maxOrder := Size(h);;
        maxClass := i;;
    fi;
od;

Print("SUBGROUP_CLASS_COUNT=", Length(classes), "\n");
Print("MAX_CENTER_AVOIDING_ORDER=", maxOrder, "\n");
Print("MAX_CENTER_AVOIDING_CLASS=", maxClass, "\n");
Print("MU_TR_Q=", 46080/maxOrder, "\n");
QUIT_GAP(0);
