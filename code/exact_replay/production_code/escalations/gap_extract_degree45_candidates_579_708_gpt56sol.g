SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
SRC:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE45_C8_BETA_579_708_GPT56SOL.txt";;
DST:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE45_CANDIDATES_579_708_GPT56SOL.txt";;
inp:=InputTextFile(SRC);; out:=OutputTextFile(DST,false);;
WriteAll(out,Concatenation(
 "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE45-CANDIDATE-EXPORT-579-708\n",
 "SOURCE\tGAP_TRANSITIVE_DEGREE45_C8_BETA_579_708_GPT56SOL.txt\n",
 "SOURCE_SHA256\t758E77088B68E559D2824B1B8F7541F55E8748BF873E45EC0720D6537730269D\n"));;
n:=0;; line:=ReadLine(inp);;
while line<>fail do
 if StartsWith(line,"CANDIDATE_NUMERIC\t") then WriteAll(out,line);; n:=n+1;; fi;;
 line:=ReadLine(inp);;
od;;
WriteAll(out,Concatenation("CANDIDATE_COUNT\t",String(n),"\nDONE\n"));;
CloseStream(inp);; CloseStream(out);;
if n<>4 then Error("candidate export count mismatch");; fi;;
QUIT;;
