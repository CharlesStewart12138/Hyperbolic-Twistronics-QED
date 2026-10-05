# Exact wrapper for sealed degree-24 seed workload shard176.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD176_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD176_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD176_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard176_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="918EE29C6CBAB9D4C19558164189BBB7BF45959886E7FA5D949E05C678180915";
S176_RECORDS:=[
rec(k:=13281,first:=66,last:=120,unitFirst:=1,unitLast:=55,order:=24576,autOrder:=786432,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=875),
rec(k:=13282,first:=1,last:=176,unitFirst:=56,unitLast:=231,order:=24576,autOrder:=786432,parity:=15,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1143),
rec(k:=13283,first:=1,last:=212,unitFirst:=232,unitLast:=443,order:=24576,autOrder:=786432,parity:=15,classes:=212,raw:=5210112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1146),
rec(k:=13284,first:=1,last:=220,unitFirst:=444,unitLast:=663,order:=24576,autOrder:=786432,parity:=15,classes:=220,raw:=5406720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=976),
rec(k:=13285,first:=1,last:=132,unitFirst:=664,unitLast:=795,order:=24576,autOrder:=786432,parity:=7,classes:=132,raw:=3244032,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1285),
rec(k:=13286,first:=1,last:=172,unitFirst:=796,unitLast:=967,order:=24576,autOrder:=786432,parity:=7,classes:=172,raw:=4227072,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1244),
rec(k:=13287,first:=1,last:=168,unitFirst:=968,unitLast:=1135,order:=24576,autOrder:=786432,parity:=7,classes:=168,raw:=4128768,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1669),
rec(k:=13288,first:=1,last:=192,unitFirst:=1136,unitLast:=1327,order:=24576,autOrder:=786432,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1861),
rec(k:=13289,first:=1,last:=128,unitFirst:=1328,unitLast:=1455,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1902),
rec(k:=13290,first:=1,last:=376,unitFirst:=1456,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2115)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard176_v7_gpt56sol.g");
