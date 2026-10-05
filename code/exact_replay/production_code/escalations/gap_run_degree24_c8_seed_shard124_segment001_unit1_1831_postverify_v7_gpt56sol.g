# Exact wrapper for sealed degree-24 seed workload shard124.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD124_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD124_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD124_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard124_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="92974CA5427CBE5A0F000B926A6457E34269136A7E494941169AFA660A48CE9C";
S124_RECORDS:=[
rec(k:=12749,first:=41,last:=60,unitFirst:=1,unitLast:=20,order:=24576,autOrder:=393216,parity:=3,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=918),
rec(k:=12750,first:=1,last:=96,unitFirst:=21,unitLast:=116,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1188),
rec(k:=12751,first:=1,last:=72,unitFirst:=117,unitLast:=188,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1072),
rec(k:=12752,first:=1,last:=136,unitFirst:=189,unitLast:=324,order:=24576,autOrder:=786432,parity:=7,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=879),
rec(k:=12753,first:=1,last:=124,unitFirst:=325,unitLast:=448,order:=24576,autOrder:=786432,parity:=7,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=870),
rec(k:=12754,first:=1,last:=176,unitFirst:=449,unitLast:=624,order:=24576,autOrder:=1572864,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=993),
rec(k:=12755,first:=1,last:=162,unitFirst:=625,unitLast:=786,order:=24576,autOrder:=1572864,parity:=7,classes:=162,raw:=3981312,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1062),
rec(k:=12756,first:=1,last:=124,unitFirst:=787,unitLast:=910,order:=24576,autOrder:=786432,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=936),
rec(k:=12757,first:=1,last:=96,unitFirst:=911,unitLast:=1006,order:=24576,autOrder:=786432,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=960),
rec(k:=12758,first:=1,last:=94,unitFirst:=1007,unitLast:=1100,order:=24576,autOrder:=2359296,parity:=3,classes:=94,raw:=2310144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=946),
rec(k:=12759,first:=1,last:=78,unitFirst:=1101,unitLast:=1178,order:=24576,autOrder:=2359296,parity:=3,classes:=78,raw:=1916928,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=793),
rec(k:=12760,first:=1,last:=134,unitFirst:=1179,unitLast:=1312,order:=24576,autOrder:=4718592,parity:=7,classes:=134,raw:=3293184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1282),
rec(k:=12761,first:=1,last:=126,unitFirst:=1313,unitLast:=1438,order:=24576,autOrder:=4718592,parity:=7,classes:=126,raw:=3096576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=927),
rec(k:=12762,first:=1,last:=192,unitFirst:=1439,unitLast:=1630,order:=24576,autOrder:=1572864,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1640),
rec(k:=12763,first:=1,last:=152,unitFirst:=1631,unitLast:=1782,order:=24576,autOrder:=1572864,parity:=7,classes:=152,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1259),
rec(k:=12765,first:=1,last:=49,unitFirst:=1783,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=240,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1591)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard124_v7_gpt56sol.g");
