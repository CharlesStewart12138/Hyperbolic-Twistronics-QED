# Exact wrapper for sealed degree-24 seed workload shard306.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD306_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD306_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD306_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard306_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A02FB35FDF5A4F81476CE1F29723E684B5B3D084B3D74756513AD609967E8866";
S306_RECORDS:=[
rec(k:=13952,first:=1760,last:=2048,unitFirst:=1,unitLast:=289,order:=24576,autOrder:=1572864,parity:=7,classes:=2048,raw:=50331648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=5746),
rec(k:=13953,first:=1,last:=1024,unitFirst:=290,unitLast:=1313,order:=24576,autOrder:=1572864,parity:=7,classes:=1024,raw:=25165824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4032),
rec(k:=13954,first:=1,last:=518,unitFirst:=1314,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=1024,raw:=25165824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4260)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard306_v7_gpt56sol.g");
