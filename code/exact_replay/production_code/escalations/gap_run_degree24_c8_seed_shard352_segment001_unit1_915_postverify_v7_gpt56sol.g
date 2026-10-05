# Exact wrapper for sealed degree-24 seed workload shard352.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD352_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD352_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD352_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard352_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="56765486AD89C4C3CD8C513FE40F83DF944EF619926BE633EC90BD0A6BAF24F6";
S352_RECORDS:=[
rec(k:=14866,first:=192,last:=334,unitFirst:=1,unitLast:=143,order:=49152,autOrder:=3145728,parity:=3,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2994),
rec(k:=14867,first:=1,last:=276,unitFirst:=144,unitLast:=419,order:=49152,autOrder:=3145728,parity:=3,classes:=276,raw:=13565952,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3461),
rec(k:=14868,first:=1,last:=334,unitFirst:=420,unitLast:=753,order:=49152,autOrder:=3145728,parity:=3,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2649),
rec(k:=14869,first:=1,last:=162,unitFirst:=754,unitLast:=915,order:=49152,autOrder:=6291456,parity:=7,classes:=364,raw:=17891328,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1853)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard352_v7_gpt56sol.g");
