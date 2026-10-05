# Exact wrapper for sealed degree-24 seed workload shard202.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD202_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD202_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD202_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard202_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="501FEC99A391EF081358C857682FD7CD5824643D04D89FDFE3AF85B585BBB91E";
S202_RECORDS:=[
rec(k:=13454,first:=785,last:=1360,unitFirst:=1,unitLast:=576,order:=24576,autOrder:=6291456,parity:=7,classes:=1360,raw:=33423360,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2416),
rec(k:=13455,first:=1,last:=76,unitFirst:=577,unitLast:=652,order:=24576,autOrder:=786432,parity:=3,classes:=76,raw:=1867776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1353),
rec(k:=13457,first:=1,last:=188,unitFirst:=653,unitLast:=840,order:=24576,autOrder:=3145728,parity:=3,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1573),
rec(k:=13459,first:=1,last:=140,unitFirst:=841,unitLast:=980,order:=24576,autOrder:=1572864,parity:=7,classes:=140,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1861),
rec(k:=13460,first:=1,last:=640,unitFirst:=981,unitLast:=1620,order:=24576,autOrder:=1572864,parity:=3,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2748),
rec(k:=13461,first:=1,last:=148,unitFirst:=1621,unitLast:=1768,order:=24576,autOrder:=393216,parity:=3,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1023),
rec(k:=13462,first:=1,last:=63,unitFirst:=1769,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1295)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard202_v7_gpt56sol.g");
