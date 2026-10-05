SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
SRC:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE42_C8_BETA_874_9491_V2_GPT56SOL.txt";;
DST:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE42_CANDIDATES_874_9491_GPT56SOL.txt";;
inp:=InputTextFile(SRC);; out:=OutputTextFile(DST,false);;
WriteAll(out,Concatenation(
 "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE42-CANDIDATE-EXPORT-874-9491\n",
 "SOURCE\tGAP_TRANSITIVE_DEGREE42_C8_BETA_874_9491_V2_GPT56SOL.txt\n",
 "SOURCE_SHA256\tF30B9BA74EA0BE4FF1032FAF9FEC1FEFD60534E2FA9DD7631419F212A39CE3F7\n"));;
n:=0;; line:=ReadLine(inp);;
while line<>fail do
 if StartsWith(line,"CANDIDATE_NUMERIC\t") then WriteAll(out,line);; n:=n+1;; fi;;
 line:=ReadLine(inp);;
od;;
WriteAll(out,Concatenation("CANDIDATE_COUNT\t",String(n),"\nDONE\n"));;
CloseStream(inp);; CloseStream(out);;
if n<>21 then Error("candidate export count mismatch");; fi;;
QUIT;;
