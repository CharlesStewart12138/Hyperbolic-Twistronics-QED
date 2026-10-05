# Exact wrapper for sealed degree-24 seed workload shard155.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD155_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD155_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD155_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard155_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="57131571E2DEBC27F6C7743DEDF645E433C96A7F674D1DA52E460E3A7A06BA7B";
S155_RECORDS:=[
rec(k:=13075,first:=7,last:=384,unitFirst:=1,unitLast:=378,order:=24576,autOrder:=393216,parity:=15,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1854),
rec(k:=13076,first:=1,last:=72,unitFirst:=379,unitLast:=450,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1118),
rec(k:=13077,first:=1,last:=40,unitFirst:=451,unitLast:=490,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=675),
rec(k:=13078,first:=1,last:=128,unitFirst:=491,unitLast:=618,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1474),
rec(k:=13079,first:=1,last:=140,unitFirst:=619,unitLast:=758,order:=24576,autOrder:=393216,parity:=7,classes:=140,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1931),
rec(k:=13080,first:=1,last:=120,unitFirst:=759,unitLast:=878,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1846),
rec(k:=13081,first:=1,last:=472,unitFirst:=879,unitLast:=1350,order:=24576,autOrder:=786432,parity:=15,classes:=472,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1803),
rec(k:=13082,first:=1,last:=230,unitFirst:=1351,unitLast:=1580,order:=24576,autOrder:=786432,parity:=7,classes:=230,raw:=5652480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1230),
rec(k:=13083,first:=1,last:=16,unitFirst:=1581,unitLast:=1596,order:=24576,autOrder:=196608,parity:=15,classes:=16,raw:=393216,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=766),
rec(k:=13084,first:=1,last:=16,unitFirst:=1597,unitLast:=1612,order:=24576,autOrder:=196608,parity:=7,classes:=16,raw:=393216,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=646),
rec(k:=13085,first:=1,last:=24,unitFirst:=1613,unitLast:=1636,order:=24576,autOrder:=1179648,parity:=15,classes:=24,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=710),
rec(k:=13086,first:=1,last:=44,unitFirst:=1637,unitLast:=1680,order:=24576,autOrder:=393216,parity:=7,classes:=44,raw:=1081344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=758),
rec(k:=13087,first:=1,last:=144,unitFirst:=1681,unitLast:=1824,order:=24576,autOrder:=196608,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1182),
rec(k:=13088,first:=1,last:=7,unitFirst:=1825,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1243)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard155_v7_gpt56sol.g");
