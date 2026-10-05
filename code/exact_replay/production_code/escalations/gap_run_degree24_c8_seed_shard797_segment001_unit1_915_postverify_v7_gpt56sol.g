# Exact wrapper for sealed degree-24 seed workload shard797.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD797_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD797_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD797_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard797_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="EF4D557FBF2779982F4A9430898B6C61C56DFCC23A90E276DAA731D7D95AC765";
S797_RECORDS:=[
rec(k:=15873,first:=2,last:=128,unitFirst:=1,unitLast:=127,order:=49152,autOrder:=393216,parity:=3,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1409),
rec(k:=15874,first:=1,last:=128,unitFirst:=128,unitLast:=255,order:=49152,autOrder:=393216,parity:=3,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1453),
rec(k:=15875,first:=1,last:=140,unitFirst:=256,unitLast:=395,order:=49152,autOrder:=3145728,parity:=3,classes:=140,raw:=6881280,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1565),
rec(k:=15876,first:=1,last:=144,unitFirst:=396,unitLast:=539,order:=49152,autOrder:=3145728,parity:=3,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1634),
rec(k:=15877,first:=1,last:=368,unitFirst:=540,unitLast:=907,order:=49152,autOrder:=6291456,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3004),
rec(k:=15878,first:=1,last:=8,unitFirst:=908,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2508)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard797_v7_gpt56sol.g");
