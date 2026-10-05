# Exact wrapper for sealed degree-24 seed workload shard603.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD603_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD603_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD603_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard603_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BDE6F99BB7225E17DF9FF3043BEC45D66A6120D6D5219F86382EE00199CDAACD";
S603_RECORDS:=[
rec(k:=15571,first:=31,last:=40,unitFirst:=1,unitLast:=10,order:=49152,autOrder:=393216,parity:=7,classes:=40,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=917),
rec(k:=15572,first:=1,last:=416,unitFirst:=11,unitLast:=426,order:=49152,autOrder:=393216,parity:=7,classes:=416,raw:=20447232,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1377),
rec(k:=15573,first:=1,last:=489,unitFirst:=427,unitLast:=915,order:=49152,autOrder:=1572864,parity:=1,classes:=1488,raw:=73138176,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2080)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard603_v7_gpt56sol.g");
