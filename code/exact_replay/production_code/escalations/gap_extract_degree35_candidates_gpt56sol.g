SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
SRC:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE35_C8_BETA_1_407_GPT56SOL.txt";;
DST:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE35_CANDIDATES_GPT56SOL.txt";;
inp:=InputTextFile(SRC);; out:=OutputTextFile(DST,false);;
WriteAll(out,Concatenation(
 "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE35-CANDIDATE-EXPORT\n",
 "SOURCE\tGAP_TRANSITIVE_DEGREE35_C8_BETA_1_407_GPT56SOL.txt\n",
 "SOURCE_SHA256\tD7CE22C1B91149EC2A7CD3D43A85F432935E76E6B2EEDDF43EDF4D8A589BD27E\n"));;
n:=0;; line:=ReadLine(inp);;
while line<>fail do
 if StartsWith(line,"CANDIDATE_NUMERIC\t") then WriteAll(out,line);; n:=n+1;; fi;;
 line:=ReadLine(inp);;
od;;
WriteAll(out,Concatenation("CANDIDATE_COUNT\t",String(n),"\nDONE\n"));;
CloseStream(inp);; CloseStream(out);;
if n<>24 then Error("candidate export count mismatch");; fi;;
QUIT;;
