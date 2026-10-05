f:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_run_degree24_c8_seed_shard005_segment002_unit12944_14648_postverify_v7_gpt56sol.g");
if f=fail then Error("S005 segment002 wrapper parse failed"); fi;
g:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard005_v7_v2_gpt56sol.g");
if g=fail then Error("S005 segment002 engine parse failed"); fi;
Print("SHARD005_SEGMENT002_V7_WRAPPER_ENGINE_PARSE_PASS\n");
QUIT_GAP(0);
