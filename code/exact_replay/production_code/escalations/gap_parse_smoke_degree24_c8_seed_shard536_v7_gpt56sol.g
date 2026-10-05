f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard536_segment001_unit1_915_postverify_v7_gpt56sol.g");
if f=fail then Error("S536 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard536_v7_gpt56sol.g");
if g=fail then Error("S536 engine parse failed"); fi;
Print("SHARD536_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
