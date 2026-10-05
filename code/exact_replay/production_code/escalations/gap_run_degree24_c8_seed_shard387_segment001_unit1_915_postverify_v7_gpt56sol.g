# Exact wrapper for sealed degree-24 seed workload shard387.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD387_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD387_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD387_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard387_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A92A80C23EF26E90A0896AC1678F832B3F17592D69BCBE6422631C67F93531F2";
S387_RECORDS:=[
rec(k:=14990,first:=205,last:=422,unitFirst:=1,unitLast:=218,order:=49152,autOrder:=6291456,parity:=1,classes:=422,raw:=20742144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3633),
rec(k:=14991,first:=1,last:=316,unitFirst:=219,unitLast:=534,order:=49152,autOrder:=1572864,parity:=15,classes:=316,raw:=15532032,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1734),
rec(k:=14992,first:=1,last:=236,unitFirst:=535,unitLast:=770,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2159),
rec(k:=14993,first:=1,last:=64,unitFirst:=771,unitLast:=834,order:=49152,autOrder:=1572864,parity:=3,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2576),
rec(k:=14994,first:=1,last:=81,unitFirst:=835,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2561)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard387_v7_gpt56sol.g");
