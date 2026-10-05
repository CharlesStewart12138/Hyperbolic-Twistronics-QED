# Exact wrapper for sealed degree-24 seed workload shard191.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD191_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD191_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD191_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard191_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E1BC2F2CD29A8F066B4D4DB0D80C62323830791C924400169DA95C602A7D8850";
S191_RECORDS:=[
rec(k:=13402,first:=267,last:=328,unitFirst:=1,unitLast:=62,order:=24576,autOrder:=786432,parity:=7,classes:=328,raw:=8060928,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1183),
rec(k:=13403,first:=1,last:=128,unitFirst:=63,unitLast:=190,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1567),
rec(k:=13404,first:=1,last:=128,unitFirst:=191,unitLast:=318,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1485),
rec(k:=13405,first:=1,last:=128,unitFirst:=319,unitLast:=446,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1456),
rec(k:=13406,first:=1,last:=180,unitFirst:=447,unitLast:=626,order:=24576,autOrder:=1572864,parity:=7,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1553),
rec(k:=13407,first:=1,last:=576,unitFirst:=627,unitLast:=1202,order:=24576,autOrder:=393216,parity:=7,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1691),
rec(k:=13408,first:=1,last:=629,unitFirst:=1203,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=816,raw:=20054016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2431)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard191_v7_gpt56sol.g");
