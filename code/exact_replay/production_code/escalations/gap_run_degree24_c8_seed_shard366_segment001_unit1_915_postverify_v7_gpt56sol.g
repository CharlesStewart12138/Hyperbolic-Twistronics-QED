# Exact wrapper for sealed degree-24 seed workload shard366.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD366_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD366_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD366_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard366_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BE216FB3D6587528B1573DF211898782AC9C2FC2F33D0EDCB052B0B372FC0FD3";
S366_RECORDS:=[
rec(k:=14920,first:=18,last:=48,unitFirst:=1,unitLast:=31,order:=49152,autOrder:=1572864,parity:=1,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1123),
rec(k:=14921,first:=1,last:=120,unitFirst:=32,unitLast:=151,order:=49152,autOrder:=3145728,parity:=1,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1739),
rec(k:=14922,first:=1,last:=76,unitFirst:=152,unitLast:=227,order:=49152,autOrder:=1572864,parity:=1,classes:=76,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1489),
rec(k:=14923,first:=1,last:=312,unitFirst:=228,unitLast:=539,order:=49152,autOrder:=6291456,parity:=3,classes:=312,raw:=15335424,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2402),
rec(k:=14924,first:=1,last:=260,unitFirst:=540,unitLast:=799,order:=49152,autOrder:=6291456,parity:=3,classes:=260,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2582),
rec(k:=14925,first:=1,last:=116,unitFirst:=800,unitLast:=915,order:=49152,autOrder:=3145728,parity:=1,classes:=192,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1311)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard366_v7_gpt56sol.g");
