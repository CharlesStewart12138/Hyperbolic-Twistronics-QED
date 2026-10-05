# Exact wrapper for sealed degree-24 seed workload shard602.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD602_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD602_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD602_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard602_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="39AD3E5B5083967CB1CC3DEF3C6239B5F5373AEDA9CC43C71CFB082E10F9B2CE";
S602_RECORDS:=[
rec(k:=15569,first:=20,last:=64,unitFirst:=1,unitLast:=45,order:=49152,autOrder:=1572864,parity:=7,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1968),
rec(k:=15570,first:=1,last:=840,unitFirst:=46,unitLast:=885,order:=49152,autOrder:=1572864,parity:=7,classes:=840,raw:=41287680,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2440),
rec(k:=15571,first:=1,last:=30,unitFirst:=886,unitLast:=915,order:=49152,autOrder:=393216,parity:=7,classes:=40,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=917)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard602_v7_gpt56sol.g");
