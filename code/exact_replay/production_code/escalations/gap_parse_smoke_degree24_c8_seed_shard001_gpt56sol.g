f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_gpt56sol.g");
if f=fail then Error("engine parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard001_gpt56sol.g");
if g=fail then Error("wrapper parse failed"); fi;
Print("PARSE_SMOKE_PASS\n");
QUIT;
