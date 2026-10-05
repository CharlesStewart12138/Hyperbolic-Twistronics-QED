# Exact wrapper for sealed degree-24 seed workload shard558.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD558_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD558_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD558_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard558_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="AF6F4EFAB74A8785FF565308D26CC92568A1A6C449C7CF010B729985B9309891";
S558_RECORDS:=[
rec(k:=15432,first:=306,last:=484,unitFirst:=1,unitLast:=179,order:=49152,autOrder:=3145728,parity:=3,classes:=484,raw:=23789568,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1644),
rec(k:=15433,first:=1,last:=376,unitFirst:=180,unitLast:=555,order:=49152,autOrder:=6291456,parity:=1,classes:=376,raw:=18481152,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2183),
rec(k:=15434,first:=1,last:=360,unitFirst:=556,unitLast:=915,order:=49152,autOrder:=6291456,parity:=7,classes:=370,raw:=18186240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1509)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard558_v7_gpt56sol.g");
