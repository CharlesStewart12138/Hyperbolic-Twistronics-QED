# Exact wrapper for sealed degree-24 seed workload shard392.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD392_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD392_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD392_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard392_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9A4B5567A78506FCCBD84ECB22D6B04AC43FDE82DC42F42EB859284B0DED0A70";
S392_RECORDS:=[
rec(k:=15015,first:=150,last:=224,unitFirst:=1,unitLast:=75,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2534),
rec(k:=15016,first:=1,last:=334,unitFirst:=76,unitLast:=409,order:=49152,autOrder:=3145728,parity:=7,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1988),
rec(k:=15017,first:=1,last:=370,unitFirst:=410,unitLast:=779,order:=49152,autOrder:=3145728,parity:=3,classes:=370,raw:=18186240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2420),
rec(k:=15018,first:=1,last:=136,unitFirst:=780,unitLast:=915,order:=49152,autOrder:=9437184,parity:=7,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1615)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard392_v7_gpt56sol.g");
