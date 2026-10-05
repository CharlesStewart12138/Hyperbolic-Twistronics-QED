f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard012_segment001_unit1_7324_postverify_v7_gpt56sol.g");
if f=fail then Error("S012 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard012_v7_gpt56sol.g");
if g=fail then Error("S012 engine parse failed"); fi;
Print("SHARD012_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
