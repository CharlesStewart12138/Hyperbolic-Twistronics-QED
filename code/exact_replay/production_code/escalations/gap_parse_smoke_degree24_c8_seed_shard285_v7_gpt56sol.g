f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard285_segment001_unit1_1831_postverify_v7_gpt56sol.g");
if f=fail then Error("S285 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard285_v7_gpt56sol.g");
if g=fail then Error("S285 engine parse failed"); fi;
Print("SHARD285_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
