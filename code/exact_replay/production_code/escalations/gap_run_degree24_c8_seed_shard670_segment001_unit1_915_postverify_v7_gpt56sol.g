# Exact wrapper for sealed degree-24 seed workload shard670.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD670_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD670_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD670_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard670_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5C98DD58856D85C33E06849FB2BAD91C079E4FD58D1E0CD71DCEDD06A1374373";
S670_RECORDS:=[
rec(k:=15713,first:=707,last:=1064,unitFirst:=1,unitLast:=358,order:=49152,autOrder:=3145728,parity:=1,classes:=1064,raw:=52297728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2498),
rec(k:=15714,first:=1,last:=172,unitFirst:=359,unitLast:=530,order:=49152,autOrder:=6291456,parity:=1,classes:=172,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2198),
rec(k:=15715,first:=1,last:=385,unitFirst:=531,unitLast:=915,order:=49152,autOrder:=3145728,parity:=1,classes:=1044,raw:=51314688,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2660)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard670_v7_gpt56sol.g");
