# Exact wrapper for sealed degree-24 seed workload shard353.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD353_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD353_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD353_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard353_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="38F5B07F68E9F1D5A82DC2D35F33F3F8CC74FE1590C89F502AC8EA78EF585B21";
S353_RECORDS:=[
rec(k:=14869,first:=163,last:=364,unitFirst:=1,unitLast:=202,order:=49152,autOrder:=6291456,parity:=7,classes:=364,raw:=17891328,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1853),
rec(k:=14870,first:=1,last:=64,unitFirst:=203,unitLast:=266,order:=49152,autOrder:=1572864,parity:=7,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1797),
rec(k:=14871,first:=1,last:=236,unitFirst:=267,unitLast:=502,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2433),
rec(k:=14872,first:=1,last:=64,unitFirst:=503,unitLast:=566,order:=49152,autOrder:=1572864,parity:=3,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2875),
rec(k:=14873,first:=1,last:=236,unitFirst:=567,unitLast:=802,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1621),
rec(k:=14874,first:=1,last:=113,unitFirst:=803,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=284,raw:=13959168,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2031)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard353_v7_gpt56sol.g");
