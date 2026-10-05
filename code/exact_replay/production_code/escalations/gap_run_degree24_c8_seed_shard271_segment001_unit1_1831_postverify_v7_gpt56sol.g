# Exact wrapper for sealed degree-24 seed workload shard271.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD271_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD271_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD271_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard271_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="35C6DB201FB8A482E30BD07CA5A6EA5DEF7C5C59EAF58D976D853A1655FF787E";
S271_RECORDS:=[
rec(k:=13797,first:=1338,last:=2928,unitFirst:=1,unitLast:=1591,order:=24576,autOrder:=3145728,parity:=1,classes:=2928,raw:=71958528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4906),
rec(k:=13798,first:=1,last:=136,unitFirst:=1592,unitLast:=1727,order:=24576,autOrder:=1572864,parity:=1,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1554),
rec(k:=13799,first:=1,last:=104,unitFirst:=1728,unitLast:=1831,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1099)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard271_v7_gpt56sol.g");
