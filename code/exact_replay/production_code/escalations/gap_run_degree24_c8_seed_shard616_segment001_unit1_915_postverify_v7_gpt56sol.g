# Exact wrapper for sealed degree-24 seed workload shard616.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD616_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD616_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD616_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard616_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7412AFFE4E49D7345EA828E77244B851959C273E20F968E7D1901CF13409B7BC";
S616_RECORDS:=[
rec(k:=15592,first:=29,last:=168,unitFirst:=1,unitLast:=140,order:=49152,autOrder:=1572864,parity:=3,classes:=168,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2080),
rec(k:=15593,first:=1,last:=72,unitFirst:=141,unitLast:=212,order:=49152,autOrder:=4718592,parity:=7,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1231),
rec(k:=15594,first:=1,last:=132,unitFirst:=213,unitLast:=344,order:=49152,autOrder:=1572864,parity:=3,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1941),
rec(k:=15595,first:=1,last:=276,unitFirst:=345,unitLast:=620,order:=49152,autOrder:=1572864,parity:=7,classes:=276,raw:=13565952,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1645),
rec(k:=15596,first:=1,last:=295,unitFirst:=621,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2014)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard616_v7_gpt56sol.g");
