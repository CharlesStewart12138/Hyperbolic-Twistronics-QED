# Exact wrapper for sealed degree-24 seed workload shard264.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD264_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD264_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD264_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard264_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="469253BC65FA95E0AA522B2D08601CECED815CF4F45E8D9963DF1BC9CD806061";
S264_RECORDS:=[
rec(k:=13783,first:=1593,last:=1784,unitFirst:=1,unitLast:=192,order:=24576,autOrder:=6291456,parity:=1,classes:=1784,raw:=43843584,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3443),
rec(k:=13784,first:=1,last:=832,unitFirst:=193,unitLast:=1024,order:=24576,autOrder:=1572864,parity:=1,classes:=832,raw:=20447232,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2853),
rec(k:=13785,first:=1,last:=807,unitFirst:=1025,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=1,classes:=1784,raw:=43843584,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3046)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard264_v7_gpt56sol.g");
