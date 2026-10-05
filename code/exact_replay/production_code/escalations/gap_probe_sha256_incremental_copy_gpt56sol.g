Pad:=function(h) while Length(h)<64 do h:=Concatenation("0",h); od; return h; end;
FinalHex:=function(s) local r; r:=GAP_SHA256_FINAL(s); r:=Sum([0..7],i->r[8-i]*2^(32*i)); return Pad(LowercaseString(HexStringInt(r))); end;
s:=GAP_SHA256_INIT(); GAP_SHA256_UPDATE(s,"a");
t:=ShallowCopy(s); h1:=FinalHex(t);
GAP_SHA256_UPDATE(s,"b"); t:=ShallowCopy(s); h2:=FinalHex(t);
Print("H1\t",h1,"\tEXPECT\t",Pad(HexSHA256("a")),"\n");
Print("H2\t",h2,"\tEXPECT\t",Pad(HexSHA256("ab")),"\n");
if h1<>Pad(HexSHA256("a")) or h2<>Pad(HexSHA256("ab")) then Error("incremental copy mismatch"); fi;
Print("INCREMENTAL_COPY_PASS\n"); QUIT;
