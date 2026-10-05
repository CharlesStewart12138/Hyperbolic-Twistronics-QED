# Exact wrapper for sealed degree-24 seed workload shard338.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD338_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD338_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD338_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard338_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="016101CED84C20DBA0656D3CE408BB732E50ECB82BF99EF6E12B13270F397C42";
S338_RECORDS:=[
rec(k:=14799,first:=352,last:=446,unitFirst:=1,unitLast:=95,order:=49152,autOrder:=6291456,parity:=1,classes:=446,raw:=21921792,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2295),
rec(k:=14800,first:=1,last:=422,unitFirst:=96,unitLast:=517,order:=49152,autOrder:=6291456,parity:=1,classes:=422,raw:=20742144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2582),
rec(k:=14801,first:=1,last:=224,unitFirst:=518,unitLast:=741,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1607),
rec(k:=14802,first:=1,last:=174,unitFirst:=742,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3189)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard338_v7_gpt56sol.g");
