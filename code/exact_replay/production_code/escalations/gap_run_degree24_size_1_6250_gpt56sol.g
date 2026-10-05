GetEnv:=function(s) if s="BOLZA24_KMIN" then return "1"; elif s="BOLZA24_KMAX" then return "6250"; else return fail; fi; end;
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_size_profile_gpt56sol.g");
