SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE30_CANDIDATE_STRUCTURES_GPT56SOL.txt";;
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\n");;
for k in [1001,1003,1006,1009,1134,1135,1136,1139,1141,1150] do
 G:=TransitiveGroup(30,k);;
 AppendTo(OUT,"GROUP\t30T",k,"\tORDER\t",Size(G),"\tSTRUCTURE\t",StructureDescription(G),"\n");;
od;;
AppendTo(OUT,"DONE\n");;
QUIT;;
