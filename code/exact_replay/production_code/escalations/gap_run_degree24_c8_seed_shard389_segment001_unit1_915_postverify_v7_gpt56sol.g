# Exact wrapper for sealed degree-24 seed workload shard389.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD389_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD389_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD389_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard389_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6EB18A997ECA7D4C6AD5D29AD9FEBDF90007224A4E83E0CE772F1AE0A6B078E6";
S389_RECORDS:=[
rec(k:=15000,first:=61,last:=272,unitFirst:=1,unitLast:=212,order:=49152,autOrder:=1572864,parity:=15,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1626),
rec(k:=15001,first:=1,last:=272,unitFirst:=213,unitLast:=484,order:=49152,autOrder:=3145728,parity:=7,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1561),
rec(k:=15002,first:=1,last:=96,unitFirst:=485,unitLast:=580,order:=49152,autOrder:=1572864,parity:=7,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1856),
rec(k:=15003,first:=1,last:=32,unitFirst:=581,unitLast:=612,order:=49152,autOrder:=393216,parity:=15,classes:=32,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=894),
rec(k:=15004,first:=1,last:=236,unitFirst:=613,unitLast:=848,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1397),
rec(k:=15005,first:=1,last:=67,unitFirst:=849,unitLast:=915,order:=49152,autOrder:=9437184,parity:=3,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1799)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard389_v7_gpt56sol.g");
