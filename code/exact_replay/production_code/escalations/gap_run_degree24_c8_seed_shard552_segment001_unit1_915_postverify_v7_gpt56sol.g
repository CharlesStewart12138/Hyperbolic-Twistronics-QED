# Exact wrapper for sealed degree-24 seed workload shard552.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD552_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD552_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD552_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard552_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="62A7FE5DE0C9C1BC62393DDA5F5DC3A244914590643BE5281279D9C0F262D71F";
S552_RECORDS:=[
rec(k:=15416,first:=218,last:=568,unitFirst:=1,unitLast:=351,order:=49152,autOrder:=3145728,parity:=3,classes:=568,raw:=27918336,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2140),
rec(k:=15417,first:=1,last:=316,unitFirst:=352,unitLast:=667,order:=49152,autOrder:=3145728,parity:=3,classes:=316,raw:=15532032,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1490),
rec(k:=15418,first:=1,last:=248,unitFirst:=668,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=484,raw:=23789568,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1360)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard552_v7_gpt56sol.g");
