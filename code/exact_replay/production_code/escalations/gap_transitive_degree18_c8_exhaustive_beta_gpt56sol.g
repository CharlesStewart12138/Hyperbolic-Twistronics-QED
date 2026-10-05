# Exact checkpoint slice of the degree-18 TransitiveGroups catalogue.
# Caller must bind kmin and kmax before Read().  For each distinct
# beta=alpha^4 the twisted-involution locus is computed once.
SetInfoLevel(InfoWarning,0);SizeScreen([1000000,1000000]);
if not IsBound(kmin) or not IsBound(kmax) then Error("bind kmin,kmax");fi;
OUT:=Concatenation("/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE18_C8_BETA_",String(kmin),"_",String(kmax),"_GPT56SOL.txt");
PrintTo(OUT,"CERTIFICATE_SLICE\tPF-GRP-001-C8-TRANSITIVE-DEGREE18-BETA\nGAP_VERSION\t",GAPInfo.Version,"\nRANGE\t",kmin,"\t",kmax,"\nSCOPE\tEvery order-window TransitiveGroup(18,k) in range; every Aut(G)-class of exact order 8; every seed in its alpha^4-twisted inverse locus; invariant internal C2 parity.\nOPTIMIZATION\tEach distinct beta=alpha^4 locus is enumerated exactly once.\n");
InvIndex:=i->((i-1+4) mod 8)+1;
Orbit8:=function(a,x)local z,j;z:=[x];for j in [2..8]do Add(z,Image(a,z[j-1]));od;return z;end;
B3:=function(G,z)local vals,fr,nx,u,j,d,v;vals:=[One(G)];fr:=[[One(G),0]];for d in [1..3]do nx:=[];for u in fr do for j in [1..8]do if u[2]=0 or j<>InvIndex(u[2])then v:=u[1]*z[j];Add(vals,v);Add(nx,[v,j]);fi;od;od;fr:=nx;od;return Size(Set(vals));end;
InvariantMaps:=function(G,a,maps)local gens;gens:=GeneratorsOfGroup(G);return Filtered(maps,f->ForAll(gens,g->Image(f,Image(a,g))=Image(f,g)));end;
OddSeed:=function(maps,x)return ForAny(maps,f->not IsOne(Image(f,x)));end;
Numeric:=function(k,an,rn,n,z)local p,i;AppendTo(OUT,"CANDIDATE_NUMERIC\t18T",k,"\t",an,"\t",rn,"\t",n);for p in z do for i in [1..18]do AppendTo(OUT,"\t",i^p-1);od;od;AppendTo(OUT,"\n");Print("CANDIDATE 18T",k," alpha=",an," rep=",rn," order=",n,"\n");end;
entries:=0;parityEntries:=0;classes:=0;invariantClasses:=0;betaComputations:=0;raw:=0;inverse:=0;inverseOdd:=0;orb8:=0;rel:=0;b3:=0;gen:=0;orbreps:=0;start:=Runtime();
for k in [kmin..kmax]do G:=TransitiveGroup(18,k);n:=Size(G);if n>=2338 and n<=50000 then entries:=entries+1;maps:=GQuotients(G,CyclicGroup(2));if Length(maps)>0 then parityEntries:=parityEntries+1;t:=Runtime();A:=AutomorphismGroup(G);
 if IsSolvableGroup(A)then iso:=IsomorphismPcGroup(A);P:=Image(iso);cc:=ConjugacyClasses(P);pc:=true;else cc:=ConjugacyClasses(A);pc:=false;fi;c8:=Filtered(cc,c->Order(Representative(c))=8);elems:=Elements(G);betas:=[];loci:=[];eic:=0;ei:=0;eio:=0;eo:=0;er:=0;eb:=0;eg:=0;ec:=0;an:=0;
 for ac in c8 do an:=an+1;if pc then a:=PreImagesRepresentative(iso,Representative(ac));else a:=Representative(ac);fi;ims:=InvariantMaps(G,a,maps);ci:=0;cio:=0;co:=0;cr:=0;cb:=0;cg:=0;maxb:=0;surv:=[];
  if Length(ims)>0 then eic:=eic+1;beta:=a^4;pos:=Position(betas,beta);if pos=fail then Add(betas,beta);Add(loci,Filtered(elems,x->Image(beta,x)=x^-1));pos:=Length(betas);betaComputations:=betaComputations+1;fi;locus:=loci[pos];ci:=Length(locus);
   for x in locus do if OddSeed(ims,x)then cio:=cio+1;z:=Orbit8(a,x);if Size(Set(z))=8 then co:=co+1;if IsOne(z[1]*z[6]*z[3]*z[8]*z[5]*z[2]*z[7]*z[4])then cr:=cr+1;bc:=B3(G,z);if bc>maxb then maxb:=bc;fi;if bc=457 then cb:=cb+1;if Size(Group(z))=n then cg:=cg+1;Add(surv,x);fi;fi;fi;fi;fi;od;
  fi;reps:=[];if Length(surv)>0 then C:=Centralizer(A,a);todo:=ShallowCopy(surv);while Length(todo)>0 do x:=todo[1];Add(reps,x);o:=Orbit(C,x,function(y,c)return Image(c,y);end);todo:=Filtered(todo,y->not y in o);od;fi;rn:=0;for x in reps do rn:=rn+1;Numeric(k,an,rn,n,Orbit8(a,x));od;
  ei:=ei+ci;eio:=eio+cio;eo:=eo+co;er:=er+cr;eb:=eb+cb;eg:=eg+cg;ec:=ec+Length(reps);AppendTo(OUT,"ALPHA\t18T",k,"\t",an,"\tCLASS_SIZE\t",Size(ac),"\tINVARIANT_PARITY_MAPS\t",Length(ims),"\tINVERSE_LOCUS\t",ci,"\tINVERSE_ODD\t",cio,"\tORBIT8\t",co,"\tRELATOR\t",cr,"\tMAX_B3\t",maxb,"\tB3\t",cb,"\tGENERATE\t",cg,"\tCENTRALIZER_ORBITS\t",Length(reps),"\n");
 od;classes:=classes+Length(c8);invariantClasses:=invariantClasses+eic;raw:=raw+n*Length(c8);inverse:=inverse+ei;inverseOdd:=inverseOdd+eio;orb8:=orb8+eo;rel:=rel+er;b3:=b3+eb;gen:=gen+eg;orbreps:=orbreps+ec;
 AppendTo(OUT,"ENTRY\t18T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tPARITY_MAPS\t",Length(maps),"\tORDER8_CLASSES\t",Length(c8),"\tINVARIANT_ALPHA_CLASSES\t",eic,"\tDISTINCT_BETA\t",Length(betas),"\tFULL_SEED_PAIRS\t",n*Length(c8),"\tINVERSE\t",ei,"\tINVERSE_ODD\t",eio,"\tORBIT8\t",eo,"\tRELATOR\t",er,"\tB3\t",eb,"\tGENERATE\t",eg,"\tCENTRALIZER_ORBITS\t",ec,"\tMS\t",Runtime()-t,"\n");
 fi;fi;od;
AppendTo(OUT,"TOTAL_SLICE\tRANGE\t",kmin,"\t",kmax,"\tORDER_WINDOW_ENTRIES\t",entries,"\tPARITY_ENTRIES\t",parityEntries,"\tORDER8_CLASSES\t",classes,"\tINVARIANT_ALPHA_CLASSES\t",invariantClasses,"\tBETA_COMPUTATIONS\t",betaComputations,"\tFULL_SEED_PAIRS\t",raw,"\tINVERSE\t",inverse,"\tINVERSE_ODD\t",inverseOdd,"\tORBIT8\t",orb8,"\tRELATOR\t",rel,"\tB3\t",b3,"\tGENERATE\t",gen,"\tPARITY\t",gen,"\tCENTRALIZER_ORBITS\t",orbreps,"\tMS\t",Runtime()-start,"\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
