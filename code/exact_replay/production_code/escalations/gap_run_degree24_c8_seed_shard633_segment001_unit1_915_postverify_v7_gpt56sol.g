# Exact wrapper for sealed degree-24 seed workload shard633.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD633_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD633_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD633_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard633_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="F3AD6D4FF89A0ACF8AADD1EFA08B77E1E7776CF41083815819AF50C92A6C932F";
S633_RECORDS:=[
rec(k:=15643,first:=116,last:=304,unitFirst:=1,unitLast:=189,order:=49152,autOrder:=1572864,parity:=7,classes:=304,raw:=14942208,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3365),
rec(k:=15644,first:=1,last:=208,unitFirst:=190,unitLast:=397,order:=49152,autOrder:=1572864,parity:=7,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1240),
rec(k:=15645,first:=1,last:=72,unitFirst:=398,unitLast:=469,order:=49152,autOrder:=1572864,parity:=7,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1489),
rec(k:=15646,first:=1,last:=168,unitFirst:=470,unitLast:=637,order:=49152,autOrder:=1572864,parity:=7,classes:=168,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1690),
rec(k:=15647,first:=1,last:=276,unitFirst:=638,unitLast:=913,order:=49152,autOrder:=1572864,parity:=3,classes:=276,raw:=13565952,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2557),
rec(k:=15648,first:=1,last:=2,unitFirst:=914,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1915)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard633_v7_gpt56sol.g");
