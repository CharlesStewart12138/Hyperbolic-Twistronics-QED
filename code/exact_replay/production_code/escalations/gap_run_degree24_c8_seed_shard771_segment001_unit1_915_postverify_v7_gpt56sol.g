# Exact wrapper for sealed degree-24 seed workload shard771.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD771_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD771_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD771_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard771_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2CF7E0EFAAC7BC592E2CE354859F77FACA565ED4398D34EDCC13379C09EA199B";
S771_RECORDS:=[
rec(k:=15836,first:=121,last:=272,unitFirst:=1,unitLast:=152,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4032),
rec(k:=15837,first:=1,last:=292,unitFirst:=153,unitLast:=444,order:=49152,autOrder:=3145728,parity:=7,classes:=292,raw:=14352384,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1847),
rec(k:=15838,first:=1,last:=370,unitFirst:=445,unitLast:=814,order:=49152,autOrder:=6291456,parity:=7,classes:=370,raw:=18186240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2734),
rec(k:=15839,first:=1,last:=101,unitFirst:=815,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=360,raw:=17694720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1680)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard771_v7_gpt56sol.g");
