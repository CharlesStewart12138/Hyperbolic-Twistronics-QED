f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard066_segment001_unit1_3662_postverify_v7_gpt56sol.g");
if f=fail then Error("S066 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard066_v7_gpt56sol.g");
if g=fail then Error("S066 engine parse failed"); fi;
Print("SHARD066_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
