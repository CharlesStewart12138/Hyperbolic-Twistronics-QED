# Frozen-presentation consistency certificate for the Bolza surface-group
# nilpotent / p-quotient audit.  This file deliberately performs no quotient
# search: it proves that all later searches use the same SG, phi_8,
# physical generators, and parity convention as PF-GRP-001.

SetInfoLevel(InfoWarning, 0);
SizeScreen([1000000, 1000000]);

OUT := "/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_NILPOTENT_PQUOTIENT_PRESENTATION_GPT56SOL.txt";

Check := function(label, condition)
  AppendTo(OUT, "CHECK\t", label, "\t", condition, "\n");
  if condition <> true then
    Error(Concatenation("certificate check failed: ", label));
  fi;
end;

PrintTo(OUT,
  "CERTIFICATE\tPF-GRP-001-BOLZA-NILPOTENT-PQUOTIENT-PRESENTATION\n",
  "GAP_VERSION\t", GAPInfo.Version, "\n",
  "NQ_LOAD\t", LoadPackage("nq"), "\n",
  "NQ_VERSION\t", PackageInfo("nq")[1].Version, "\n",
  "ANUPQ_LOAD\t", LoadPackage("anupq"), "\n",
  "WORD_CONVENTION\tleft-to-right group multiplication as written\n",
  "STANDARD_PRESENTATION\t<a1,b1,a2,b2 | a1*b1*a1^-1*b1^-1*a2*b2*a2^-1*b2^-1>\n",
  "PARITY\ta1,b1,a2,b2 all map to the nonidentity element of C2\n",
  "SCOPE\tpresentation/map/filter interface only; no finite-quotient exhaustiveness asserted\n");

F := FreeGroup("a1", "b1", "a2", "b2");
fa1 := F.1;; fb1 := F.2;; fa2 := F.3;; fb2 := F.4;;
relF := fa1*fb1*fa1^-1*fb1^-1*fa2*fb2*fa2^-1*fb2^-1;
SG := F / [relF];
gg := GeneratorsOfGroup(SG);
a1 := gg[1];; b1 := gg[2];; a2 := gg[3];; b2 := gg[4];;

# PF-GRP-001-PHI8, expressed in the standard genus-two basis.
phiImages := [
  b1^-1,
  a2^-1*b1*a1,
  a2^-1*b1*a1*b1^-1*a1^-1*b1^-1*b2^-1,
  a1*b1*a1^-1*b1^-1*a2
];
phiInverseImages := [
  b2*b1*a1,
  a1^-1,
  a1^-1*b2*b1*a1*b1^-1,
  a2^-1*b2^-1*a1
];
phi := GroupHomomorphismByImages(SG, SG, gg, phiImages);
phiInv := GroupHomomorphismByImages(SG, SG, gg, phiInverseImages);
Check("phi_map_constructed", phi <> fail);
Check("phi_inverse_map_constructed", phiInv <> fail);
Check("phi_inverse_right", ForAll(gg, x -> Image(phiInv, Image(phi, x)) = x));
Check("phi_inverse_left", ForAll(gg, x -> Image(phi, Image(phiInv, x)) = x));
Check("phi_power_8_identity", ForAll(gg, x -> Image(phi^8, x) = x));
for k in [1..7] do
  Check(Concatenation("phi_power_", String(k), "_nonidentity"),
        ForAny(gg, x -> Image(phi^k, x) <> x));
od;

# Frozen physical side pairings g_0,...,g_7 in the standard basis.
physical := [
  a1,
  b1^-1,
  a1^-1*b1^-1*a2,
  a1^-1*b1^-1*b2^-1,
  a1^-1,
  b1,
  a2^-1*b1*a1,
  b2*b1*a1
];
Check("physical_inverse_pairing", ForAll([1..4], j -> physical[j+4] = physical[j]^-1));
Check("physical_phi_rotation", ForAll([1..8],
      j -> Image(phi, physical[j]) = physical[(j mod 8)+1]));
Check("physical_boundary_relator",
      IsOne(physical[1]*physical[6]*physical[3]*physical[8]
            *physical[5]*physical[2]*physical[7]*physical[4]));

# Oriented geometric basis h0=g0, h1=g1^-1, h2=g2, h3=g3^-1,
# and its exact inverse Nielsen map back to the standard basis.
h := [physical[1], physical[2]^-1, physical[3], physical[4]^-1];
Check("geometric_boundary_relator",
      IsOne(h[1]*h[2]*h[3]*h[4]*h[1]^-1*h[2]^-1*h[3]^-1*h[4]^-1));
Check("standard_from_geometric_a1", h[1] = a1);
Check("standard_from_geometric_b1", h[2] = b1);
Check("standard_from_geometric_a2", h[2]*h[1]*h[3] = a2);
Check("standard_from_geometric_b2", h[4]*h[1]^-1*h[2]^-1 = b2);

C2 := CyclicGroup(IsPermGroup, 2);
t := GeneratorsOfGroup(C2)[1];
parity := GroupHomomorphismByImages(SG, C2, gg, [t,t,t,t]);
Check("parity_map_constructed", parity <> fail);
Check("parity_surjective", Size(Image(parity)) = 2);
Check("all_physical_generators_odd", ForAll(physical, x -> not IsOne(Image(parity, x))));
Check("phi_preserves_parity", ForAll(gg,
      x -> Image(parity, Image(phi, x)) = Image(parity, x)));

AppendTo(OUT,
  "PHI8_STANDARD_IMAGES\t", List(phiImages, String), "\n",
  "PHI8_INVERSE_STANDARD_IMAGES\t", List(phiInverseImages, String), "\n",
  "PHYSICAL_STANDARD_WORDS\t", List(physical, String), "\n",
  "RESULT\tPASS\nDONE\n");
Print("WROTE ", OUT, "\n");
QUIT;
