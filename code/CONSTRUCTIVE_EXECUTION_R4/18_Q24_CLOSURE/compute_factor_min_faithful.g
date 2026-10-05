Read("CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/artifacts/CAND-R4-0005_factor_regular_generators.g");;

muA := MinimalFaithfulPermutationDegree(Areg);;
Print("MU_A=", muA, "\n");
muB := MinimalFaithfulPermutationDegree(Breg);;
Print("MU_B=", muB, "\n");

repA := MinimalFaithfulPermutationRepresentation(Areg);;
if IsMapping(repA) then imageA := Image(repA);; else imageA := repA;; fi;
repB := MinimalFaithfulPermutationRepresentation(Breg);;
if IsMapping(repB) then imageB := Image(repB);; else imageB := repB;; fi;
Print("IMAGE_A_ORDER=", Size(imageA), " DEGREE=", LargestMovedPoint(imageA), " ORBITS=", List(Orbits(imageA,MovedPoints(imageA)),Length), "\n");
Print("IMAGE_B_ORDER=", Size(imageB), " DEGREE=", LargestMovedPoint(imageB), " ORBITS=", List(Orbits(imageB,MovedPoints(imageB)),Length), "\n");

PrintTo("CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/minimal_factor_images.g", "Amin := ", imageA, ";;\nBmin := ", imageB, ";;\n");;
QUIT_GAP(0);
