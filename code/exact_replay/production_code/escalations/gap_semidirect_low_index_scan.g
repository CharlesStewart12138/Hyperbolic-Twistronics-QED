# Proof-complete transitive low-index scan for the two-generator
# Bolza-by-C8 presentation.  A subgroup of index d gives one transitive
# permutation representation of degree d; GAP returns conjugacy classes.

LoadPackage("fga");

f := FreeGroup("x", "t");;
x := f.1;;
t := f.2;;
physical := List([0..7], j -> t^j * x * t^(-j));;
surfaceRelator := Product([0,5,2,7,4,1,6,3], j -> physical[j+1]);;
e := f / [t^8, t^4*x*t^(-4)*x, surfaceRelator];;
x := e.1;;
t := e.2;;
physical := List([0..7], j -> t^j * x * t^(-j));;

maxIndex := 15;;
subs := LowIndexSubgroupsFpGroup(e, maxIndex);;
indexHistogram := Collected(List(subs, IndexInWholeGroup));;

words := [ [] ];;
frontier := [ [] ];;
for depth in [1..3] do
  next := [];;
  for word in frontier do
    for j in [0..7] do
      if Length(word)=0 or j <> ((word[Length(word)] + 4) mod 8) then
        Add(next, Concatenation(word, [j]));
      fi;
    od;
  od;
  Append(words, next);
  frontier := next;
od;
if Length(words) <> 457 then Error("wrong B3 cardinality"); fi;

counts := rec(
  subgroups := Length(subs),
  finite_actions := 0,
  q_in_window := 0,
  parity_pass := 0,
  alpha8_pass := 0,
  b3_pass := 0
);;
candidates := [];;

for subgroup in subs do
  hom := FactorCosetAction(e, subgroup);;
  r := Image(hom);;
  qgens := List(physical, g -> Image(hom, g));;
  q := Group(qgens);;
  qorder := Size(q);;
  counts.finite_actions := counts.finite_actions + 1;
  if qorder >= 2338 and qorder <= 50000 then
    counts.q_in_window := counts.q_in_window + 1;
    evenGenerators := [];;
    for i in [1..8] do
      for j in [1..8] do
        Add(evenGenerators, qgens[i]*qgens[j]);
      od;
    od;
    even := Group(evenGenerators);;
    parityPass := Size(even)*2 = qorder and ForAll(qgens, g -> not g in even);;
    if parityPass then
      counts.parity_pass := counts.parity_pass + 1;
      tt := Image(hom, t);;
      alphaExact := ForAll([1..7], k ->
        ForAny(qgens, g -> g^(tt^(-k)) <> g)
      );;
      if alphaExact then
        counts.alpha8_pass := counts.alpha8_pass + 1;
        values := [];;
        for word in words do
          value := One(q);;
          for letter in word do value := value*qgens[letter+1]; od;
          Add(values, value);
        od;
        b3Pass := Length(Set(values)) = 457;
        if b3Pass then
          counts.b3_pass := counts.b3_pass + 1;
          Add(candidates, rec(
            index := IndexInWholeGroup(subgroup),
            r_order := Size(r),
            q_order := qorder,
            t_image := tt,
            physical_images := qgens
          ));
        fi;
      fi;
    fi;
  fi;
od;

Print("max_index=", maxIndex, "\n");
Print("index_histogram=", indexHistogram, "\n");
Print("counts=", counts, "\n");
Print("candidate_count=", Length(candidates), "\n");
for candidate in candidates do Print("candidate=", candidate, "\n"); od;
QUIT;
