Print("GAP_VERSION ", GAPInfo.Version, "\n");
for p in ["fga","smallgrp","transgrp","polycyclic","autpgrp"] do
  Print("PACKAGE ", p, " ", LoadPackage(p), "\n");
od;
QUIT;
