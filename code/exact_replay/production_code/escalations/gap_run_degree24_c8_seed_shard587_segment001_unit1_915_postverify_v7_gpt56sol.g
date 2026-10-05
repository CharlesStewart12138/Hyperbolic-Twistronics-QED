# Exact wrapper for sealed degree-24 seed workload shard587.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD587_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD587_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD587_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard587_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CDAAF5A753C6F0611EEA908184037222757D9065C9894CAEC42A7F134E713BC0";
S587_RECORDS:=[
rec(k:=15534,first:=5,last:=48,unitFirst:=1,unitLast:=44,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1027),
rec(k:=15535,first:=1,last:=224,unitFirst:=45,unitLast:=268,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1429),
rec(k:=15536,first:=1,last:=160,unitFirst:=269,unitLast:=428,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1366),
rec(k:=15537,first:=1,last:=487,unitFirst:=429,unitLast:=915,order:=49152,autOrder:=3145728,parity:=31,classes:=944,raw:=46399488,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1752)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard587_v7_gpt56sol.g");
