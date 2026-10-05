f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard426_segment001_unit1_915_postverify_v7_gpt56sol.g");
if f=fail then Error("S426 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard426_v7_gpt56sol.g");
if g=fail then Error("S426 engine parse failed"); fi;
Print("SHARD426_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
