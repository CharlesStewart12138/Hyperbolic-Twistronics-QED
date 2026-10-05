# Exact wrapper for sealed degree-24 seed workload shard200.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD200_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD200_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD200_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard200_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3BD0C89296D4F44ECE657BCAA43A4132634E59B996D1A782A36DAB776E16D1C7";
S200_RECORDS:=[
rec(k:=13446,first:=244,last:=512,unitFirst:=1,unitLast:=269,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2487),
rec(k:=13447,first:=1,last:=724,unitFirst:=270,unitLast:=993,order:=24576,autOrder:=1572864,parity:=7,classes:=724,raw:=17793024,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1403),
rec(k:=13448,first:=1,last:=738,unitFirst:=994,unitLast:=1731,order:=24576,autOrder:=1572864,parity:=7,classes:=738,raw:=18137088,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1788),
rec(k:=13449,first:=1,last:=100,unitFirst:=1732,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1163)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard200_v7_gpt56sol.g");
