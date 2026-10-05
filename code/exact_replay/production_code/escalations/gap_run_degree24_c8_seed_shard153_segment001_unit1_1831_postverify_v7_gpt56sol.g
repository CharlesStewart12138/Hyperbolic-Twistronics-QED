# Exact wrapper for sealed degree-24 seed workload shard153.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD153_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD153_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD153_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard153_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B4C83C1EA9A1488EDC59BA7861213A56432ACC2056F3D1EEB2E69BFEA82A6D47";
S153_RECORDS:=[
rec(k:=13058,first:=943,last:=2288,unitFirst:=1,unitLast:=1346,order:=24576,autOrder:=25165824,parity:=3,classes:=2288,raw:=56229888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=7194),
rec(k:=13059,first:=1,last:=64,unitFirst:=1347,unitLast:=1410,order:=24576,autOrder:=786432,parity:=1,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1528),
rec(k:=13060,first:=1,last:=96,unitFirst:=1411,unitLast:=1506,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1342),
rec(k:=13061,first:=1,last:=144,unitFirst:=1507,unitLast:=1650,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1640),
rec(k:=13062,first:=1,last:=144,unitFirst:=1651,unitLast:=1794,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1227),
rec(k:=13063,first:=1,last:=37,unitFirst:=1795,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=3,classes:=239,raw:=5873664,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1914)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard153_v7_gpt56sol.g");
