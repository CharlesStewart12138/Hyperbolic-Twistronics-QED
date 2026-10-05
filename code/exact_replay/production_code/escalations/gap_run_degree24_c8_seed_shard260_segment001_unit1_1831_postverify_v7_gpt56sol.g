# Exact wrapper for sealed degree-24 seed workload shard260.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD260_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD260_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD260_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard260_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="10EDFE64236D26B634A53E4EB2B808D9BFA2F2CAD6E353764B69F24145905BF2";
S260_RECORDS:=[
rec(k:=13773,first:=251,last:=800,unitFirst:=1,unitLast:=550,order:=24576,autOrder:=393216,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1856),
rec(k:=13774,first:=1,last:=800,unitFirst:=551,unitLast:=1350,order:=24576,autOrder:=393216,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1767),
rec(k:=13775,first:=1,last:=481,unitFirst:=1351,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1922)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard260_v7_gpt56sol.g");
