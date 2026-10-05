# Exact wrapper for sealed degree-24 seed workload shard484.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD484_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD484_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD484_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard484_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="EC45883A25869E8226423D0BD83D503EA21B57E8FDC637FC57005AEAA43FD6B2";
S484_RECORDS:=[
rec(k:=15244,first:=147,last:=160,unitFirst:=1,unitLast:=14,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1084),
rec(k:=15245,first:=1,last:=208,unitFirst:=15,unitLast:=222,order:=49152,autOrder:=1572864,parity:=15,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2764),
rec(k:=15246,first:=1,last:=272,unitFirst:=223,unitLast:=494,order:=49152,autOrder:=1572864,parity:=15,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1987),
rec(k:=15247,first:=1,last:=320,unitFirst:=495,unitLast:=814,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1788),
rec(k:=15248,first:=1,last:=101,unitFirst:=815,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=360,raw:=17694720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2000)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard484_v7_gpt56sol.g");
