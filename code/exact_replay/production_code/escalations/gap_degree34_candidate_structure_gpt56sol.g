SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE34_CANDIDATE_STRUCTURE_GPT56SOL.txt";;
G:=TransitiveGroup(34,27);;
PrintTo(OUT,"GAP_VERSION\t",GAPInfo.Version,"\nGROUP\t34T27\tORDER\t",Size(G),
 "\tSTRUCTURE\t",StructureDescription(G),"\nDONE\n");;
QUIT;;
