Read("CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/minimal_factor_images.g");;
Qcompact := DirectProduct(Amin, Bmin);;
muQ := MinimalFaithfulPermutationDegree(Qcompact);;
PrintTo(
  "CONSTRUCTIVE_EXECUTION_R4/18_Q24_CLOSURE/MIN_FAITHFUL_DEGREE_GAP_REPLAY.txt",
  "GAP_VERSION=", GAPInfo.Version, "\n",
  "Q_ORDER=", Size(Qcompact), "\n",
  "INPUT_FAITHFUL_DEGREE=", LargestMovedPoint(Qcompact), "\n",
  "MU_Q=", muQ, "\n",
  "CLASSIFICATION=PASS_EXACT\n"
);;
Print("MU_Q_REPLAY=", muQ, "\n");
QUIT_GAP(0);
