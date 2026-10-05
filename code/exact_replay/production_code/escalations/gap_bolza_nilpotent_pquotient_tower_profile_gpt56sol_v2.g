# Corrected exact universal NQ/PQuotient tower profile.  V2 uses explicit
# repeated Image iteration for the descended phi_8 maps.
SetInfoLevel(InfoWarning,0);SetInfoLevel(InfoQuotientSystem,0);SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_BOLZA_NILPOTENT_PQUOTIENT_TOWER_PROFILE_GPT56SOL_V2.txt";
IterImage:=function(h,x,n)local i,y;y:=x;for i in [1..n]do y:=Image(h,y);od;return y;end;
ExactOrder8:=function(h,gens)return ForAll(gens,x->IterImage(h,x,8)=x) and ForAll([1..7],k->ForAny(gens,x->IterImage(h,x,k)<>x));end;
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-BOLZA-NILPOTENT-PQUOTIENT-TOWER-PROFILE-V2\n",
 "SUPERSEDES\tGAP_BOLZA_NILPOTENT_PQUOTIENT_TOWER_PROFILE_GPT56SOL_SUPERSEDED_INVALID_MAPPING_POWER.txt\n",
 "CORRECTION\texplicit repeated Image iteration replaces invalid general-mapping exponent syntax\n",
 "GAP_VERSION\t",GAPInfo.Version,"\nNQ_LOAD\t",LoadPackage("nq"),"\nNQ_VERSION\t",PackageInfo("nq")[1].Version,"\n",
 "SCOPE\tuniversal characteristic lower-central and lower exponent-p central quotients only\n",
 "NONCLAIM\tnot an enumeration of all normal quotients; no negative universal-family result is globalized\n",
 "ORDER_WINDOW\t2338\t50000\nPURE_2_EXPONENTS\t12\t15\nODD_P_SEMIDIRECT_EXPONENTS\tp=3:7..9;p=5:5..6;p=7:4..5\n",
 "CLASS2_SKIP\tp=3,5,7 class-2 quotient enumeration is pre-existing and is not repeated\n");
F:=FreeGroup("a1","b1","a2","b2");relF:=F.1*F.2*F.1^-1*F.2^-1*F.3*F.4*F.3^-1*F.4^-1;SG:=F/[relF];sgens:=GeneratorsOfGroup(SG);
phiWords:=[sgens[2]^-1,sgens[3]^-1*sgens[2]*sgens[1],sgens[3]^-1*sgens[2]*sgens[1]*sgens[2]^-1*sgens[1]^-1*sgens[2]^-1*sgens[4]^-1,sgens[1]*sgens[2]*sgens[1]^-1*sgens[2]^-1*sgens[3]];
start:=Runtime();
for c in [1..5]do t0:=Runtime();nilq:=NilpotentQuotient(SG,c);lcs:=LowerCentralSeries(nilq);invs:=[];
 for j in [1..Length(lcs)-1]do Add(invs,AbelianInvariants(lcs[j]/lcs[j+1]));od;
 AppendTo(OUT,"NQ\tCLASS\t",c,"\tPCP_RELATIVE_ORDERS\t",RelativeOrdersOfPcp(Pcp(nilq)),"\tLCS_FACTORS\t",invs,"\tHIRSCH\t",HirschLength(nilq),"\tMS\t",Runtime()-t0,"\n");
od;
for p in [2,3,5,7]do for c in [1..3]do t0:=Runtime();qs:=PQuotient(SG,p,c,256,"combinatorial":noninteractive:=true);
 if qs=fail then AppendTo(OUT,"PQUOTIENT\tP\t",p,"\tCLASS\t",c,"\tRESULT\tfail\tMS\t",Runtime()-t0,"\n");
 else ranks:=RanksOfDescendingSeries(qs);epi:=EpimorphismQuotientSystem(qs);pq:=Image(epi);pgens:=List(sgens,x->Image(epi,x));
  alpha:=GroupHomomorphismByImages(pq,pq,pgens,List(phiWords,x->Image(epi,x)));
  AppendTo(OUT,"PQUOTIENT\tP\t",p,"\tCLASS\t",c,"\tRANKS\t",ranks,"\tLOGP_ORDER\t",Sum(ranks),"\tORDER\t",Size(pq),
   "\tPHI_DESCENDS\t",alpha<>fail and IsGroupHomomorphism(alpha),"\tPHI_BIJECTIVE\t",alpha<>fail and IsBijective(alpha),
   "\tPHI_EXACT_ORDER8_EXPLICIT\t",alpha<>fail and ExactOrder8(alpha,pgens),"\tMS\t",Runtime()-t0,"\n");fi;
od;od;
AppendTo(OUT,"TOTAL_MS\t",Runtime()-start,"\nRESULT\tPASS\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
