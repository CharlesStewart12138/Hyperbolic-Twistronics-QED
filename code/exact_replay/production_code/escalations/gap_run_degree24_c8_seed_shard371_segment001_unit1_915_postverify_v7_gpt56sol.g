# Exact wrapper for sealed degree-24 seed workload shard371.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD371_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD371_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD371_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard371_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7736FBBCD170DE7AC44D533C939BF3CE28F856A7C110DDCE1316C3548656A45F";
S371_RECORDS:=[
rec(k:=14935,first:=215,last:=416,unitFirst:=1,unitLast:=202,order:=49152,autOrder:=3145728,parity:=3,classes:=416,raw:=20447232,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2110),
rec(k:=14936,first:=1,last:=320,unitFirst:=203,unitLast:=522,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1155),
rec(k:=14937,first:=1,last:=96,unitFirst:=523,unitLast:=618,order:=49152,autOrder:=786432,parity:=1,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1071),
rec(k:=14938,first:=1,last:=272,unitFirst:=619,unitLast:=890,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=5428),
rec(k:=14939,first:=1,last:=25,unitFirst:=891,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2246)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard371_v7_gpt56sol.g");
