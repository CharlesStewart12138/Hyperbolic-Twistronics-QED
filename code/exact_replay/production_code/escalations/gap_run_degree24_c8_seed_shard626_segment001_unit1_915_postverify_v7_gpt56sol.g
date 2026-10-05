# Exact wrapper for sealed degree-24 seed workload shard626.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD626_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD626_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD626_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard626_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3A9FEB1B6D0722CAA225C3DCBAB7684E0AAC17E84017B8A9C9F1AD1679873BF0";
S626_RECORDS:=[
rec(k:=15623,first:=349,last:=840,unitFirst:=1,unitLast:=492,order:=49152,autOrder:=786432,parity:=7,classes:=840,raw:=41287680,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2758),
rec(k:=15624,first:=1,last:=52,unitFirst:=493,unitLast:=544,order:=49152,autOrder:=393216,parity:=3,classes:=52,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1969),
rec(k:=15625,first:=1,last:=128,unitFirst:=545,unitLast:=672,order:=49152,autOrder:=393216,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1440),
rec(k:=15626,first:=1,last:=114,unitFirst:=673,unitLast:=786,order:=49152,autOrder:=393216,parity:=3,classes:=114,raw:=5603328,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1816),
rec(k:=15627,first:=1,last:=129,unitFirst:=787,unitLast:=915,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1415)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard626_v7_gpt56sol.g");
