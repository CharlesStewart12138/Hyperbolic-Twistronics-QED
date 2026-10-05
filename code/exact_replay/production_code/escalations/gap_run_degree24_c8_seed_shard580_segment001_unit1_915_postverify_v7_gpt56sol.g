# Exact wrapper for sealed degree-24 seed workload shard580.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD580_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD580_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD580_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard580_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="167A714070ADC119C8912B4200DA8879EC07BDEC85758B4DD64E19ECFEF2EF29";
S580_RECORDS:=[
rec(k:=15508,first:=63,last:=334,unitFirst:=1,unitLast:=272,order:=49152,autOrder:=3145728,parity:=7,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1987),
rec(k:=15509,first:=1,last:=348,unitFirst:=273,unitLast:=620,order:=49152,autOrder:=18874368,parity:=3,classes:=348,raw:=17104896,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2142),
rec(k:=15510,first:=1,last:=295,unitFirst:=621,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=341,raw:=16760832,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2808)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard580_v7_gpt56sol.g");
