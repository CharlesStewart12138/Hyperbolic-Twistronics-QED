# Exact wrapper for sealed degree-24 seed workload shard211.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD211_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD211_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD211_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard211_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="34E0B55478F0E815DE1C3D97E39AE3F42CEA542A5459D6A3AB6923C25C052306";
S211_RECORDS:=[
rec(k:=13512,first:=28,last:=640,unitFirst:=1,unitLast:=613,order:=24576,autOrder:=393216,parity:=3,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1301),
rec(k:=13513,first:=1,last:=148,unitFirst:=614,unitLast:=761,order:=24576,autOrder:=786432,parity:=7,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1465),
rec(k:=13514,first:=1,last:=112,unitFirst:=762,unitLast:=873,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1421),
rec(k:=13515,first:=1,last:=540,unitFirst:=874,unitLast:=1413,order:=24576,autOrder:=786432,parity:=7,classes:=540,raw:=13271040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1289),
rec(k:=13516,first:=1,last:=88,unitFirst:=1414,unitLast:=1501,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1051),
rec(k:=13517,first:=1,last:=330,unitFirst:=1502,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=480,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1369)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard211_v7_gpt56sol.g");
