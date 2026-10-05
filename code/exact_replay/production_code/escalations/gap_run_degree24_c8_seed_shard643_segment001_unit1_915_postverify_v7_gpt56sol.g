# Exact wrapper for sealed degree-24 seed workload shard643.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD643_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD643_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD643_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard643_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3B9E07254B29A5FFADFE6AF5907B831F0E6A92AB094D29B271E937248B4A2BFD";
S643_RECORDS:=[
rec(k:=15674,first:=635,last:=1334,unitFirst:=1,unitLast:=700,order:=49152,autOrder:=3145728,parity:=3,classes:=1334,raw:=65568768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2352),
rec(k:=15675,first:=1,last:=134,unitFirst:=701,unitLast:=834,order:=49152,autOrder:=1572864,parity:=3,classes:=134,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1449),
rec(k:=15676,first:=1,last:=81,unitFirst:=835,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=358,raw:=17596416,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2626)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard643_v7_gpt56sol.g");
