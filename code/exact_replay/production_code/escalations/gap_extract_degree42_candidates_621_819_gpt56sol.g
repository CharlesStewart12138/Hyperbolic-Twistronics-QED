SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
SRC:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE42_C8_BETA_621_819_V2_GPT56SOL.txt";;
DST:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE42_CANDIDATES_621_819_GPT56SOL.txt";;
inp:=InputTextFile(SRC);; out:=OutputTextFile(DST,false);;
WriteAll(out,Concatenation(
 "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE42-CANDIDATE-EXPORT-621-819\n",
 "SOURCE\tGAP_TRANSITIVE_DEGREE42_C8_BETA_621_819_V2_GPT56SOL.txt\n",
 "SOURCE_SHA256\tE4EE1A2509997C0A075380E147BEC4521C52C5E80122849E9D8C4A08693B8A05\n"));;
n:=0;; line:=ReadLine(inp);;
while line<>fail do
 if StartsWith(line,"CANDIDATE_NUMERIC\t") then WriteAll(out,line);; n:=n+1;; fi;;
 line:=ReadLine(inp);;
od;;
WriteAll(out,Concatenation("CANDIDATE_COUNT\t",String(n),"\nDONE\n"));;
CloseStream(inp);; CloseStream(out);;
if n<>8 then Error("candidate export count mismatch");; fi;;
QUIT;;
