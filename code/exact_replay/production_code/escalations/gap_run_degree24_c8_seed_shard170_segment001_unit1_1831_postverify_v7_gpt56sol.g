# Exact wrapper for sealed degree-24 seed workload shard170.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD170_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD170_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD170_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard170_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2B7CCD3573A3124B4ADBC997AF383D0E73636985F7B1C79BF58C8CFFC6FBB9D7";
S170_RECORDS:=[
rec(k:=13210,first:=92,last:=302,unitFirst:=1,unitLast:=211,order:=24576,autOrder:=6291456,parity:=3,classes:=302,raw:=7421952,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1622),
rec(k:=13211,first:=1,last:=74,unitFirst:=212,unitLast:=285,order:=24576,autOrder:=1572864,parity:=3,classes:=74,raw:=1818624,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=912),
rec(k:=13212,first:=1,last:=206,unitFirst:=286,unitLast:=491,order:=24576,autOrder:=3145728,parity:=3,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2266),
rec(k:=13213,first:=1,last:=48,unitFirst:=492,unitLast:=539,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1208),
rec(k:=13214,first:=1,last:=294,unitFirst:=540,unitLast:=833,order:=24576,autOrder:=6291456,parity:=3,classes:=294,raw:=7225344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1558),
rec(k:=13215,first:=1,last:=48,unitFirst:=834,unitLast:=881,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1896),
rec(k:=13216,first:=1,last:=569,unitFirst:=882,unitLast:=1450,order:=24576,autOrder:=12582912,parity:=3,classes:=569,raw:=13983744,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2971),
rec(k:=13217,first:=1,last:=48,unitFirst:=1451,unitLast:=1498,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1854),
rec(k:=13218,first:=1,last:=48,unitFirst:=1499,unitLast:=1546,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1742),
rec(k:=13219,first:=1,last:=32,unitFirst:=1547,unitLast:=1578,order:=24576,autOrder:=786432,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1891),
rec(k:=13220,first:=1,last:=194,unitFirst:=1579,unitLast:=1772,order:=24576,autOrder:=3145728,parity:=3,classes:=194,raw:=4767744,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2282),
rec(k:=13221,first:=1,last:=48,unitFirst:=1773,unitLast:=1820,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1616),
rec(k:=13222,first:=1,last:=11,unitFirst:=1821,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=3,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1340)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard170_v7_gpt56sol.g");
