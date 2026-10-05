# Exact wrapper for sealed degree-24 seed workload shard184.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD184_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD184_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD184_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard184_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="16223043E7C33EEA18A16587D6365D04D851D190948FC38F0C22327342F2B057";
S184_RECORDS:=[
rec(k:=13355,first:=61,last:=525,unitFirst:=1,unitLast:=465,order:=24576,autOrder:=9437184,parity:=7,classes:=525,raw:=12902400,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2135),
rec(k:=13356,first:=1,last:=154,unitFirst:=466,unitLast:=619,order:=24576,autOrder:=786432,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1121),
rec(k:=13357,first:=1,last:=60,unitFirst:=620,unitLast:=679,order:=24576,autOrder:=2359296,parity:=3,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1117),
rec(k:=13358,first:=1,last:=96,unitFirst:=680,unitLast:=775,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1387),
rec(k:=13359,first:=1,last:=64,unitFirst:=776,unitLast:=839,order:=24576,autOrder:=1179648,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1373),
rec(k:=13360,first:=1,last:=128,unitFirst:=840,unitLast:=967,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2440),
rec(k:=13361,first:=1,last:=162,unitFirst:=968,unitLast:=1129,order:=24576,autOrder:=4718592,parity:=7,classes:=162,raw:=3981312,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1075),
rec(k:=13362,first:=1,last:=158,unitFirst:=1130,unitLast:=1287,order:=24576,autOrder:=786432,parity:=3,classes:=158,raw:=3883008,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1823),
rec(k:=13363,first:=1,last:=126,unitFirst:=1288,unitLast:=1413,order:=24576,autOrder:=4718592,parity:=7,classes:=126,raw:=3096576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1080),
rec(k:=13364,first:=1,last:=206,unitFirst:=1414,unitLast:=1619,order:=24576,autOrder:=786432,parity:=3,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1939),
rec(k:=13365,first:=1,last:=212,unitFirst:=1620,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=290,raw:=7127040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1617)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard184_v7_gpt56sol.g");
