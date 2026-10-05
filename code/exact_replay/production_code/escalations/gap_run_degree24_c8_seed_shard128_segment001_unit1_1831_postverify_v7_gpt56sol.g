# Exact wrapper for sealed degree-24 seed workload shard128.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD128_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD128_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD128_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard128_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2C123DEFD21A1359F55B100384D4F3CD32333ADF5797B1F1516DEAB54DA3B8A4";
S128_RECORDS:=[
rec(k:=12809,first:=61,last:=88,unitFirst:=1,unitLast:=28,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=920),
rec(k:=12810,first:=1,last:=96,unitFirst:=29,unitLast:=124,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1499),
rec(k:=12811,first:=1,last:=72,unitFirst:=125,unitLast:=196,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=836),
rec(k:=12812,first:=1,last:=64,unitFirst:=197,unitLast:=260,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1294),
rec(k:=12813,first:=1,last:=72,unitFirst:=261,unitLast:=332,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=987),
rec(k:=12814,first:=1,last:=403,unitFirst:=333,unitLast:=735,order:=24576,autOrder:=12582912,parity:=15,classes:=403,raw:=9904128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2177),
rec(k:=12815,first:=1,last:=200,unitFirst:=736,unitLast:=935,order:=24576,autOrder:=6291456,parity:=3,classes:=200,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1533),
rec(k:=12816,first:=1,last:=188,unitFirst:=936,unitLast:=1123,order:=24576,autOrder:=3145728,parity:=15,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2251),
rec(k:=12817,first:=1,last:=188,unitFirst:=1124,unitLast:=1311,order:=24576,autOrder:=3145728,parity:=3,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1212),
rec(k:=12818,first:=1,last:=32,unitFirst:=1312,unitLast:=1343,order:=24576,autOrder:=786432,parity:=7,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1076),
rec(k:=12819,first:=1,last:=32,unitFirst:=1344,unitLast:=1375,order:=24576,autOrder:=786432,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1029),
rec(k:=12821,first:=1,last:=136,unitFirst:=1376,unitLast:=1511,order:=24576,autOrder:=786432,parity:=3,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1266),
rec(k:=12822,first:=1,last:=76,unitFirst:=1512,unitLast:=1587,order:=24576,autOrder:=786432,parity:=3,classes:=76,raw:=1867776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=848),
rec(k:=12823,first:=1,last:=120,unitFirst:=1588,unitLast:=1707,order:=24576,autOrder:=9437184,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1395),
rec(k:=12824,first:=1,last:=40,unitFirst:=1708,unitLast:=1747,order:=24576,autOrder:=393216,parity:=7,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=712),
rec(k:=12825,first:=1,last:=64,unitFirst:=1748,unitLast:=1811,order:=24576,autOrder:=786432,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1164),
rec(k:=12826,first:=1,last:=20,unitFirst:=1812,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=653)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard128_v7_gpt56sol.g");
