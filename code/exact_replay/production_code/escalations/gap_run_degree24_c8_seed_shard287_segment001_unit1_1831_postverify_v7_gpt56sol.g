# Exact wrapper for sealed degree-24 seed workload shard287.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD287_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD287_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD287_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard287_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="34E23855AB6D329BE69B57E6944D52CF21AF5986A66EDEBD58EB092C691A1B98";
S287_RECORDS:=[
rec(k:=13889,first:=409,last:=1344,unitFirst:=1,unitLast:=936,order:=24576,autOrder:=50331648,parity:=7,classes:=1344,raw:=33030144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=19176),
rec(k:=13890,first:=1,last:=340,unitFirst:=937,unitLast:=1276,order:=24576,autOrder:=393216,parity:=3,classes:=340,raw:=8355840,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=973),
rec(k:=13891,first:=1,last:=340,unitFirst:=1277,unitLast:=1616,order:=24576,autOrder:=393216,parity:=3,classes:=340,raw:=8355840,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1116),
rec(k:=13892,first:=1,last:=215,unitFirst:=1617,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1164)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard287_v7_gpt56sol.g");
