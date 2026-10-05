# Exact wrapper for sealed degree-24 seed workload shard530.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD530_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD530_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD530_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard530_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A3B90659C87510BE5459CEEE56B279CA78B5B52AE5396A3CB423A8C85CFAE823";
S530_RECORDS:=[
rec(k:=15360,first:=769,last:=1056,unitFirst:=1,unitLast:=288,order:=49152,autOrder:=12582912,parity:=7,classes:=1056,raw:=51904512,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2697),
rec(k:=15361,first:=1,last:=132,unitFirst:=289,unitLast:=420,order:=49152,autOrder:=3145728,parity:=1,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1949),
rec(k:=15362,first:=1,last:=320,unitFirst:=421,unitLast:=740,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1855),
rec(k:=15363,first:=1,last:=175,unitFirst:=741,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=1376,raw:=67633152,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3685)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard530_v7_gpt56sol.g");
