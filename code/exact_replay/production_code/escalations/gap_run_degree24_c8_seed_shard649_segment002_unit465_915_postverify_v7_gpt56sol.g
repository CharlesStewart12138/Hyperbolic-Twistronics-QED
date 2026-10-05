# Exact wrapper for sealed degree-24 seed workload shard649.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD649_SEGMENT002_UNIT465_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=465;
INITIAL_COUNTERS:=[464,22806528,464,2,593920,564224,118784,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="8a4b7276cc2bcd256ff9e5656a548dc7837f2b1d915fff3b87b78513d3210ce0";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD649_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=345852;
PREVIOUS_OUTPUT_PREFIX_SHA256:="745ef00dac2ecc369816af224b13ae6c0624b94ca463f1ce379db247fbe37e4f";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD649_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD649_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard649_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B4C8E7C7F27730D48861439FA00C53B59DC4C89F353C28FEDBADCA0B77DE91F3";
S649_RECORDS:=[
rec(k:=15683,first:=30,last:=840,unitFirst:=1,unitLast:=811,order:=49152,autOrder:=786432,parity:=7,classes:=840,raw:=41287680,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1731),
rec(k:=15684,first:=1,last:=104,unitFirst:=812,unitLast:=915,order:=49152,autOrder:=393216,parity:=7,classes:=672,raw:=33030144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2359)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard649_v7_gpt56sol.g");
