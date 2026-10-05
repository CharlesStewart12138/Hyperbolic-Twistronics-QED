f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard113_segment001_unit1_3662_postverify_v7_gpt56sol.g");
if f=fail then Error("S113 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard113_v7_gpt56sol.g");
if g=fail then Error("S113 engine parse failed"); fi;
Print("SHARD113_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
