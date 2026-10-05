SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
G:=TransitiveGroup(26,49);
PrintTo("/mnt/d/work/revise/production_code/escalations/GAP_IDENTIFY_26T49_GPT56SOL.txt",
 "TARGET\t26T49\nORDER\t",Size(G),"\nSTRUCTURE\t",StructureDescription(G),"\n");
Print("26T49 order=",Size(G)," structure=",StructureDescription(G),"\n");
QUIT;
