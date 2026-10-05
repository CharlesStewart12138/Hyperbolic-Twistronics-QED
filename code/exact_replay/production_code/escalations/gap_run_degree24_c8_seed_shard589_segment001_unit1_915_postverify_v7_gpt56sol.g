# Exact wrapper for sealed degree-24 seed workload shard589.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD589_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD589_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD589_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard589_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="FF585EC073D0EB82506FE5E94C674B014595D7666AC23165E4C073EEBAF0BD5B";
S589_RECORDS:=[
rec(k:=15538,first:=459,last:=504,unitFirst:=1,unitLast:=46,order:=49152,autOrder:=3145728,parity:=31,classes:=504,raw:=24772608,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1702),
rec(k:=15539,first:=1,last:=72,unitFirst:=47,unitLast:=118,order:=49152,autOrder:=4718592,parity:=31,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=984),
rec(k:=15540,first:=1,last:=208,unitFirst:=119,unitLast:=326,order:=49152,autOrder:=1572864,parity:=31,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1821),
rec(k:=15541,first:=1,last:=304,unitFirst:=327,unitLast:=630,order:=49152,autOrder:=1572864,parity:=7,classes:=304,raw:=14942208,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2796),
rec(k:=15542,first:=1,last:=208,unitFirst:=631,unitLast:=838,order:=49152,autOrder:=1572864,parity:=7,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2142),
rec(k:=15543,first:=1,last:=77,unitFirst:=839,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2311)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard589_v7_gpt56sol.g");
