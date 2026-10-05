# Exact wrapper for sealed degree-24 seed workload shard599.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD599_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD599_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD599_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard599_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7D766D9861A706A28BD8AE2902FE7CF3E5D9B86C184AFF177FC4AA4C9AE48F0A";
S599_RECORDS:=[
rec(k:=15561,first:=911,last:=1050,unitFirst:=1,unitLast:=140,order:=49152,autOrder:=3145728,parity:=7,classes:=1050,raw:=51609600,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1779),
rec(k:=15562,first:=1,last:=204,unitFirst:=141,unitLast:=344,order:=49152,autOrder:=786432,parity:=7,classes:=204,raw:=10027008,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1103),
rec(k:=15563,first:=1,last:=236,unitFirst:=345,unitLast:=580,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1677),
rec(k:=15564,first:=1,last:=40,unitFirst:=581,unitLast:=620,order:=49152,autOrder:=393216,parity:=7,classes:=40,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=956),
rec(k:=15565,first:=1,last:=128,unitFirst:=621,unitLast:=748,order:=49152,autOrder:=4718592,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1139),
rec(k:=15566,first:=1,last:=167,unitFirst:=749,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2579)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard599_v7_gpt56sol.g");
