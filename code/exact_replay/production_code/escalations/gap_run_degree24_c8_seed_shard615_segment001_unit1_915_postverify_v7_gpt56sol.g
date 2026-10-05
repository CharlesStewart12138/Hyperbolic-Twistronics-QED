# Exact wrapper for sealed degree-24 seed workload shard615.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD615_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD615_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD615_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard615_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="263DA7A53A809B56FAD09B18BB8AB4761882102B0BDE33C516569123CC95709F";
S615_RECORDS:=[
rec(k:=15588,first:=10,last:=304,unitFirst:=1,unitLast:=295,order:=49152,autOrder:=1572864,parity:=3,classes:=304,raw:=14942208,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1540),
rec(k:=15589,first:=1,last:=200,unitFirst:=296,unitLast:=495,order:=49152,autOrder:=1572864,parity:=7,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1087),
rec(k:=15590,first:=1,last:=216,unitFirst:=496,unitLast:=711,order:=49152,autOrder:=1572864,parity:=3,classes:=216,raw:=10616832,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1627),
rec(k:=15591,first:=1,last:=176,unitFirst:=712,unitLast:=887,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1244),
rec(k:=15592,first:=1,last:=28,unitFirst:=888,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=168,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2080)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard615_v7_gpt56sol.g");
