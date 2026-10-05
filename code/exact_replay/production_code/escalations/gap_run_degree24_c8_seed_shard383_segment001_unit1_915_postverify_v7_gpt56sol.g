# Exact wrapper for sealed degree-24 seed workload shard383.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD383_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD383_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD383_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard383_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="452F59B3CAC0FFFA26227DA055D74CF9AFA759CA6F43318465DF26CFF82C7733";
S383_RECORDS:=[
rec(k:=14981,first:=87,last:=134,unitFirst:=1,unitLast:=48,order:=49152,autOrder:=1572864,parity:=3,classes:=134,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1699),
rec(k:=14982,first:=1,last:=282,unitFirst:=49,unitLast:=330,order:=49152,autOrder:=6291456,parity:=3,classes:=282,raw:=13860864,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2740),
rec(k:=14983,first:=1,last:=256,unitFirst:=331,unitLast:=586,order:=49152,autOrder:=3145728,parity:=3,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1992),
rec(k:=14984,first:=1,last:=108,unitFirst:=587,unitLast:=694,order:=49152,autOrder:=1572864,parity:=1,classes:=108,raw:=5308416,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1500),
rec(k:=14985,first:=1,last:=221,unitFirst:=695,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=466,raw:=22904832,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1597)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard383_v7_gpt56sol.g");
