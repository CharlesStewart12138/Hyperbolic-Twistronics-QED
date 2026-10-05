# Proof-complete TransGrp degree-21/22 C8 scan with exact beta-locus caching.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE21_22_C8_EXHAUSTIVE_GPT56SOL.txt";
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE21-22\nGAP_VERSION\t",GAPInfo.Version,"\n",
 "SCOPE\tEvery order-window TransitiveGroup(d,k), d in {21,22}; all Aut(G)-classes of exact order 8; every alpha^4-twisted inverse seed with invariant frozen parity.\n");
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
PhysicalOrbit:=function(a,x)local z,j;z:=[x];for j in [2..8]do Add(z,Image(a,z[j-1]));od;return z;end;
Relator:=z->IsOne(z[1]*z[6]*z[3]*z[8]*z[5]*z[2]*z[7]*z[4]);
B3:=function(G,z)local vals,fr,nx,u,j,d,v;vals:=[One(G)];fr:=[[One(G),0]];for d in [1..3]do nx:=[];for u in fr do for j in [1..8]do if u[2]=0 or j<>InvPhysicalIndex(u[2])then v:=u[1]*z[j];Add(vals,v);Add(nx,[v,j]);fi;od;od;fr:=nx;od;return Size(Set(vals));end;
InvariantMaps:=function(G,a,maps)local gens;gens:=GeneratorsOfGroup(G);return Filtered(maps,f->ForAll(gens,g->Image(f,Image(a,g))=Image(f,g)));end;
PrintNumeric:=function(out,d,k,an,rn,n,z)local p,i;AppendTo(out,"CANDIDATE_NUMERIC\t",d,"T",k,"\t",an,"\t",rn,"\t",n,"\t",d);for p in z do for i in [1..d]do AppendTo(out,"\t",i^p-1);od;od;AppendTo(out,"\n");end;

grand:=[0,0,0,0,0,0,0,0,0,0,0,0]; start:=Runtime();
for d in [21,22]do db:=NrTransitiveGroups(d);win:=0;pent:=0;c8tot:=0;inva:=0;betat:=0;full:=0;inv:=0;invodd:=0;orb8:=0;rel:=0;b3:=0;gen:=0;corb:=0;ds:=Runtime();
 for k in [1..db]do G:=TransitiveGroup(d,k);n:=Size(G);if n>=2338 and n<=50000 then win:=win+1;maps:=GQuotients(G,CyclicGroup(2));if Length(maps)>0 then pent:=pent+1;es:=Runtime();A:=AutomorphismGroup(G);
   if IsSolvableGroup(A)then iso:=IsomorphismPcGroup(A);allcc:=ConjugacyClasses(Image(iso));pc:=true;else allcc:=ConjugacyClasses(A);pc:=false;fi;classes:=Filtered(allcc,c->Order(Representative(c))=8);elems:=Elements(G);betas:=[];loci:=[];ct:=[0,0,0,0,0,0,0,0];an:=0;
   for ac in classes do an:=an+1;if pc then a:=PreImagesRepresentative(iso,Representative(ac));else a:=Representative(ac);fi;ims:=InvariantMaps(G,a,maps);ci:=0;cio:=0;co:=0;cr:=0;cb:=0;cg:=0;maxb:=0;surv:=[];
    if Length(ims)>0 then ct[1]:=ct[1]+1;beta:=a^4;pos:=Position(betas,beta);if pos=fail then Add(betas,beta);Add(loci,Filtered(elems,x->Image(beta,x)=x^-1));pos:=Length(betas);fi;locus:=loci[pos];ci:=Length(locus);
     for x in locus do if ForAny(ims,f->not IsOne(Image(f,x)))then cio:=cio+1;z:=PhysicalOrbit(a,x);if Size(Set(z))=8 then co:=co+1;if Relator(z)then cr:=cr+1;bc:=B3(G,z);if bc>maxb then maxb:=bc;fi;if bc=457 then cb:=cb+1;if Size(Group(z))=n then cg:=cg+1;Add(surv,x);fi;fi;fi;fi;fi;od;
    fi;
    reps:=[];if Length(surv)>0 then C:=Centralizer(A,a);todo:=ShallowCopy(surv);while Length(todo)>0 do x:=todo[1];Add(reps,x);oo:=Orbit(C,x,function(y,c)return Image(c,y);end);todo:=Filtered(todo,y->not y in oo);od;fi;rn:=0;for x in reps do rn:=rn+1;PrintNumeric(OUT,d,k,an,rn,n,PhysicalOrbit(a,x));od;
    ct:=ct+[0,ci,cio,co,cr,cb,cg,Length(reps)];AppendTo(OUT,"ALPHA\t",d,"T",k,"\t",an,"\tCLASS_SIZE\t",Size(ac),"\tINVARIANT_PARITY_MAPS\t",Length(ims),"\tINVERSE\t",ci,"\tINVERSE_ODD\t",cio,"\tORBIT8\t",co,"\tRELATOR\t",cr,"\tMAX_B3\t",maxb,"\tB3\t",cb,"\tGENERATE\t",cg,"\tORBITS\t",Length(reps),"\n");
   od;
   c8tot:=c8tot+Length(classes);inva:=inva+ct[1];betat:=betat+Length(betas);full:=full+n*Length(classes);inv:=inv+ct[2];invodd:=invodd+ct[3];orb8:=orb8+ct[4];rel:=rel+ct[5];b3:=b3+ct[6];gen:=gen+ct[7];corb:=corb+ct[8];
   AppendTo(OUT,"ENTRY\t",d,"T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tPARITY_MAPS\t",Length(maps),"\tORDER8_CLASSES\t",Length(classes),"\tINVARIANT_ALPHA_CLASSES\t",ct[1],"\tDISTINCT_BETA\t",Length(betas),"\tINVERSE\t",ct[2],"\tINVERSE_ODD\t",ct[3],"\tORBIT8\t",ct[4],"\tRELATOR\t",ct[5],"\tB3\t",ct[6],"\tGENERATE\t",ct[7],"\tORBITS\t",ct[8],"\tMS\t",Runtime()-es,"\n");
  fi;fi;od;
 AppendTo(OUT,"DEGREE_TOTAL\t",d,"\tDATABASE\t",db,"\tORDER_WINDOW\t",win,"\tPARITY_ENTRIES\t",pent,"\tORDER8_CLASSES\t",c8tot,"\tINVARIANT_ALPHA_CLASSES\t",inva,"\tDISTINCT_BETA\t",betat,"\tFULL_PAIRS\t",full,"\tINVERSE\t",inv,"\tINVERSE_ODD\t",invodd,"\tORBIT8\t",orb8,"\tRELATOR\t",rel,"\tB3\t",b3,"\tGENERATE\t",gen,"\tORBITS\t",corb,"\tMS\t",Runtime()-ds,"\n");
 grand:=grand+[db,win,pent,c8tot,inva,betat,full,inv,invodd,orb8,rel,b3];
od;
AppendTo(OUT,"TOTAL\tDATABASE\t",grand[1],"\tORDER_WINDOW\t",grand[2],"\tPARITY_ENTRIES\t",grand[3],"\tORDER8_CLASSES\t",grand[4],"\tINVARIANT_ALPHA_CLASSES\t",grand[5],"\tDISTINCT_BETA\t",grand[6],"\tFULL_PAIRS\t",grand[7],"\tINVERSE\t",grand[8],"\tINVERSE_ODD\t",grand[9],"\tORBIT8\t",grand[10],"\tRELATOR\t",grand[11],"\tB3\t",grand[12],"\tMS\t",Runtime()-start,"\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
