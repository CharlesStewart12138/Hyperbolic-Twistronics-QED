# Exact wrapper for sealed degree-24 seed workload shard354.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD354_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD354_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD354_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard354_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="434208B1763EEB2A663ACD9AA6EC20DA37F3B4906CE724DCCDFB6C26D1A2EEBA";
S354_RECORDS:=[
rec(k:=14874,first:=114,last:=284,unitFirst:=1,unitLast:=171,order:=49152,autOrder:=6291456,parity:=3,classes:=284,raw:=13959168,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2031),
rec(k:=14875,first:=1,last:=240,unitFirst:=172,unitLast:=411,order:=49152,autOrder:=3145728,parity:=7,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2222),
rec(k:=14876,first:=1,last:=64,unitFirst:=412,unitLast:=475,order:=49152,autOrder:=1572864,parity:=7,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1914),
rec(k:=14877,first:=1,last:=236,unitFirst:=476,unitLast:=711,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2198),
rec(k:=14878,first:=1,last:=64,unitFirst:=712,unitLast:=775,order:=49152,autOrder:=1572864,parity:=3,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2134),
rec(k:=14879,first:=1,last:=140,unitFirst:=776,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2238)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard354_v7_gpt56sol.g");
