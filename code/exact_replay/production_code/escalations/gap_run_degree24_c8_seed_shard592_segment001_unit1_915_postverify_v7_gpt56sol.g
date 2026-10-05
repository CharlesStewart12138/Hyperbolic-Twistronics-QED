# Exact wrapper for sealed degree-24 seed workload shard592.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD592_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD592_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD592_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard592_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C92A92937684442E642313B8FE45CC966860BBD5318F2278B303DFCEC6EC3BF0";
S592_RECORDS:=[
rec(k:=15548,first:=800,last:=1228,unitFirst:=1,unitLast:=429,order:=49152,autOrder:=3145728,parity:=15,classes:=1228,raw:=60358656,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3516),
rec(k:=15549,first:=1,last:=60,unitFirst:=430,unitLast:=489,order:=49152,autOrder:=393216,parity:=7,classes:=60,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=911),
rec(k:=15550,first:=1,last:=136,unitFirst:=490,unitLast:=625,order:=49152,autOrder:=393216,parity:=7,classes:=136,raw:=6684672,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1180),
rec(k:=15551,first:=1,last:=208,unitFirst:=626,unitLast:=833,order:=49152,autOrder:=1572864,parity:=31,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1851),
rec(k:=15552,first:=1,last:=82,unitFirst:=834,unitLast:=915,order:=49152,autOrder:=1572864,parity:=31,classes:=1120,raw:=55050240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2178)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard592_v7_gpt56sol.g");
