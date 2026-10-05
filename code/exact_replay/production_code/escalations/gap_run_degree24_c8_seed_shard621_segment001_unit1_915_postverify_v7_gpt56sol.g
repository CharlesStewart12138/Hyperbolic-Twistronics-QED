# Exact wrapper for sealed degree-24 seed workload shard621.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD621_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD621_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD621_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard621_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CECA0ABAB8C1800A0E64E8F438AB1270D704751FD41B954BD9AFB90B4DCAAF3B";
S621_RECORDS:=[
rec(k:=15610,first:=604,last:=940,unitFirst:=1,unitLast:=337,order:=49152,autOrder:=1572864,parity:=7,classes:=940,raw:=46202880,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2611),
rec(k:=15611,first:=1,last:=256,unitFirst:=338,unitLast:=593,order:=49152,autOrder:=786432,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1877),
rec(k:=15612,first:=1,last:=176,unitFirst:=594,unitLast:=769,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1433),
rec(k:=15613,first:=1,last:=146,unitFirst:=770,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=1060,raw:=52101120,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2091)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard621_v7_gpt56sol.g");
