f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard408_segment001_unit1_915_postverify_v7_gpt56sol.g");
if f=fail then Error("S408 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard408_v7_gpt56sol.g");
if g=fail then Error("S408 engine parse failed"); fi;
Print("SHARD408_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
