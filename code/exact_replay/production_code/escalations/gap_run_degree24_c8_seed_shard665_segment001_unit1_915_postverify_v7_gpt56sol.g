# Exact wrapper for sealed degree-24 seed workload shard665.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD665_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD665_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD665_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard665_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E2B0C74A18CB2AE20A1AADFFB44C6EFAD92ECB139C8F7A0E412103A0E484A730";
S665_RECORDS:=[
rec(k:=15705,first:=492,last:=1080,unitFirst:=1,unitLast:=589,order:=49152,autOrder:=1572864,parity:=7,classes:=1080,raw:=53084160,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1730),
rec(k:=15706,first:=1,last:=152,unitFirst:=590,unitLast:=741,order:=49152,autOrder:=1572864,parity:=7,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1115),
rec(k:=15707,first:=1,last:=160,unitFirst:=742,unitLast:=901,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1367),
rec(k:=15708,first:=1,last:=14,unitFirst:=902,unitLast:=915,order:=49152,autOrder:=1572864,parity:=1,classes:=1360,raw:=66846720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1587)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard665_v7_gpt56sol.g");
