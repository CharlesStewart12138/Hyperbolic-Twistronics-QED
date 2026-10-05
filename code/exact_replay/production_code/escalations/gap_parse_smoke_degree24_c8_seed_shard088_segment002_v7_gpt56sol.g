f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard088_segment002_unit2168_3662_postverify_v7_gpt56sol.g");
if f=fail then Error("S088 segment002 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard088_v7_gpt56sol.g");
if g=fail then Error("S088 segment002 engine parse failed"); fi;
Print("SHARD088_SEGMENT002_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
