# Exact extension of the transitive-target catalogue exhaustion to degree 17.
SetInfoLevel(InfoWarning,0); SizeScreen([1000000,1000000]);
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE17_C8_EXHAUSTIVE_GPT56SOL.txt";
PrintTo(OUT,"CERTIFICATE\tPF-GRP-001-C8-TRANSITIVE-DEGREE17\nGAP_VERSION\t",GAPInfo.Version,"\n");
InvPhysicalIndex:=i->((i-1+4) mod 8)+1;
Orbit8:=function(a,x)local z,j;z:=[x];for j in [2..8]do Add(z,Image(a,z[j-1]));od;return z;end;
B3:=function(G,z)local vals,fr,nx,u,j,d,v;vals:=[One(G)];fr:=[[One(G),0]];for d in [1..3]do nx:=[];for u in fr do for j in [1..8]do if u[2]=0 or j<>InvPhysicalIndex(u[2])then v:=u[1]*z[j];Add(vals,v);Add(nx,[v,j]);fi;od;od;fr:=nx;od;return Size(Set(vals));end;
tot:=0;eligible:=0;parityEligible:=0;c8tot:=0;full:=0;inv:=0;invodd:=0;orb:=0;rel:=0;b3:=0;gen:=0;orbreps:=0;start:=Runtime();
for k in [1..NrTransitiveGroups(17)]do G:=TransitiveGroup(17,k);n:=Size(G);tot:=tot+1;if n>=2338 and n<=50000 then eligible:=eligible+1;maps:=GQuotients(G,CyclicGroup(2));if Length(maps)>0 then parityEligible:=parityEligible+1;A:=AutomorphismGroup(G);cc:=ConjugacyClasses(A);classes:=Filtered(cc,c->Order(Representative(c))=8);elems:=Elements(G);ct:=[0,0,0,0,0,0,0];an:=0;
 for ac in classes do an:=an+1;a:=Representative(ac);ims:=Filtered(maps,f->ForAll(GeneratorsOfGroup(G),g->Image(f,Image(a,g))=Image(f,g)));ci:=0;cio:=0;co:=0;cr:=0;cb:=0;cg:=0;surv:=[];
  if Length(ims)>0 then beta:=a^4;locus:=Filtered(elems,x->Image(beta,x)=x^-1);ci:=Length(locus);for x in locus do if ForAny(ims,f->not IsOne(Image(f,x)))then cio:=cio+1;z:=Orbit8(a,x);if Size(Set(z))=8 then co:=co+1;if IsOne(z[1]*z[6]*z[3]*z[8]*z[5]*z[2]*z[7]*z[4])then cr:=cr+1;if B3(G,z)=457 then cb:=cb+1;if Size(Group(z))=n then cg:=cg+1;Add(surv,x);fi;fi;fi;fi;fi;od;fi;
  reps:=[];if Length(surv)>0 then C:=Centralizer(A,a);todo:=ShallowCopy(surv);while Length(todo)>0 do x:=todo[1];Add(reps,x);o:=Orbit(C,x,function(y,c)return Image(c,y);end);todo:=Filtered(todo,y->not y in o);od;fi;
  AppendTo(OUT,"ALPHA\t17T",k,"\t",an,"\tINVARIANT_PARITY_MAPS\t",Length(ims),"\tINVERSE\t",ci,"\tINVERSE_ODD\t",cio,"\tORBIT8\t",co,"\tRELATOR\t",cr,"\tB3\t",cb,"\tGENERATE\t",cg,"\tORBITS\t",Length(reps),"\n");
  ct:=ct+[ci,cio,co,cr,cb,cg,Length(reps)];
 od;
 AppendTo(OUT,"ENTRY\t17T",k,"\tORDER\t",n,"\tAUT_ORDER\t",Size(A),"\tPARITY_MAPS\t",Length(maps),"\tORDER8_CLASSES\t",Length(classes),"\tCOUNTS\t",ct,"\n");
 c8tot:=c8tot+Length(classes);full:=full+n*Length(classes);inv:=inv+ct[1];invodd:=invodd+ct[2];orb:=orb+ct[3];rel:=rel+ct[4];b3:=b3+ct[5];gen:=gen+ct[6];orbreps:=orbreps+ct[7];
fi;fi;od;
AppendTo(OUT,"TOTAL\tDATABASE\t",tot,"\tORDER_WINDOW\t",eligible,"\tPARITY_ENTRIES\t",parityEligible,"\tORDER8_CLASSES\t",c8tot,"\tFULL_PAIRS\t",full,"\tINVERSE\t",inv,"\tINVERSE_ODD\t",invodd,"\tORBIT8\t",orb,"\tRELATOR\t",rel,"\tB3\t",b3,"\tGENERATE\t",gen,"\tORBITS\t",orbreps,"\tMS\t",Runtime()-start,"\nDONE\n");Print("WROTE ",OUT,"\n");QUIT;
