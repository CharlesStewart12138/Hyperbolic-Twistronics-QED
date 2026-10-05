# Exact wrapper for sealed degree-24 seed workload shard783.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD783_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD783_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD783_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard783_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E4310DEC4E6A142CC01FB8C7B7E17B9F529FF218FC487FABBA9683FFC6B09193";
S783_RECORDS:=[
rec(k:=15853,first:=324,last:=484,unitFirst:=1,unitLast:=161,order:=49152,autOrder:=786432,parity:=7,classes:=484,raw:=23789568,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2123),
rec(k:=15854,first:=1,last:=144,unitFirst:=162,unitLast:=305,order:=49152,autOrder:=786432,parity:=7,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1641),
rec(k:=15855,first:=1,last:=610,unitFirst:=306,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=1248,raw:=61341696,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3367)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard783_v7_gpt56sol.g");
