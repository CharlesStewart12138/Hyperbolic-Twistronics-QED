# Exact wrapper for sealed degree-24 seed workload shard357.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD357_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD357_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD357_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard357_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="AAAFC4E670294C87E164E75631F7C35410E16C9847107102C6C82D56FBEA4E58";
S357_RECORDS:=[
rec(k:=14887,first:=171,last:=184,unitFirst:=1,unitLast:=14,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2277),
rec(k:=14888,first:=1,last:=208,unitFirst:=15,unitLast:=222,order:=49152,autOrder:=1572864,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2455),
rec(k:=14889,first:=1,last:=160,unitFirst:=223,unitLast:=382,order:=49152,autOrder:=1572864,parity:=3,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2369),
rec(k:=14890,first:=1,last:=180,unitFirst:=383,unitLast:=562,order:=49152,autOrder:=1572864,parity:=3,classes:=180,raw:=8847360,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1945),
rec(k:=14891,first:=1,last:=184,unitFirst:=563,unitLast:=746,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1689),
rec(k:=14892,first:=1,last:=168,unitFirst:=747,unitLast:=914,order:=49152,autOrder:=1572864,parity:=3,classes:=168,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2105),
rec(k:=14893,first:=1,last:=1,unitFirst:=915,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=444,raw:=21823488,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2197)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard357_v7_gpt56sol.g");
