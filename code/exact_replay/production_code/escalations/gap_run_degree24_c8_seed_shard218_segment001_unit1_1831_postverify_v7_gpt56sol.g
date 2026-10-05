# Exact wrapper for sealed degree-24 seed workload shard218.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD218_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD218_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD218_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard218_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="605F9FBAE2BBCED04168E2A26C49ADC696CBFC3A21EB49457393FB1465A80A6D";
S218_RECORDS:=[
rec(k:=13552,first:=137,last:=512,unitFirst:=1,unitLast:=376,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1702),
rec(k:=13553,first:=1,last:=120,unitFirst:=377,unitLast:=496,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1404),
rec(k:=13554,first:=1,last:=520,unitFirst:=497,unitLast:=1016,order:=24576,autOrder:=786432,parity:=3,classes:=520,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1393),
rec(k:=13555,first:=1,last:=154,unitFirst:=1017,unitLast:=1170,order:=24576,autOrder:=786432,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1392),
rec(k:=13556,first:=1,last:=520,unitFirst:=1171,unitLast:=1690,order:=24576,autOrder:=786432,parity:=3,classes:=520,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1867),
rec(k:=13557,first:=1,last:=72,unitFirst:=1691,unitLast:=1762,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=972),
rec(k:=13558,first:=1,last:=69,unitFirst:=1763,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=520,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1323)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard218_v7_gpt56sol.g");
