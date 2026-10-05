# Exact wrapper for sealed degree-24 seed workload shard165.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD165_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD165_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD165_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard165_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="FE3A6AC3D42C3B8D30F6F817F0FE9A9ECC7A3BF695084A5A8F96CBB2CBB74476";
S165_RECORDS:=[
rec(k:=13171,first:=162,last:=470,unitFirst:=1,unitLast:=309,order:=24576,autOrder:=786432,parity:=3,classes:=470,raw:=11550720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2082),
rec(k:=13172,first:=1,last:=44,unitFirst:=310,unitLast:=353,order:=24576,autOrder:=393216,parity:=3,classes:=44,raw:=1081344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1735),
rec(k:=13173,first:=1,last:=64,unitFirst:=354,unitLast:=417,order:=24576,autOrder:=786432,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1428),
rec(k:=13174,first:=1,last:=136,unitFirst:=418,unitLast:=553,order:=24576,autOrder:=786432,parity:=3,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1794),
rec(k:=13175,first:=1,last:=184,unitFirst:=554,unitLast:=737,order:=24576,autOrder:=1572864,parity:=3,classes:=184,raw:=4521984,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1858),
rec(k:=13176,first:=1,last:=685,unitFirst:=738,unitLast:=1422,order:=24576,autOrder:=1572864,parity:=3,classes:=685,raw:=16834560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2654),
rec(k:=13177,first:=1,last:=128,unitFirst:=1423,unitLast:=1550,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2065),
rec(k:=13178,first:=1,last:=281,unitFirst:=1551,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2387)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard165_v7_gpt56sol.g");
