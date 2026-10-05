# Exact wrapper for sealed degree-24 seed workload shard433.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD433_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD433_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD433_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard433_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C69916768281198356ECCB5AC10279D8872BDB74725DDD3565836C2F76E7D4E2";
S433_RECORDS:=[
rec(k:=15136,first:=112,last:=256,unitFirst:=1,unitLast:=145,order:=49152,autOrder:=3145728,parity:=3,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1468),
rec(k:=15137,first:=1,last:=94,unitFirst:=146,unitLast:=239,order:=49152,autOrder:=786432,parity:=1,classes:=94,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1504),
rec(k:=15138,first:=1,last:=96,unitFirst:=240,unitLast:=335,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=961),
rec(k:=15139,first:=1,last:=480,unitFirst:=336,unitLast:=815,order:=49152,autOrder:=786432,parity:=3,classes:=480,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1069),
rec(k:=15140,first:=1,last:=100,unitFirst:=816,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1460)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard433_v7_gpt56sol.g");
