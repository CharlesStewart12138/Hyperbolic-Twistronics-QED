# Exact wrapper for sealed degree-24 seed workload shard347.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD347_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD347_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD347_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard347_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="FBDE322CD96B1423B3283D8DF2662D39B0ECDD9B6405A7935591F142E8E5D569";
S347_RECORDS:=[
rec(k:=14842,first:=141,last:=200,unitFirst:=1,unitLast:=60,order:=49152,autOrder:=1572864,parity:=7,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1647),
rec(k:=14843,first:=1,last:=160,unitFirst:=61,unitLast:=220,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1198),
rec(k:=14844,first:=1,last:=128,unitFirst:=221,unitLast:=348,order:=49152,autOrder:=393216,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1017),
rec(k:=14845,first:=1,last:=144,unitFirst:=349,unitLast:=492,order:=49152,autOrder:=786432,parity:=7,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1460),
rec(k:=14846,first:=1,last:=96,unitFirst:=493,unitLast:=588,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1258),
rec(k:=14847,first:=1,last:=60,unitFirst:=589,unitLast:=648,order:=49152,autOrder:=393216,parity:=7,classes:=60,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=909),
rec(k:=14848,first:=1,last:=52,unitFirst:=649,unitLast:=700,order:=49152,autOrder:=393216,parity:=3,classes:=52,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1708),
rec(k:=14849,first:=1,last:=144,unitFirst:=701,unitLast:=844,order:=49152,autOrder:=786432,parity:=7,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1744),
rec(k:=14850,first:=1,last:=71,unitFirst:=845,unitLast:=915,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1072)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard347_v7_gpt56sol.g");
