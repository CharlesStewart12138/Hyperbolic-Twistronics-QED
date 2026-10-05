# Exact wrapper for sealed degree-24 seed workload shard753.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD753_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD753_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD753_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard753_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="866BA293B477C63DFBBDF55C13D1B426D94D6BD01AA424F07142644EF904E364";
S753_RECORDS:=[
rec(k:=15809,first:=571,last:=1280,unitFirst:=1,unitLast:=710,order:=49152,autOrder:=786432,parity:=7,classes:=1280,raw:=62914560,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2250),
rec(k:=15810,first:=1,last:=72,unitFirst:=711,unitLast:=782,order:=49152,autOrder:=1572864,parity:=7,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1197),
rec(k:=15811,first:=1,last:=133,unitFirst:=783,unitLast:=915,order:=49152,autOrder:=18874368,parity:=7,classes:=296,raw:=14548992,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1294)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard753_v7_gpt56sol.g");
