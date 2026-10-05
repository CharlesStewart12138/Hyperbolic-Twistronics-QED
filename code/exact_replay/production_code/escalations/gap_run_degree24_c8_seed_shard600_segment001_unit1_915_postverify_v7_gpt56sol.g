# Exact wrapper for sealed degree-24 seed workload shard600.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD600_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD600_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD600_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard600_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3C1C0D33E5AF82DCCF7127B01F2FD3CB8A4209CBCC1200A650F89A362DB33C1C";
S600_RECORDS:=[
rec(k:=15566,first:=168,last:=240,unitFirst:=1,unitLast:=73,order:=49152,autOrder:=3145728,parity:=7,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2579),
rec(k:=15567,first:=1,last:=368,unitFirst:=74,unitLast:=441,order:=49152,autOrder:=3145728,parity:=7,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1924),
rec(k:=15568,first:=1,last:=474,unitFirst:=442,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=1370,raw:=67338240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3748)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard600_v7_gpt56sol.g");
