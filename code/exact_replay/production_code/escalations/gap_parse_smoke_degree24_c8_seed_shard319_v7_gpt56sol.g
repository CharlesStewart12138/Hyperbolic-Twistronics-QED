f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard319_segment001_unit1_1220_postverify_v7_gpt56sol.g");
if f=fail then Error("S319 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard319_v7_gpt56sol.g");
if g=fail then Error("S319 engine parse failed"); fi;
Print("SHARD319_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
