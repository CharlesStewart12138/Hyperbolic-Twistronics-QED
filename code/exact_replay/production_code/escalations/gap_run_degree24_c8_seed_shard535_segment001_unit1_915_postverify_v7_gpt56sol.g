# Exact wrapper for sealed degree-24 seed workload shard535.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD535_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD535_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD535_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard535_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="934D913000914E576730CD2B81B5444FDF7A914D3F642BA07753F624D56F1E4D";
S535_RECORDS:=[
rec(k:=15369,first:=152,last:=314,unitFirst:=1,unitLast:=163,order:=49152,autOrder:=3145728,parity:=3,classes:=314,raw:=15433728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1444),
rec(k:=15370,first:=1,last:=128,unitFirst:=164,unitLast:=291,order:=49152,autOrder:=393216,parity:=3,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1106),
rec(k:=15371,first:=1,last:=464,unitFirst:=292,unitLast:=755,order:=49152,autOrder:=786432,parity:=3,classes:=464,raw:=22806528,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1518),
rec(k:=15372,first:=1,last:=128,unitFirst:=756,unitLast:=883,order:=49152,autOrder:=393216,parity:=3,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1657),
rec(k:=15373,first:=1,last:=32,unitFirst:=884,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=888,raw:=43646976,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2618)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard535_v7_gpt56sol.g");
