# Exact wrapper for sealed degree-24 seed workload shard286.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD286_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD286_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD286_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard286_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="738BC6683DA9B5D7593DC6743962266E319037ADCE7080F0DE42EC58446375F4";
S286_RECORDS:=[
rec(k:=13885,first:=118,last:=292,unitFirst:=1,unitLast:=175,order:=24576,autOrder:=196608,parity:=3,classes:=292,raw:=7176192,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=853),
rec(k:=13886,first:=1,last:=96,unitFirst:=176,unitLast:=271,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=714),
rec(k:=13887,first:=1,last:=754,unitFirst:=272,unitLast:=1025,order:=24576,autOrder:=786432,parity:=7,classes:=754,raw:=18530304,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1534),
rec(k:=13888,first:=1,last:=398,unitFirst:=1026,unitLast:=1423,order:=24576,autOrder:=25165824,parity:=15,classes:=398,raw:=9781248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1826),
rec(k:=13889,first:=1,last:=408,unitFirst:=1424,unitLast:=1831,order:=24576,autOrder:=50331648,parity:=7,classes:=1344,raw:=33030144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=19176)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard286_v7_gpt56sol.g");
