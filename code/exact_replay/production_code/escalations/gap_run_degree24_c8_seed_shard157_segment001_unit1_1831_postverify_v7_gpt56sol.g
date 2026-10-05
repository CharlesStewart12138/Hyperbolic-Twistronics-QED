# Exact wrapper for sealed degree-24 seed workload shard157.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD157_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD157_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD157_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard157_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="FC2CE42EAFAEB34F8A682476A204B128D56207E9A4E4B43275D749C268D8C000";
S157_RECORDS:=[
rec(k:=13107,first:=36,last:=188,unitFirst:=1,unitLast:=153,order:=24576,autOrder:=3145728,parity:=15,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1802),
rec(k:=13108,first:=1,last:=96,unitFirst:=154,unitLast:=249,order:=24576,autOrder:=786432,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1560),
rec(k:=13109,first:=1,last:=48,unitFirst:=250,unitLast:=297,order:=24576,autOrder:=786432,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1396),
rec(k:=13110,first:=1,last:=64,unitFirst:=298,unitLast:=361,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1426),
rec(k:=13111,first:=1,last:=96,unitFirst:=362,unitLast:=457,order:=24576,autOrder:=786432,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1240),
rec(k:=13112,first:=1,last:=142,unitFirst:=458,unitLast:=599,order:=24576,autOrder:=18874368,parity:=15,classes:=142,raw:=3489792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=809),
rec(k:=13113,first:=1,last:=48,unitFirst:=600,unitLast:=647,order:=24576,autOrder:=786432,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1907),
rec(k:=13114,first:=1,last:=64,unitFirst:=648,unitLast:=711,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1612),
rec(k:=13115,first:=1,last:=569,unitFirst:=712,unitLast:=1280,order:=24576,autOrder:=12582912,parity:=15,classes:=569,raw:=13983744,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1234),
rec(k:=13116,first:=1,last:=128,unitFirst:=1281,unitLast:=1408,order:=24576,autOrder:=786432,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1199),
rec(k:=13117,first:=1,last:=48,unitFirst:=1409,unitLast:=1456,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1932),
rec(k:=13118,first:=1,last:=48,unitFirst:=1457,unitLast:=1504,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1492),
rec(k:=13119,first:=1,last:=32,unitFirst:=1505,unitLast:=1536,order:=24576,autOrder:=786432,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1410),
rec(k:=13120,first:=1,last:=194,unitFirst:=1537,unitLast:=1730,order:=24576,autOrder:=3145728,parity:=3,classes:=194,raw:=4767744,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2506),
rec(k:=13121,first:=1,last:=48,unitFirst:=1731,unitLast:=1778,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2148),
rec(k:=13122,first:=1,last:=53,unitFirst:=1779,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=3,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1955)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard157_v7_gpt56sol.g");
