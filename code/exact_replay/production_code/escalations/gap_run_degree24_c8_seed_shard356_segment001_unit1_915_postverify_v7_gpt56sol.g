# Exact wrapper for sealed degree-24 seed workload shard356.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD356_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD356_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD356_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard356_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E1A8570F6BBC3227251FC06A59534D340D743121EF6C2E8470EE9A681E1F6A3B";
S356_RECORDS:=[
rec(k:=14884,first:=84,last:=184,unitFirst:=1,unitLast:=101,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2194),
rec(k:=14885,first:=1,last:=468,unitFirst:=102,unitLast:=569,order:=49152,autOrder:=3145728,parity:=7,classes:=468,raw:=23003136,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1332),
rec(k:=14886,first:=1,last:=176,unitFirst:=570,unitLast:=745,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1378),
rec(k:=14887,first:=1,last:=170,unitFirst:=746,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2277)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard356_v7_gpt56sol.g");
