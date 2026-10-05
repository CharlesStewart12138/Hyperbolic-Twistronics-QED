Read("CONSTRUCTIVE_EXECUTION_R4/17_FINAL_FREEZE/artifacts/CAND-R4-0005_factor_regular_generators.g");;
Qreg := DirectProduct(Areg, Breg);;

muA := MinimalFaithfulPermutationDegree(Areg);;
muB := MinimalFaithfulPermutationDegree(Breg);;
muQ := MinimalFaithfulPermutationDegree(Qreg);;

Print("MU_A=", muA, "\n");
Print("MU_B=", muB, "\n");
Print("MU_Q=", muQ, "\n");

repQ := MinimalFaithfulPermutationRepresentation(Qreg);;
Print("REP_IS_MAPPING=", IsMapping(repQ), "\n");
if IsMapping(repQ) then
    imageQ := Image(repQ);;
else
    imageQ := repQ;;
fi;
Print("REP_IMAGE_ORDER=", Size(imageQ), "\n");
Print("REP_DEGREE=", LargestMovedPoint(imageQ), "\n");
orbits := Orbits(imageQ, MovedPoints(imageQ));;
Print("REP_ORBIT_SIZES=", List(orbits, Length), "\n");
QUIT_GAP(0);
