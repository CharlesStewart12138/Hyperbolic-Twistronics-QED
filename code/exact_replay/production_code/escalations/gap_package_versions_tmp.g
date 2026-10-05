for p in ["transgrp","smallgrp","fga","autpgrp"] do
 i:=PackageInfo(p); if Length(i)>0 then Print(p," ",i[1].Version,"\n"); else Print(p," absent\n"); fi;
od; QUIT;
