# Exact wrapper for sealed degree-24 seed workload shard362.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD362_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD362_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD362_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard362_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="828BE42C867913A0F52531F3383A9B5056619C2C5058665FE023E350F42CA094";
S362_RECORDS:=[
rec(k:=14907,first:=618,last:=864,unitFirst:=1,unitLast:=247,order:=49152,autOrder:=12582912,parity:=3,classes:=864,raw:=42467328,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2660),
rec(k:=14908,first:=1,last:=308,unitFirst:=248,unitLast:=555,order:=49152,autOrder:=3145728,parity:=3,classes:=308,raw:=15138816,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1840),
rec(k:=14909,first:=1,last:=312,unitFirst:=556,unitLast:=867,order:=49152,autOrder:=6291456,parity:=3,classes:=312,raw:=15335424,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2059),
rec(k:=14910,first:=1,last:=48,unitFirst:=868,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1486)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard362_v7_gpt56sol.g");
