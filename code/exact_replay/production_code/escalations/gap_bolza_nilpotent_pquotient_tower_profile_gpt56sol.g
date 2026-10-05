# Exact universal lower-central and lower exponent-p central tower profile for
# the frozen Bolza surface-group presentation.  A universal tower term is not
# a census of all of its finite quotients; the certificate says so explicitly.

SetInfoLevel(InfoWarning, 0);
SetInfoLevel(InfoQuotientSystem, 0);
SizeScreen([1000000, 1000000]);

OUT := "/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_NILPOTENT_PQUOTIENT_TOWER_PROFILE_GPT56SOL.txt";
PrintTo(OUT,
  "CERTIFICATE\tPF-GRP-001-BOLZA-NILPOTENT-PQUOTIENT-TOWER-PROFILE\n",
  "GAP_VERSION\t", GAPInfo.Version, "\n",
  "NQ_LOAD\t", LoadPackage("nq"), "\n",
  "NQ_VERSION\t", PackageInfo("nq")[1].Version, "\n",
  "SCOPE\tuniversal characteristic lower-central quotients and universal characteristic lower exponent-p central quotients only\n",
  "NONCLAIM\tnot an enumeration of all normal quotients; no negative universal-family result is globalized\n",
  "ORDER_WINDOW\t2338\t50000\n",
  "PURE_2_EXPONENTS\t12\t15\n",
  "ODD_P_SEMIDIRECT_EXPONENTS\tp=3:7..9;p=5:5..6;p=7:4..5\n",
  "CLASS2_SKIP\tp=3,5,7 class-2 quotient enumeration is pre-existing and is not repeated\n");

F := FreeGroup("a1", "b1", "a2", "b2");
relF := F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;
SG := F / [relF];
sgens := GeneratorsOfGroup(SG);
phiWords := [
  sgens[2]^-1,
  sgens[3]^-1*sgens[2]*sgens[1],
  sgens[3]^-1*sgens[2]*sgens[1]*sgens[2]^-1*sgens[1]^-1*sgens[2]^-1*sgens[4]^-1,
  sgens[1]*sgens[2]*sgens[1]^-1*sgens[2]^-1*sgens[3]
];

start := Runtime();
for c in [1..5] do
  t := Runtime();
  N := NilpotentQuotient(SG, c);
  lcs := LowerCentralSeries(N);
  invs := [];
  for j in [1..Length(lcs)-1] do
    Add(invs, AbelianInvariants(lcs[j]/lcs[j+1]));
  od;
  AppendTo(OUT, "NQ\tCLASS\t", c,
    "\tPCP_RELATIVE_ORDERS\t", RelativeOrdersOfPcp(Pcp(N)),
    "\tLCS_FACTORS\t", invs,
    "\tHIRSCH\t", HirschLength(N),
    "\tMS\t", Runtime()-t, "\n");
od;

# Classes 1..3 suffice for the first feasibility boundary.  Class 3 already
# dominates every target log-order in the requested window; quotient-lattice
# enumeration is a separate stage and must not be conflated with this profile.
for p in [2,3,5,7] do
  for c in [1..3] do
    t := Runtime();
    qs := PQuotient(SG, p, c, 256, "combinatorial" : noninteractive := true);
    if qs = fail then
      AppendTo(OUT, "PQUOTIENT\tP\t",p,"\tCLASS\t",c,"\tRESULT\tfail\tMS\t",Runtime()-t,"\n");
    else
      ranks := RanksOfDescendingSeries(qs);
      epi := EpimorphismQuotientSystem(qs);
      P := Image(epi);
      pgens := List(sgens, x -> Image(epi,x));
      alpha := GroupHomomorphismByImages(P, P, pgens,
                 List(phiWords, x -> Image(epi,x)));
      AppendTo(OUT, "PQUOTIENT\tP\t", p,
        "\tCLASS\t", c,
        "\tRANKS\t", ranks,
        "\tLOGP_ORDER\t", Sum(ranks),
        "\tORDER\t", Size(P),
        "\tPHI_DESCENDS\t", alpha <> fail,
        "\tPHI_EXACT_ORDER8\t",
          alpha <> fail and ForAll(pgens,x->Image(alpha^8,x)=x)
            and ForAll([1..7],k->ForAny(pgens,x->Image(alpha^k,x)<>x)),
        "\tMS\t", Runtime()-t, "\n");
    fi;
  od;
od;
AppendTo(OUT,"TOTAL_MS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n");
QUIT;
