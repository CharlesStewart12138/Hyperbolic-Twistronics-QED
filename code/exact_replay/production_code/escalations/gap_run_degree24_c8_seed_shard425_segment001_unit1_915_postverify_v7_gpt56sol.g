# Exact wrapper for sealed degree-24 seed workload shard425.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD425_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD425_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD425_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard425_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1B13617078A78DF24D457BBFB15F69CF10AE80EDE57081988FE1030928234E52";
S425_RECORDS:=[
rec(k:=15114,first:=161,last:=320,unitFirst:=1,unitLast:=160,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1831),
rec(k:=15115,first:=1,last:=288,unitFirst:=161,unitLast:=448,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1622),
rec(k:=15116,first:=1,last:=288,unitFirst:=449,unitLast:=736,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1621),
rec(k:=15117,first:=1,last:=179,unitFirst:=737,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=512,raw:=25165824,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2773)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard425_v7_gpt56sol.g");
