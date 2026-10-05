# Exact wrapper for sealed degree-24 seed workload shard076.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD076_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD076_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD076_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard076_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E12B1874A162ED1949AB2C6EE92B86B42554F97D82A6AEA06B50F6A2824B184D";
S076_RECORDS:=[
rec(k:=11389,first:=80,last:=320,unitFirst:=1,unitLast:=241,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=823),
rec(k:=11390,first:=1,last:=176,unitFirst:=242,unitLast:=417,order:=12288,autOrder:=196608,parity:=7,classes:=176,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=707),
rec(k:=11391,first:=1,last:=256,unitFirst:=418,unitLast:=673,order:=12288,autOrder:=393216,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1113),
rec(k:=11392,first:=1,last:=256,unitFirst:=674,unitLast:=929,order:=12288,autOrder:=98304,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=706),
rec(k:=11393,first:=1,last:=320,unitFirst:=930,unitLast:=1249,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=685),
rec(k:=11394,first:=1,last:=106,unitFirst:=1250,unitLast:=1355,order:=12288,autOrder:=393216,parity:=7,classes:=106,raw:=1302528,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=666),
rec(k:=11395,first:=1,last:=320,unitFirst:=1356,unitLast:=1675,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=834),
rec(k:=11396,first:=1,last:=256,unitFirst:=1676,unitLast:=1931,order:=12288,autOrder:=98304,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=755),
rec(k:=11397,first:=1,last:=320,unitFirst:=1932,unitLast:=2251,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=881),
rec(k:=11398,first:=1,last:=176,unitFirst:=2252,unitLast:=2427,order:=12288,autOrder:=196608,parity:=7,classes:=176,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=570),
rec(k:=11399,first:=1,last:=320,unitFirst:=2428,unitLast:=2747,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=807),
rec(k:=11400,first:=1,last:=106,unitFirst:=2748,unitLast:=2853,order:=12288,autOrder:=393216,parity:=7,classes:=106,raw:=1302528,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=556),
rec(k:=11401,first:=1,last:=176,unitFirst:=2854,unitLast:=3029,order:=12288,autOrder:=196608,parity:=7,classes:=176,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=612),
rec(k:=11402,first:=1,last:=256,unitFirst:=3030,unitLast:=3285,order:=12288,autOrder:=98304,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=563),
rec(k:=11403,first:=1,last:=320,unitFirst:=3286,unitLast:=3605,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=826),
rec(k:=11404,first:=1,last:=57,unitFirst:=3606,unitLast:=3662,order:=12288,autOrder:=786432,parity:=7,classes:=92,raw:=1130496,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=788)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard076_v7_gpt56sol.g");
