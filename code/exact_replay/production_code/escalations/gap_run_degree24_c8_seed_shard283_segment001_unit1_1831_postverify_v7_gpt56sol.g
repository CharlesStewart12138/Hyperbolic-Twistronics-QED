# Exact wrapper for sealed degree-24 seed workload shard283.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD283_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD283_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD283_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard283_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2B59EC9C551EA92824B1717DE3D1E009073E4A32755619C3FCFF04A77410FDEA";
S283_RECORDS:=[
rec(k:=13873,first:=964,last:=1280,unitFirst:=1,unitLast:=317,order:=24576,autOrder:=393216,parity:=7,classes:=1280,raw:=31457280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2374),
rec(k:=13874,first:=1,last:=868,unitFirst:=318,unitLast:=1185,order:=24576,autOrder:=786432,parity:=7,classes:=868,raw:=21331968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2773),
rec(k:=13875,first:=1,last:=646,unitFirst:=1186,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=868,raw:=21331968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1782)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard283_v7_gpt56sol.g");
