# Exact wrapper for sealed degree-24 seed workload shard395.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD395_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD395_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD395_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard395_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2775076F99969EC655ADBA3E3159BE7871065C26F5D28001E53382B82D39639A";
S395_RECORDS:=[
rec(k:=15027,first:=33,last:=242,unitFirst:=1,unitLast:=210,order:=49152,autOrder:=9437184,parity:=3,classes:=242,raw:=11894784,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1075),
rec(k:=15028,first:=1,last:=360,unitFirst:=211,unitLast:=570,order:=49152,autOrder:=786432,parity:=15,classes:=360,raw:=17694720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1568),
rec(k:=15029,first:=1,last:=256,unitFirst:=571,unitLast:=826,order:=49152,autOrder:=393216,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1465),
rec(k:=15030,first:=1,last:=89,unitFirst:=827,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3320)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard395_v7_gpt56sol.g");
