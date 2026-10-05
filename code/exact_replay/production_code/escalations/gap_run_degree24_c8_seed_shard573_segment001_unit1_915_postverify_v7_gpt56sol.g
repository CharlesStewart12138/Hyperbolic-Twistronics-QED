# Exact wrapper for sealed degree-24 seed workload shard573.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD573_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD573_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD573_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard573_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="593688FBD2AF5C6A275AF7975F172D14D8EE84B5A10B9CEF7DF50D9CC68FBF89";
S573_RECORDS:=[
rec(k:=15479,first:=7,last:=96,unitFirst:=1,unitLast:=90,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3006),
rec(k:=15480,first:=1,last:=148,unitFirst:=91,unitLast:=238,order:=49152,autOrder:=3145728,parity:=3,classes:=148,raw:=7274496,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2618),
rec(k:=15481,first:=1,last:=64,unitFirst:=239,unitLast:=302,order:=49152,autOrder:=1572864,parity:=3,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2744),
rec(k:=15482,first:=1,last:=96,unitFirst:=303,unitLast:=398,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2106),
rec(k:=15483,first:=1,last:=148,unitFirst:=399,unitLast:=546,order:=49152,autOrder:=3145728,parity:=3,classes:=148,raw:=7274496,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2348),
rec(k:=15484,first:=1,last:=96,unitFirst:=547,unitLast:=642,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2336),
rec(k:=15485,first:=1,last:=96,unitFirst:=643,unitLast:=738,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3034),
rec(k:=15486,first:=1,last:=96,unitFirst:=739,unitLast:=834,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2284),
rec(k:=15487,first:=1,last:=81,unitFirst:=835,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1540)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard573_v7_gpt56sol.g");
