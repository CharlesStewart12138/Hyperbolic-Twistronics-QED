# Exact wrapper for sealed degree-24 seed workload shard638.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD638_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD638_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD638_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard638_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="DA40C83B5B6163F5A5F88816DAF020FF2CD9E950860D49A2C950A9167B7568CE";
S638_RECORDS:=[
rec(k:=15663,first:=731,last:=944,unitFirst:=1,unitLast:=214,order:=49152,autOrder:=3145728,parity:=7,classes:=944,raw:=46399488,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2420),
rec(k:=15664,first:=1,last:=456,unitFirst:=215,unitLast:=670,order:=49152,autOrder:=3145728,parity:=7,classes:=456,raw:=22413312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2017),
rec(k:=15665,first:=1,last:=212,unitFirst:=671,unitLast:=882,order:=49152,autOrder:=1572864,parity:=7,classes:=212,raw:=10420224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1681),
rec(k:=15666,first:=1,last:=33,unitFirst:=883,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1632)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard638_v7_gpt56sol.g");
