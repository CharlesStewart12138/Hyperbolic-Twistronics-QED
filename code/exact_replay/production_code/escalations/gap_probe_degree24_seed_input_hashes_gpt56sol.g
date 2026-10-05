for p in [
 "/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt",
 "/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv",
 "/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_v4_gpt56sol.g"
] do
 Print(p,"\t",Length(StringFile(p)),"\t",HexSHA256(StringFile(p)),"\n");
od;
QUIT;
