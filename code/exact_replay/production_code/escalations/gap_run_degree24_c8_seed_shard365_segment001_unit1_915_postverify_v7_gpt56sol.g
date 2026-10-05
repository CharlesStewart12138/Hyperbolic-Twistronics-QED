# Exact wrapper for sealed degree-24 seed workload shard365.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD365_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD365_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD365_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard365_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3124C06D1987DD8293BCD8ACF42AF33456C155CBFA2533229B272AFBA8F349D9";
S365_RECORDS:=[
rec(k:=14911,first:=1623,last:=1820,unitFirst:=1,unitLast:=198,order:=49152,autOrder:=100663296,parity:=7,classes:=1820,raw:=89456640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=6200),
rec(k:=14912,first:=1,last:=260,unitFirst:=199,unitLast:=458,order:=49152,autOrder:=6291456,parity:=3,classes:=260,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=5396),
rec(k:=14913,first:=1,last:=208,unitFirst:=459,unitLast:=666,order:=49152,autOrder:=3145728,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2109),
rec(k:=14914,first:=1,last:=120,unitFirst:=667,unitLast:=786,order:=49152,autOrder:=1572864,parity:=1,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1395),
rec(k:=14919,first:=1,last:=112,unitFirst:=787,unitLast:=898,order:=49152,autOrder:=6291456,parity:=1,classes:=112,raw:=5505024,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1528),
rec(k:=14920,first:=1,last:=17,unitFirst:=899,unitLast:=915,order:=49152,autOrder:=1572864,parity:=1,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1123)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard365_v7_gpt56sol.g");
