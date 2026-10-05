# Exact wrapper for sealed degree-24 seed workload shard152.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD152_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD152_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD152_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard152_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5707FC6E29CB2C6B3A86217F8D9B0703454397BD5599CDB09DDE7D0FCD4C3ED7";
S152_RECORDS:=[
rec(k:=13056,first:=59,last:=600,unitFirst:=1,unitLast:=542,order:=24576,autOrder:=786432,parity:=7,classes:=600,raw:=14745600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1768),
rec(k:=13057,first:=1,last:=347,unitFirst:=543,unitLast:=889,order:=24576,autOrder:=6291456,parity:=1,classes:=347,raw:=8527872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1927),
rec(k:=13058,first:=1,last:=942,unitFirst:=890,unitLast:=1831,order:=24576,autOrder:=25165824,parity:=3,classes:=2288,raw:=56229888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=7194)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard152_v7_gpt56sol.g");
