# Exact wrapper for sealed degree-24 seed workload shard379.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD379_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD379_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD379_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard379_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="39F39B56B246B2B2F0729698A509341586F7FA7C64FE07F61266C00AAE0FA3D1";
S379_RECORDS:=[
rec(k:=14964,first:=215,last:=288,unitFirst:=1,unitLast:=74,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1650),
rec(k:=14965,first:=1,last:=152,unitFirst:=75,unitLast:=226,order:=49152,autOrder:=786432,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1090),
rec(k:=14966,first:=1,last:=104,unitFirst:=227,unitLast:=330,order:=49152,autOrder:=786432,parity:=3,classes:=104,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1152),
rec(k:=14967,first:=1,last:=92,unitFirst:=331,unitLast:=422,order:=49152,autOrder:=786432,parity:=1,classes:=92,raw:=4521984,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=996),
rec(k:=14968,first:=1,last:=124,unitFirst:=423,unitLast:=546,order:=49152,autOrder:=786432,parity:=1,classes:=124,raw:=6094848,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1217),
rec(k:=14969,first:=1,last:=360,unitFirst:=547,unitLast:=906,order:=49152,autOrder:=3145728,parity:=3,classes:=360,raw:=17694720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1949),
rec(k:=14970,first:=1,last:=9,unitFirst:=907,unitLast:=915,order:=49152,autOrder:=786432,parity:=1,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=868)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard379_v7_gpt56sol.g");
