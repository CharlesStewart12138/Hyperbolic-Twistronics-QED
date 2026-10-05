# Exact wrapper for sealed degree-24 seed workload shard280.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD280_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD280_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD280_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard280_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5950D89AF1CFFD24D36DD76A6CF33B046E4A05E15A4770D293C28C8B9405B030";
S280_RECORDS:=[
rec(k:=13851,first:=7,last:=352,unitFirst:=1,unitLast:=346,order:=24576,autOrder:=786432,parity:=7,classes:=352,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1887),
rec(k:=13852,first:=1,last:=128,unitFirst:=347,unitLast:=474,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1168),
rec(k:=13853,first:=1,last:=242,unitFirst:=475,unitLast:=716,order:=24576,autOrder:=393216,parity:=3,classes:=242,raw:=5947392,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1344),
rec(k:=13854,first:=1,last:=348,unitFirst:=717,unitLast:=1064,order:=24576,autOrder:=786432,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2057),
rec(k:=13855,first:=1,last:=144,unitFirst:=1065,unitLast:=1208,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2080),
rec(k:=13856,first:=1,last:=96,unitFirst:=1209,unitLast:=1304,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1467),
rec(k:=13857,first:=1,last:=352,unitFirst:=1305,unitLast:=1656,order:=24576,autOrder:=393216,parity:=3,classes:=352,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2550),
rec(k:=13858,first:=1,last:=175,unitFirst:=1657,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=452,raw:=11108352,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1581)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard280_v7_gpt56sol.g");
