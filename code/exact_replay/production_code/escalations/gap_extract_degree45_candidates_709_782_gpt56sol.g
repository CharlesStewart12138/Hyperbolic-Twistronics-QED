SetInfoLevel(InfoWarning,0);; SizeScreen([1000000,1000000]);;
SRC:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE45_C8_BETA_709_782_GPT56SOL.txt";;
DST:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE45_CANDIDATES_709_782_GPT56SOL.txt";;
inp:=InputTextFile(SRC);; out:=OutputTextFile(DST,false);;
WriteAll(out,Concatenation(
 "CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE45-CANDIDATE-EXPORT-709-782\n",
 "SOURCE\tGAP_TRANSITIVE_DEGREE45_C8_BETA_709_782_GPT56SOL.txt\n",
 "SOURCE_SHA256\t1A4D43BB87E171487AE89E5F22E70AD5CBB700373FFF96DCA0FE5355DBBC35A6\n"));;
n:=0;; line:=ReadLine(inp);;
while line<>fail do
 if StartsWith(line,"CANDIDATE_NUMERIC\t") then WriteAll(out,line);; n:=n+1;; fi;;
 line:=ReadLine(inp);;
od;;
WriteAll(out,Concatenation("CANDIDATE_COUNT\t",String(n),"\nDONE\n"));;
CloseStream(inp);; CloseStream(out);;
if n<>10 then Error("candidate export count mismatch");; fi;;
QUIT;;
