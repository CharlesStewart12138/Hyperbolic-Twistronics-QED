# Exact wrapper for sealed degree-24 seed workload shard134.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD134_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD134_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD134_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard134_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8F223CC2CF48556B509DA6F00DC6EA176FD56C3E5D6F6F68AC9DB0C4B1DE1E37";
S134_RECORDS:=[
rec(k:=12909,first:=78,last:=128,unitFirst:=1,unitLast:=51,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1075),
rec(k:=12910,first:=1,last:=128,unitFirst:=52,unitLast:=179,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=901),
rec(k:=12911,first:=1,last:=104,unitFirst:=180,unitLast:=283,order:=24576,autOrder:=1572864,parity:=1,classes:=104,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=934),
rec(k:=12912,first:=1,last:=128,unitFirst:=284,unitLast:=411,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1292),
rec(k:=12913,first:=1,last:=128,unitFirst:=412,unitLast:=539,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1451),
rec(k:=12914,first:=1,last:=128,unitFirst:=540,unitLast:=667,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1252),
rec(k:=12915,first:=1,last:=128,unitFirst:=668,unitLast:=795,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1623),
rec(k:=12916,first:=1,last:=128,unitFirst:=796,unitLast:=923,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1482),
rec(k:=12917,first:=1,last:=128,unitFirst:=924,unitLast:=1051,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1686),
rec(k:=12918,first:=1,last:=128,unitFirst:=1052,unitLast:=1179,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1377),
rec(k:=12919,first:=1,last:=344,unitFirst:=1180,unitLast:=1523,order:=24576,autOrder:=786432,parity:=15,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2232),
rec(k:=12920,first:=1,last:=116,unitFirst:=1524,unitLast:=1639,order:=24576,autOrder:=786432,parity:=3,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1492),
rec(k:=12921,first:=1,last:=128,unitFirst:=1640,unitLast:=1767,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=945),
rec(k:=12922,first:=1,last:=64,unitFirst:=1768,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=1,classes:=277,raw:=6807552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=866)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard134_v7_gpt56sol.g");
