# Exact wrapper for sealed degree-24 seed workload shard289.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD289_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD289_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD289_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard289_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="4AAC6E17673E1F713C3D958FE0A74E8F59220F7F35CA87B2D437B993912142BE";
S289_RECORDS:=[
rec(k:=13898,first:=185,last:=754,unitFirst:=1,unitLast:=570,order:=24576,autOrder:=786432,parity:=7,classes:=754,raw:=18530304,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1379),
rec(k:=13899,first:=1,last:=96,unitFirst:=571,unitLast:=666,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=955),
rec(k:=13900,first:=1,last:=440,unitFirst:=667,unitLast:=1106,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=994),
rec(k:=13901,first:=1,last:=96,unitFirst:=1107,unitLast:=1202,order:=24576,autOrder:=25165824,parity:=7,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=32489),
rec(k:=13902,first:=1,last:=629,unitFirst:=1203,unitLast:=1831,order:=24576,autOrder:=50331648,parity:=7,classes:=1368,raw:=33619968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=16457)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard289_v7_gpt56sol.g");
