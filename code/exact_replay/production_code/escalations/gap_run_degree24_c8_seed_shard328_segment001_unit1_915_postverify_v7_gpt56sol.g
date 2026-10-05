# Exact wrapper for sealed degree-24 seed workload shard328.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD328_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD328_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD328_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard328_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E04C6C85DA8090B144730CCFC2F0B83979BD34BF69282F15C3FEDE1057CAD903";
S328_RECORDS:=[
rec(k:=14749,first:=34,last:=172,unitFirst:=1,unitLast:=139,order:=49152,autOrder:=6291456,parity:=1,classes:=172,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2820),
rec(k:=14750,first:=1,last:=172,unitFirst:=140,unitLast:=311,order:=49152,autOrder:=6291456,parity:=1,classes:=172,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2603),
rec(k:=14751,first:=1,last:=208,unitFirst:=312,unitLast:=519,order:=49152,autOrder:=6291456,parity:=1,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2410),
rec(k:=14752,first:=1,last:=208,unitFirst:=520,unitLast:=727,order:=49152,autOrder:=6291456,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1640),
rec(k:=14753,first:=1,last:=104,unitFirst:=728,unitLast:=831,order:=49152,autOrder:=1572864,parity:=1,classes:=104,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1378),
rec(k:=14754,first:=1,last:=84,unitFirst:=832,unitLast:=915,order:=49152,autOrder:=1572864,parity:=1,classes:=104,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1741)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard328_v7_gpt56sol.g");
