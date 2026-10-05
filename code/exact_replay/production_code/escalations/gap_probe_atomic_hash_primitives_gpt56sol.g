Print("RENAME_BOUND\t",IsBoundGlobal("RenameFile"),"\n");
Print("REMOVE_BOUND\t",IsBoundGlobal("RemoveFile"),"\n");
for n in Filtered(NamesGVars(),x->PositionSublist(UppercaseString(x),"SHA")<>fail or PositionSublist(UppercaseString(x),"HASH")<>fail) do
 Print("GLOBAL\t",n,"\n");
od;
QUIT;
