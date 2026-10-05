# Exact wrapper for sealed degree-24 seed workload shard251.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD251_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD251_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD251_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard251_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B94513CC72B8A3A9FC6E1FAB2E25E0EFAFD0663D95016DDFB2B89EEABF5C2511";
S251_RECORDS:=[
rec(k:=13734,first:=154,last:=848,unitFirst:=1,unitLast:=695,order:=24576,autOrder:=1572864,parity:=15,classes:=848,raw:=20840448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3143),
rec(k:=13735,first:=1,last:=960,unitFirst:=696,unitLast:=1655,order:=24576,autOrder:=1572864,parity:=15,classes:=960,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3259),
rec(k:=13736,first:=1,last:=176,unitFirst:=1656,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2259)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard251_v7_gpt56sol.g");
