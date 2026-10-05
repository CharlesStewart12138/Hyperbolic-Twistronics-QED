# Exact wrapper for sealed degree-24 seed workload shard273.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD273_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD273_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD273_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard273_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8E14962467AB157FB9549C9F82C861B712EB1723357CDD4EE75D6297FE198346";
S273_RECORDS:=[
rec(k:=13804,first:=2,last:=428,unitFirst:=1,unitLast:=427,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1151),
rec(k:=13805,first:=1,last:=585,unitFirst:=428,unitLast:=1012,order:=24576,autOrder:=1572864,parity:=1,classes:=585,raw:=14376960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1221),
rec(k:=13806,first:=1,last:=500,unitFirst:=1013,unitLast:=1512,order:=24576,autOrder:=786432,parity:=1,classes:=500,raw:=12288000,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1006),
rec(k:=13807,first:=1,last:=319,unitFirst:=1513,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=1,classes:=585,raw:=14376960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1524)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard273_v7_gpt56sol.g");
