f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard796_segment001_unit1_915_postverify_v7_gpt56sol.g");
if f=fail then Error("S796 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard796_v7_gpt56sol.g");
if g=fail then Error("S796 engine parse failed"); fi;
Print("SHARD796_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
