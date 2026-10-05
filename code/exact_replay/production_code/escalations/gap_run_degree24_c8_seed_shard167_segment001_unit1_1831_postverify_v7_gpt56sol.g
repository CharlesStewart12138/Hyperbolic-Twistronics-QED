# Exact wrapper for sealed degree-24 seed workload shard167.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD167_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD167_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD167_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard167_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5FECE5DDF78D68B9DCF6C60C186E1DA38F57EF5AA6B89F1EFC94F85B35858A6E";
S167_RECORDS:=[
rec(k:=13184,first:=201,last:=376,unitFirst:=1,unitLast:=176,order:=24576,autOrder:=786432,parity:=15,classes:=376,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2073),
rec(k:=13185,first:=1,last:=848,unitFirst:=177,unitLast:=1024,order:=24576,autOrder:=1572864,parity:=15,classes:=848,raw:=20840448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3125),
rec(k:=13186,first:=1,last:=144,unitFirst:=1025,unitLast:=1168,order:=24576,autOrder:=786432,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2221),
rec(k:=13187,first:=1,last:=352,unitFirst:=1169,unitLast:=1520,order:=24576,autOrder:=786432,parity:=7,classes:=352,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1746),
rec(k:=13188,first:=1,last:=128,unitFirst:=1521,unitLast:=1648,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1321),
rec(k:=13189,first:=1,last:=72,unitFirst:=1649,unitLast:=1720,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1122),
rec(k:=13190,first:=1,last:=111,unitFirst:=1721,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=530,raw:=13025280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2022)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard167_v7_gpt56sol.g");
