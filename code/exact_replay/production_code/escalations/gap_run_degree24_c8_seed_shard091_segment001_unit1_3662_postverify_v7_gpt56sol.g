# Exact wrapper for sealed degree-24 seed workload shard091.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD091_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD091_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD091_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard091_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="52B8FB5AE686CB769F5E122B2C3412B66A07E3BF7FB64BBDE6FA62838B0494FF";
S091_RECORDS:=[
rec(k:=11651,first:=54,last:=188,unitFirst:=1,unitLast:=135,order:=12288,autOrder:=196608,parity:=3,classes:=188,raw:=2310144,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=521),
rec(k:=11652,first:=1,last:=420,unitFirst:=136,unitLast:=555,order:=12288,autOrder:=393216,parity:=3,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1228),
rec(k:=11653,first:=1,last:=420,unitFirst:=556,unitLast:=975,order:=12288,autOrder:=393216,parity:=3,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1033),
rec(k:=11654,first:=1,last:=64,unitFirst:=976,unitLast:=1039,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=699),
rec(k:=11655,first:=1,last:=64,unitFirst:=1040,unitLast:=1103,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=670),
rec(k:=11656,first:=1,last:=212,unitFirst:=1104,unitLast:=1315,order:=12288,autOrder:=196608,parity:=3,classes:=212,raw:=2605056,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=783),
rec(k:=11657,first:=1,last:=212,unitFirst:=1316,unitLast:=1527,order:=12288,autOrder:=196608,parity:=3,classes:=212,raw:=2605056,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=881),
rec(k:=11658,first:=1,last:=480,unitFirst:=1528,unitLast:=2007,order:=12288,autOrder:=393216,parity:=3,classes:=480,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=867),
rec(k:=11659,first:=1,last:=480,unitFirst:=2008,unitLast:=2487,order:=12288,autOrder:=393216,parity:=3,classes:=480,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1179),
rec(k:=11660,first:=1,last:=96,unitFirst:=2488,unitLast:=2583,order:=12288,autOrder:=98304,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=702),
rec(k:=11661,first:=1,last:=96,unitFirst:=2584,unitLast:=2679,order:=12288,autOrder:=98304,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=660),
rec(k:=11662,first:=1,last:=64,unitFirst:=2680,unitLast:=2743,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=687),
rec(k:=11663,first:=1,last:=64,unitFirst:=2744,unitLast:=2807,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=852),
rec(k:=11664,first:=1,last:=96,unitFirst:=2808,unitLast:=2903,order:=12288,autOrder:=98304,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=757),
rec(k:=11665,first:=1,last:=96,unitFirst:=2904,unitLast:=2999,order:=12288,autOrder:=98304,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=744),
rec(k:=11666,first:=1,last:=208,unitFirst:=3000,unitLast:=3207,order:=12288,autOrder:=196608,parity:=3,classes:=208,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=777),
rec(k:=11667,first:=1,last:=208,unitFirst:=3208,unitLast:=3415,order:=12288,autOrder:=196608,parity:=3,classes:=208,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=735),
rec(k:=11668,first:=1,last:=247,unitFirst:=3416,unitLast:=3662,order:=12288,autOrder:=196608,parity:=3,classes:=440,raw:=5406720,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1175)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard091_v7_gpt56sol.g");
