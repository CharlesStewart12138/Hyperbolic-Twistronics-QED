# Exact wrapper for sealed degree-24 seed workload shard534.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD534_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD534_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD534_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard534_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="0A1C2F8BE88378B4371771AC954955E26CD2D845B4438BEE6CA4B42B11EBFEDB";
S534_RECORDS:=[
rec(k:=15367,first:=969,last:=1376,unitFirst:=1,unitLast:=408,order:=49152,autOrder:=3145728,parity:=7,classes:=1376,raw:=67633152,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2584),
rec(k:=15368,first:=1,last:=356,unitFirst:=409,unitLast:=764,order:=49152,autOrder:=3145728,parity:=3,classes:=356,raw:=17498112,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1051),
rec(k:=15369,first:=1,last:=151,unitFirst:=765,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=314,raw:=15433728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1444)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard534_v7_gpt56sol.g");
