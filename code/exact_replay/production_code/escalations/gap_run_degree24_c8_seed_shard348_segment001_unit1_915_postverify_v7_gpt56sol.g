# Exact wrapper for sealed degree-24 seed workload shard348.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD348_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD348_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD348_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard348_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9FBD4DF51321867BF107A3B1654DC71F55C998E2D6A78BB9BB1039C7449E9B56";
S348_RECORDS:=[
rec(k:=14850,first:=72,last:=96,unitFirst:=1,unitLast:=25,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1072),
rec(k:=14851,first:=1,last:=60,unitFirst:=26,unitLast:=85,order:=49152,autOrder:=393216,parity:=7,classes:=60,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=903),
rec(k:=14852,first:=1,last:=52,unitFirst:=86,unitLast:=137,order:=49152,autOrder:=393216,parity:=3,classes:=52,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1587),
rec(k:=14853,first:=1,last:=224,unitFirst:=138,unitLast:=361,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3135),
rec(k:=14854,first:=1,last:=224,unitFirst:=362,unitLast:=585,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4031),
rec(k:=14855,first:=1,last:=224,unitFirst:=586,unitLast:=809,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4182),
rec(k:=14856,first:=1,last:=106,unitFirst:=810,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=188,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2717)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard348_v7_gpt56sol.g");
