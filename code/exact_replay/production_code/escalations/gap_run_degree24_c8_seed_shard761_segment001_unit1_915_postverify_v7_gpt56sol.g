# Exact wrapper for sealed degree-24 seed workload shard761.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD761_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD761_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD761_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard761_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9CE0AB3EC2C5AA3E33EFC1C6BD6C7F9469CB81397184BD1A891D9162547B4235";
S761_RECORDS:=[
rec(k:=15825,first:=1119,last:=1600,unitFirst:=1,unitLast:=482,order:=49152,autOrder:=1572864,parity:=7,classes:=1600,raw:=78643200,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2569),
rec(k:=15826,first:=1,last:=72,unitFirst:=483,unitLast:=554,order:=49152,autOrder:=1572864,parity:=7,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1546),
rec(k:=15827,first:=1,last:=240,unitFirst:=555,unitLast:=794,order:=49152,autOrder:=786432,parity:=7,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1218),
rec(k:=15828,first:=1,last:=121,unitFirst:=795,unitLast:=915,order:=49152,autOrder:=786432,parity:=7,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1715)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard761_v7_gpt56sol.g");
