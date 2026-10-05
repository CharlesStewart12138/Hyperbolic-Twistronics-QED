# Exact wrapper for sealed degree-24 seed workload shard594.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD594_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD594_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD594_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard594_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BACD8AA7513610C8B27DA9802E1ACF8FECFFBC9AD331D22780074ECB0EACAE59";
S594_RECORDS:=[
rec(k:=15552,first:=998,last:=1120,unitFirst:=1,unitLast:=123,order:=49152,autOrder:=1572864,parity:=31,classes:=1120,raw:=55050240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2178),
rec(k:=15553,first:=1,last:=256,unitFirst:=124,unitLast:=379,order:=49152,autOrder:=786432,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1496),
rec(k:=15554,first:=1,last:=144,unitFirst:=380,unitLast:=523,order:=49152,autOrder:=786432,parity:=7,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1768),
rec(k:=15555,first:=1,last:=392,unitFirst:=524,unitLast:=915,order:=49152,autOrder:=4718592,parity:=31,classes:=860,raw:=42270720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2983)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard594_v7_gpt56sol.g");
