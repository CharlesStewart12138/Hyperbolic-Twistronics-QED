# Exact relative low-index test for E=Delta(2,8,8), constrained to contain <t>.
SetInfoLevel(InfoWarning,0); SetInfoLevel(InfoFpGroup,1);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_RELATIVE_LOW_INDEX_16_GPT56SOL.txt";
F:=FreeGroup("r","t"); r:=F.1; t:=F.2;
Tri:=F/[r^2,t^8,(r*t)^8]; tt:=Tri.2; H:=Subgroup(Tri,[tt]);
start:=Runtime(); lis:=LowIndexSubgroupsFpGroup(Tri,H,16);
PrintTo(OUT,"CERTIFICATE\tRELATIVE_LOW_INDEX_DELTA_2_8_8\nGAP_VERSION\t",GAPInfo.Version,
 "\nBOUND\t16\nCONSTRAINT\tSubgroups L containing <t>\nCLASSES\t",Length(lis),
 "\nINDEX_HISTOGRAM\t",Collected(List(lis,L->Index(Tri,L))),"\nMS\t",Runtime()-start,"\nDONE\n");
Print("WROTE ",OUT,"\n"); QUIT;
