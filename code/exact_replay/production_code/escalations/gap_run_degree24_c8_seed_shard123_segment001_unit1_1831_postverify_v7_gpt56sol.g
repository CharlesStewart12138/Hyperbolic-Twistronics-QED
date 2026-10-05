# Exact wrapper for sealed degree-24 seed workload shard123.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD123_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD123_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD123_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard123_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="FA436D919E61B26866C8C2A4DFC5112F452D21F0A660DDE0BB918EDDF8CCCF4A";
S123_RECORDS:=[
rec(k:=12731,first:=94,last:=148,unitFirst:=1,unitLast:=55,order:=24576,autOrder:=9437184,parity:=3,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1312),
rec(k:=12732,first:=1,last:=148,unitFirst:=56,unitLast:=203,order:=24576,autOrder:=9437184,parity:=15,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=770),
rec(k:=12734,first:=1,last:=174,unitFirst:=204,unitLast:=377,order:=24576,autOrder:=9437184,parity:=3,classes:=174,raw:=4276224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1244),
rec(k:=12735,first:=1,last:=174,unitFirst:=378,unitLast:=551,order:=24576,autOrder:=9437184,parity:=3,classes:=174,raw:=4276224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1409),
rec(k:=12736,first:=1,last:=72,unitFirst:=552,unitLast:=623,order:=24576,autOrder:=1572864,parity:=1,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1139),
rec(k:=12737,first:=1,last:=144,unitFirst:=624,unitLast:=767,order:=24576,autOrder:=1572864,parity:=1,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=727),
rec(k:=12738,first:=1,last:=120,unitFirst:=768,unitLast:=887,order:=24576,autOrder:=786432,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=770),
rec(k:=12739,first:=1,last:=24,unitFirst:=888,unitLast:=911,order:=24576,autOrder:=393216,parity:=15,classes:=24,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=839),
rec(k:=12740,first:=1,last:=48,unitFirst:=912,unitLast:=959,order:=24576,autOrder:=393216,parity:=15,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=817),
rec(k:=12741,first:=1,last:=108,unitFirst:=960,unitLast:=1067,order:=24576,autOrder:=786432,parity:=15,classes:=108,raw:=2654208,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=803),
rec(k:=12742,first:=1,last:=132,unitFirst:=1068,unitLast:=1199,order:=24576,autOrder:=786432,parity:=7,classes:=132,raw:=3244032,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1185),
rec(k:=12743,first:=1,last:=60,unitFirst:=1200,unitLast:=1259,order:=24576,autOrder:=393216,parity:=3,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1007),
rec(k:=12744,first:=1,last:=60,unitFirst:=1260,unitLast:=1319,order:=24576,autOrder:=393216,parity:=7,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1096),
rec(k:=12745,first:=1,last:=132,unitFirst:=1320,unitLast:=1451,order:=24576,autOrder:=786432,parity:=3,classes:=132,raw:=3244032,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1241),
rec(k:=12746,first:=1,last:=132,unitFirst:=1452,unitLast:=1583,order:=24576,autOrder:=786432,parity:=7,classes:=132,raw:=3244032,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1237),
rec(k:=12747,first:=1,last:=116,unitFirst:=1584,unitLast:=1699,order:=24576,autOrder:=786432,parity:=7,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1051),
rec(k:=12748,first:=1,last:=92,unitFirst:=1700,unitLast:=1791,order:=24576,autOrder:=393216,parity:=3,classes:=92,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=849),
rec(k:=12749,first:=1,last:=40,unitFirst:=1792,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=918)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard123_v7_gpt56sol.g");
