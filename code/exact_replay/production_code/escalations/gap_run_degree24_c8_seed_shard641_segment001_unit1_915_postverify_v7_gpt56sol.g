# Exact wrapper for sealed degree-24 seed workload shard641.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD641_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD641_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD641_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard641_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BA2D166D9FF601C5FE4292E81C463C166F074D111CB406A9CC68BAB6674D32AD";
S641_RECORDS:=[
rec(k:=15669,first:=709,last:=986,unitFirst:=1,unitLast:=278,order:=49152,autOrder:=3145728,parity:=3,classes:=986,raw:=48463872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2161),
rec(k:=15670,first:=1,last:=364,unitFirst:=279,unitLast:=642,order:=49152,autOrder:=786432,parity:=1,classes:=364,raw:=17891328,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1151),
rec(k:=15671,first:=1,last:=72,unitFirst:=643,unitLast:=714,order:=49152,autOrder:=786432,parity:=1,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=976),
rec(k:=15672,first:=1,last:=104,unitFirst:=715,unitLast:=818,order:=49152,autOrder:=1572864,parity:=1,classes:=104,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1278),
rec(k:=15673,first:=1,last:=97,unitFirst:=819,unitLast:=915,order:=49152,autOrder:=1572864,parity:=1,classes:=378,raw:=18579456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1200)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard641_v7_gpt56sol.g");
