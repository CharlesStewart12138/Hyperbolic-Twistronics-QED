# Exact wrapper for sealed degree-24 seed workload shard080.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD080_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD080_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD080_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard080_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="174098433ECEFA995AEB4CC39E744F25654BDA8BA23300D0D56C659CFF99C075";
S080_RECORDS:=[
rec(k:=11476,first:=130,last:=420,unitFirst:=1,unitLast:=291,order:=12288,autOrder:=393216,parity:=7,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1482),
rec(k:=11477,first:=1,last:=224,unitFirst:=292,unitLast:=515,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=742),
rec(k:=11478,first:=1,last:=280,unitFirst:=516,unitLast:=795,order:=12288,autOrder:=196608,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1037),
rec(k:=11479,first:=1,last:=224,unitFirst:=796,unitLast:=1019,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=627),
rec(k:=11480,first:=1,last:=420,unitFirst:=1020,unitLast:=1439,order:=12288,autOrder:=393216,parity:=7,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1384),
rec(k:=11481,first:=1,last:=224,unitFirst:=1440,unitLast:=1663,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=680),
rec(k:=11482,first:=1,last:=224,unitFirst:=1664,unitLast:=1887,order:=12288,autOrder:=196608,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=711),
rec(k:=11483,first:=1,last:=224,unitFirst:=1888,unitLast:=2111,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=872),
rec(k:=11484,first:=1,last:=224,unitFirst:=2112,unitLast:=2335,order:=12288,autOrder:=196608,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=639),
rec(k:=11485,first:=1,last:=224,unitFirst:=2336,unitLast:=2559,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=829),
rec(k:=11486,first:=1,last:=340,unitFirst:=2560,unitLast:=2899,order:=12288,autOrder:=393216,parity:=7,classes:=340,raw:=4177920,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1218),
rec(k:=11487,first:=1,last:=224,unitFirst:=2900,unitLast:=3123,order:=12288,autOrder:=98304,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=662),
rec(k:=11488,first:=1,last:=420,unitFirst:=3124,unitLast:=3543,order:=12288,autOrder:=393216,parity:=7,classes:=420,raw:=5160960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1338),
rec(k:=11489,first:=1,last:=119,unitFirst:=3544,unitLast:=3662,order:=12288,autOrder:=196608,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=864)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard080_v7_gpt56sol.g");
