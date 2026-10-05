# Exact wrapper for sealed degree-24 seed workload shard266.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD266_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD266_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD266_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard266_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BBD54302EE9439551A1529C3A6EDBEC06FDF76873A8F93F18BA7117F2569F9D2";
S266_RECORDS:=[
rec(k:=13789,first:=479,last:=784,unitFirst:=1,unitLast:=306,order:=24576,autOrder:=603979776,parity:=1,classes:=784,raw:=19267584,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=12511),
rec(k:=13790,first:=1,last:=72,unitFirst:=307,unitLast:=378,order:=24576,autOrder:=1572864,parity:=1,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1128),
rec(k:=13791,first:=1,last:=1232,unitFirst:=379,unitLast:=1610,order:=24576,autOrder:=201326592,parity:=1,classes:=1232,raw:=30277632,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=29321),
rec(k:=13792,first:=1,last:=221,unitFirst:=1611,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=1,classes:=991,raw:=24354816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2669)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard266_v7_gpt56sol.g");
