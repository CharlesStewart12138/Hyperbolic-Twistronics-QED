# Exact wrapper for sealed degree-24 seed workload shard448.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD448_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD448_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD448_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard448_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3AEA79F17F54AEE789CD20804E38BCCFF49B011BEF4FE125578D043C7583C94F";
S448_RECORDS:=[
rec(k:=15167,first:=174,last:=288,unitFirst:=1,unitLast:=115,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1562),
rec(k:=15168,first:=1,last:=282,unitFirst:=116,unitLast:=397,order:=49152,autOrder:=6291456,parity:=3,classes:=282,raw:=13860864,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2143),
rec(k:=15169,first:=1,last:=376,unitFirst:=398,unitLast:=773,order:=49152,autOrder:=6291456,parity:=3,classes:=376,raw:=18481152,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1779),
rec(k:=15170,first:=1,last:=142,unitFirst:=774,unitLast:=915,order:=49152,autOrder:=3145728,parity:=1,classes:=768,raw:=37748736,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1358)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard448_v7_gpt56sol.g");
