# Exact wrapper for sealed degree-24 seed workload shard367.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD367_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD367_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD367_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard367_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3EE51B5FC2350636CB0F925C2C8D07C10582DE19108EA00B224E8E74A1AC6461";
S367_RECORDS:=[
rec(k:=14925,first:=117,last:=192,unitFirst:=1,unitLast:=76,order:=49152,autOrder:=3145728,parity:=1,classes:=192,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1311),
rec(k:=14926,first:=1,last:=582,unitFirst:=77,unitLast:=658,order:=49152,autOrder:=12582912,parity:=1,classes:=582,raw:=28606464,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1334),
rec(k:=14927,first:=1,last:=112,unitFirst:=659,unitLast:=770,order:=49152,autOrder:=6291456,parity:=1,classes:=112,raw:=5505024,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1182),
rec(k:=14928,first:=1,last:=145,unitFirst:=771,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=164,raw:=8060928,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1144)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard367_v7_gpt56sol.g");
