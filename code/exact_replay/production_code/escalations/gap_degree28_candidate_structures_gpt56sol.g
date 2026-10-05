SetInfoLevel(InfoWarning,0);;
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE28_CANDIDATE_STRUCTURES_GPT56SOL.txt";;
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");;
for k in [439,519] do
 G:=TransitiveGroup(28,k);;
 AppendTo(OUT,"GROUP\t28T",k,"\tORDER\t",Size(G),"\tSTRUCTURE\t",StructureDescription(G),"\n");;
od;;
AppendTo(OUT,"DONE\n");;
QUIT;;
