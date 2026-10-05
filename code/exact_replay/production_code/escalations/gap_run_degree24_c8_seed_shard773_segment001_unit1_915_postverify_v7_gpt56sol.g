# Exact wrapper for sealed degree-24 seed workload shard773.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD773_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD773_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD773_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard773_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="EA46069346F63054D8FCE3FAFFF1ED0880AAD3BBFBE06CBEB09F0CDF48BFC42C";
S773_RECORDS:=[
rec(k:=15840,first:=657,last:=988,unitFirst:=1,unitLast:=332,order:=49152,autOrder:=1572864,parity:=3,classes:=988,raw:=48562176,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3104),
rec(k:=15841,first:=1,last:=292,unitFirst:=333,unitLast:=624,order:=49152,autOrder:=3145728,parity:=7,classes:=292,raw:=14352384,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2224),
rec(k:=15842,first:=1,last:=272,unitFirst:=625,unitLast:=896,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=5453),
rec(k:=15843,first:=1,last:=19,unitFirst:=897,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=1248,raw:=61341696,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3111)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard773_v7_gpt56sol.g");
