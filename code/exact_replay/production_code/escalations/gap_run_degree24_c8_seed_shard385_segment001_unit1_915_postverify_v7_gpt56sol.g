# Exact wrapper for sealed degree-24 seed workload shard385.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD385_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD385_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD385_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard385_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3ED684E6A11DE62AECCFBBD8C2D5F2855ACC56824FA0520D8FCD4E0051828A67";
S385_RECORDS:=[
rec(k:=14986,first:=671,last:=704,unitFirst:=1,unitLast:=34,order:=49152,autOrder:=3145728,parity:=3,classes:=704,raw:=34603008,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3314),
rec(k:=14987,first:=1,last:=422,unitFirst:=35,unitLast:=456,order:=49152,autOrder:=6291456,parity:=3,classes:=422,raw:=20742144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2006),
rec(k:=14988,first:=1,last:=459,unitFirst:=457,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=466,raw:=22904832,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2891)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard385_v7_gpt56sol.g");
