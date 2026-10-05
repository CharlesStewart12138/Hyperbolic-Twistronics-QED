SetInfoLevel(InfoWarning,0);;
SRC:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE34_C8_BETA_1_115_GPT56SOL.txt";;
DST:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE34_CANDIDATES_GPT56SOL.txt";;
inp:=InputTextFile(SRC);;
PrintTo(DST,"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE34-CANDIDATE-EXPORT\n",
 "SOURCE\tGAP_TRANSITIVE_DEGREE34_C8_BETA_1_115_GPT56SOL.txt\n",
 "SOURCE_SHA256\t50EC9689B7DC980358824D3659DFF6151239A115426BB0B4656E4E42AB2B9591\n");;
n:=0;; line:=ReadLine(inp);;
while line<>fail do
 if StartsWith(line,"CANDIDATE_NUMERIC\t") then AppendTo(DST,line);; n:=n+1;; fi;;
 line:=ReadLine(inp);;
od;;
CloseStream(inp);;
AppendTo(DST,"CANDIDATE_COUNT\t",n,"\nDONE\n");;
if n<>8 then Error("candidate export count mismatch");; fi;;
QUIT;;
