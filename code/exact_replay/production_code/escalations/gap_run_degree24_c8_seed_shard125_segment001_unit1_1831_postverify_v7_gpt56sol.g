# Exact wrapper for sealed degree-24 seed workload shard125.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD125_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD125_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD125_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard125_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="667001195A35A9E8AD9F8E319C8DF1B4D8A55BED237F4BCD9E4717EB011F4B16";
S125_RECORDS:=[
rec(k:=12765,first:=50,last:=240,unitFirst:=1,unitLast:=191,order:=24576,autOrder:=1572864,parity:=7,classes:=240,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1591),
rec(k:=12766,first:=1,last:=140,unitFirst:=192,unitLast:=331,order:=24576,autOrder:=1572864,parity:=7,classes:=140,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=906),
rec(k:=12768,first:=1,last:=128,unitFirst:=332,unitLast:=459,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1361),
rec(k:=12769,first:=1,last:=128,unitFirst:=460,unitLast:=587,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1148),
rec(k:=12770,first:=1,last:=96,unitFirst:=588,unitLast:=683,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1183),
rec(k:=12771,first:=1,last:=96,unitFirst:=684,unitLast:=779,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=849),
rec(k:=12772,first:=1,last:=180,unitFirst:=780,unitLast:=959,order:=24576,autOrder:=1572864,parity:=7,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1163),
rec(k:=12773,first:=1,last:=226,unitFirst:=960,unitLast:=1185,order:=24576,autOrder:=1572864,parity:=7,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1539),
rec(k:=12774,first:=1,last:=24,unitFirst:=1186,unitLast:=1209,order:=24576,autOrder:=1179648,parity:=15,classes:=24,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=580),
rec(k:=12775,first:=1,last:=44,unitFirst:=1210,unitLast:=1253,order:=24576,autOrder:=393216,parity:=7,classes:=44,raw:=1081344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=751),
rec(k:=12776,first:=1,last:=44,unitFirst:=1254,unitLast:=1297,order:=24576,autOrder:=393216,parity:=7,classes:=44,raw:=1081344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=814),
rec(k:=12777,first:=1,last:=88,unitFirst:=1298,unitLast:=1385,order:=24576,autOrder:=393216,parity:=7,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=818),
rec(k:=12778,first:=1,last:=80,unitFirst:=1386,unitLast:=1465,order:=24576,autOrder:=393216,parity:=7,classes:=80,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=799),
rec(k:=12779,first:=1,last:=68,unitFirst:=1466,unitLast:=1533,order:=24576,autOrder:=393216,parity:=7,classes:=68,raw:=1671168,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=691),
rec(k:=12780,first:=1,last:=112,unitFirst:=1534,unitLast:=1645,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1947),
rec(k:=12781,first:=1,last:=96,unitFirst:=1646,unitLast:=1741,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=769),
rec(k:=12782,first:=1,last:=90,unitFirst:=1742,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1567)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard125_v7_gpt56sol.g");
