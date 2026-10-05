# Exact wrapper for sealed degree-24 seed workload shard606.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD606_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD606_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD606_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard606_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="999505984175E67B254CB2C0468FDAAB79C6EB5F2D30217C7B56ED46BF4DF697";
S606_RECORDS:=[
rec(k:=15577,first:=124,last:=898,unitFirst:=1,unitLast:=775,order:=49152,autOrder:=12582912,parity:=1,classes:=898,raw:=44138496,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2361),
rec(k:=15578,first:=1,last:=120,unitFirst:=776,unitLast:=895,order:=49152,autOrder:=3145728,parity:=1,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1667),
rec(k:=15579,first:=1,last:=20,unitFirst:=896,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=172,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1707)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard606_v7_gpt56sol.g");
