# Exact wrapper for sealed degree-24 seed workload shard903.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD903_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD903_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD903_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard903_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="947ACDA666F386B8EB1591E3DAE3D74F726562D9832D7E1AB82BF69603D7AA9F";
S903_RECORDS:=[
rec(k:=15977,first:=4066,last:=4208,unitFirst:=1,unitLast:=143,order:=49152,autOrder:=12582912,parity:=15,classes:=4208,raw:=206831616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=8018),
rec(k:=15978,first:=1,last:=224,unitFirst:=144,unitLast:=367,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3035),
rec(k:=15979,first:=1,last:=224,unitFirst:=368,unitLast:=591,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2692),
rec(k:=15980,first:=1,last:=324,unitFirst:=592,unitLast:=915,order:=49152,autOrder:=393216,parity:=15,classes:=880,raw:=43253760,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2044)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard903_v7_gpt56sol.g");
