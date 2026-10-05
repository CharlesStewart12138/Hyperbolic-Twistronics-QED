# Exact wrapper for sealed degree-24 seed workload shard586.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD586_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD586_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD586_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard586_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D6D954961F56BD8D61C4FAFD4CD78E86DE53ED30FA12DD7A1300A3CDA6BB856B";
S586_RECORDS:=[
rec(k:=15530,first:=10,last:=320,unitFirst:=1,unitLast:=311,order:=49152,autOrder:=393216,parity:=7,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1030),
rec(k:=15531,first:=1,last:=212,unitFirst:=312,unitLast:=523,order:=49152,autOrder:=1572864,parity:=7,classes:=212,raw:=10420224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1002),
rec(k:=15532,first:=1,last:=256,unitFirst:=524,unitLast:=779,order:=49152,autOrder:=393216,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1535),
rec(k:=15533,first:=1,last:=132,unitFirst:=780,unitLast:=911,order:=49152,autOrder:=1572864,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2067),
rec(k:=15534,first:=1,last:=4,unitFirst:=912,unitLast:=915,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1027)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard586_v7_gpt56sol.g");
