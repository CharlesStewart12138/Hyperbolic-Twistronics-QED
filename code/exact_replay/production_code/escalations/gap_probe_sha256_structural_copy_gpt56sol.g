Pad:=function(h)
 while Length(h)<64 do h:=Concatenation("0",h); od;
 return h;
end;

FinalHex:=function(s)
 local r;
 r:=GAP_SHA256_FINAL(s);
 r:=Sum([0..7],i->r[8-i]*2^(32*i));
 return Pad(LowercaseString(HexStringInt(r)));
end;

expectedA:=Pad(HexSHA256("a"));
expectedAB:=Pad(HexSHA256("ab"));
s:=GAP_SHA256_INIT();
GAP_SHA256_UPDATE(s,"a");
t:=StructuralCopy(s);
h1:=FinalHex(t);
GAP_SHA256_UPDATE(s,"b");
u:=StructuralCopy(s);
h2:=FinalHex(u);
Print("STRUCTURAL_H1\t",h1,"\tEXPECT\t",expectedA,"\n");
Print("STRUCTURAL_H2\t",h2,"\tEXPECT\t",expectedAB,"\n");
if h1<>expectedA or h2<>expectedAB then Error("structural copy mismatch"); fi;

# Repeated snapshots must not mutate the live state.
v:=StructuralCopy(s); h3:=FinalHex(v);
w:=StructuralCopy(s); h4:=FinalHex(w);
Print("REPEAT_H3\t",h3,"\nREPEAT_H4\t",h4,"\n");
if h3<>expectedAB or h4<>expectedAB then Error("repeated structural snapshot mismatch"); fi;
Print("STRUCTURAL_COPY_PASS\n");
QUIT;
