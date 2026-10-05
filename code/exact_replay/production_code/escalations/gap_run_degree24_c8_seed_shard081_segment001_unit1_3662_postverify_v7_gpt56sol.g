# Exact wrapper for sealed degree-24 seed workload shard081.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD081_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD081_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD081_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard081_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="F367AFE070D6EB85F755C308AD5244853A815B9038719C6D476F524FA3701703";
S081_RECORDS:=[
rec(k:=11489,first:=120,last:=280,unitFirst:=1,unitLast:=161,order:=12288,autOrder:=196608,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=864),
rec(k:=11490,first:=1,last:=160,unitFirst:=162,unitLast:=321,order:=12288,autOrder:=196608,parity:=7,classes:=160,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=807),
rec(k:=11491,first:=1,last:=420,unitFirst:=322,unitLast:=741,order:=12288,autOrder:=393216,parity:=7,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1305),
rec(k:=11492,first:=1,last:=224,unitFirst:=742,unitLast:=965,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=794),
rec(k:=11493,first:=1,last:=224,unitFirst:=966,unitLast:=1189,order:=12288,autOrder:=196608,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=826),
rec(k:=11494,first:=1,last:=224,unitFirst:=1190,unitLast:=1413,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=995),
rec(k:=11495,first:=1,last:=232,unitFirst:=1414,unitLast:=1645,order:=12288,autOrder:=393216,parity:=7,classes:=232,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1084),
rec(k:=11496,first:=1,last:=224,unitFirst:=1646,unitLast:=1869,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=841),
rec(k:=11497,first:=1,last:=224,unitFirst:=1870,unitLast:=2093,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=796),
rec(k:=11498,first:=1,last:=420,unitFirst:=2094,unitLast:=2513,order:=12288,autOrder:=393216,parity:=7,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1569),
rec(k:=11499,first:=1,last:=224,unitFirst:=2514,unitLast:=2737,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=849),
rec(k:=11500,first:=1,last:=224,unitFirst:=2738,unitLast:=2961,order:=12288,autOrder:=196608,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=655),
rec(k:=11501,first:=1,last:=160,unitFirst:=2962,unitLast:=3121,order:=12288,autOrder:=196608,parity:=7,classes:=160,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=905),
rec(k:=11502,first:=1,last:=420,unitFirst:=3122,unitLast:=3541,order:=12288,autOrder:=393216,parity:=7,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1142),
rec(k:=11503,first:=1,last:=64,unitFirst:=3542,unitLast:=3605,order:=12288,autOrder:=98304,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=709),
rec(k:=11504,first:=1,last:=57,unitFirst:=3606,unitLast:=3662,order:=12288,autOrder:=98304,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=801)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard081_v7_gpt56sol.g");
