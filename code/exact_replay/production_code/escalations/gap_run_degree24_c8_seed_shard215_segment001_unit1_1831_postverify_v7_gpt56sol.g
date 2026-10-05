# Exact wrapper for sealed degree-24 seed workload shard215.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD215_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD215_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD215_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard215_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5BE879E7CEE6DC97090A98D33C8F3CD09543E8ED91F3F6DD73E859B9D398A463";
S215_RECORDS:=[
rec(k:=13535,first:=318,last:=960,unitFirst:=1,unitLast:=643,order:=24576,autOrder:=1572864,parity:=7,classes:=960,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2740),
rec(k:=13536,first:=1,last:=208,unitFirst:=644,unitLast:=851,order:=24576,autOrder:=3145728,parity:=3,classes:=208,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2970),
rec(k:=13537,first:=1,last:=96,unitFirst:=852,unitLast:=947,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1578),
rec(k:=13538,first:=1,last:=96,unitFirst:=948,unitLast:=1043,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1482),
rec(k:=13539,first:=1,last:=144,unitFirst:=1044,unitLast:=1187,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1579),
rec(k:=13540,first:=1,last:=128,unitFirst:=1188,unitLast:=1315,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1312),
rec(k:=13541,first:=1,last:=424,unitFirst:=1316,unitLast:=1739,order:=24576,autOrder:=393216,parity:=3,classes:=424,raw:=10420224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1223),
rec(k:=13542,first:=1,last:=92,unitFirst:=1740,unitLast:=1831,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1118)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard215_v7_gpt56sol.g");
