# Exact wrapper for sealed degree-24 seed workload shard706.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD706_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD706_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD706_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard706_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3D49700B2A59ECECF4739A46E5211AD1C5F22FA697B18B6B2C191F38C2D5A0AD";
S706_RECORDS:=[
rec(k:=15742,first:=1451,last:=1488,unitFirst:=1,unitLast:=38,order:=49152,autOrder:=1572864,parity:=1,classes:=1488,raw:=73138176,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2744),
rec(k:=15743,first:=1,last:=76,unitFirst:=39,unitLast:=114,order:=49152,autOrder:=1572864,parity:=1,classes:=76,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1507),
rec(k:=15744,first:=1,last:=596,unitFirst:=115,unitLast:=710,order:=49152,autOrder:=12582912,parity:=1,classes:=596,raw:=29294592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2804),
rec(k:=15745,first:=1,last:=205,unitFirst:=711,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=606,raw:=29786112,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1810)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard706_v7_gpt56sol.g");
