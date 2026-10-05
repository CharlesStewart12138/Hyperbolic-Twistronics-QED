# Exact wrapper for sealed degree-24 seed workload shard882.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD882_SEGMENT002_UNIT293_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=293;
INITIAL_COUNTERS:=[292,14352384,292,6,376320,226816,61184,21120,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="6d70f42953fac5eb0503d8e48b0e7e0c45bd470d961c3866470095797e6ebbb6";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD882_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=219049;
PREVIOUS_OUTPUT_PREFIX_SHA256:="3020cc8657c11fecceec4d423d1b0a1a570b6311d1b5f031e7de0c9a3e299ca3";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD882_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD882_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard882_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="24D3DBE4B835EBCD0DCD8166B3A2F97E02FA0B43801CB3B03AC37E5EE71F4945";
S882_RECORDS:=[
rec(k:=15946,first:=847,last:=952,unitFirst:=1,unitLast:=106,order:=49152,autOrder:=1572864,parity:=3,classes:=952,raw:=46792704,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2097),
rec(k:=15947,first:=1,last:=672,unitFirst:=107,unitLast:=778,order:=49152,autOrder:=786432,parity:=3,classes:=672,raw:=33030144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1689),
rec(k:=15948,first:=1,last:=137,unitFirst:=779,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=952,raw:=46792704,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1299)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard882_v7_gpt56sol.g");
